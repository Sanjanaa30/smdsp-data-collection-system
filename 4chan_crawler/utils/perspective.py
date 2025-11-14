# utils/perspective.py
import html
import os
import re
import time
from pathlib import Path

import requests
from chan_client import ChanClient
from constants.api_constants import PERSPECTIVE_ENDPOINT
from constants.constants import DEFAULT_LANG_ENV, PERSPECTIVE_ATTRS
from dotenv import load_dotenv
from utils.logger import Logger

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
logger = Logger("Perspective").get_logger()

_TAG = re.compile(r"<[^>]+>")


def clean_html(html_text: str) -> str:
    """Remove HTML tags from text."""
    no_tags = _TAG.sub("", html_text)

    # 2. Unescape HTML entities like &gt; and &#039;
    cleaned = html.unescape(no_tags)
    logger.debug(f"Cleaned HTML: {len(html or '')} chars -> {len(cleaned)} chars")
    return cleaned


MAX_BYTES = 20 * 1024  # 20 KB


def trim_to_20kb(text: str) -> str:
    """
    Ensure the given text does not exceed 20 KB (UTF-8 bytes).
    Truncates safely if needed.
    """
    encoded = text.encode("utf-8")
    size = len(encoded)

    logger.debug(f"Original text size: {size} bytes")

    if size <= MAX_BYTES:
        logger.info("Text size is within limit.")
        return text

    logger.warning(f"Text exceeds 20 KB ({size} bytes). Truncating...")
    trimmed = encoded[:MAX_BYTES]
    trimmed_text = trimmed.decode("utf-8", errors="ignore")
    logger.info(f"Trimmed text to {len(trimmed_text.encode('utf-8'))} bytes.")

    return trimmed_text


def score_text(text: str, lang: str | None = None) -> dict:
    """
    Calls Perspective for the attributes in PERSPECTIVE_ATTRS.
    Returns lowercase keys that match your DB columns.
    Retries a couple times on transient errors (429/5xx).
    """
    logger.info("Starting toxicity scoring for text")

    text = trim_to_20kb(clean_html(text))
    
    logger.debug(f"Text length after cleaning: {len(text)} characters")

    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        logger.error("PERSPECTIVE_API_KEY not set in environment variables")
        raise RuntimeError("PERSPECTIVE_API_KEY not set")

    lang = lang or os.getenv(DEFAULT_LANG_ENV, "en")
    logger.debug(f"Using language: {lang}")

    # text = (text or "")[:2800]
    if len(text) == 0:
        logger.warning("Empty text provided, returning empty scores")
        return {}

    payload = {
        "comment": {"text": text},
        "languages": [lang],
        "requestedAttributes": {attr: {} for attr in PERSPECTIVE_ATTRS},
        "doNotStore": True,
    }
    logger.debug(f"Requesting {len(PERSPECTIVE_ATTRS)} attributes from Perspective API")

    url = f"?key={api_key}"

    # --- tiny retry loop for transient failures ---
    for attempt in range(3):
        try:
            logger.info(f"Attempt {attempt + 1}/3: Calling Perspective API")
            client = ChanClient(PERSPECTIVE_ENDPOINT)
            response = client.make_post_request(
                endpoint=url, payload=payload, timeout=20
            )
            logger.info("Successfully received response from Perspective API")

            data = response.get("attributeScores", {})
            logger.debug(f"Received scores for {len(data)} attributes")
            break

        except requests.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            logger.error(f"HTTP Error on attempt {attempt + 1}: Status {status}")

            # backoff on 429/5xx
            if status in (429, 500, 502, 503, 504) and attempt < 2:
                sleep_s = 1.5**attempt
                logger.warning(
                    f"Perspective API returned {status}; retrying in {sleep_s:.1f}s"
                )
                time.sleep(sleep_s)
                continue
            logger.error(f"Perspective API request failed after {attempt + 1} attempts")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error on attempt {attempt + 1}: {type(e).__name__}: {e}"
            )
            if attempt < 2:
                sleep_s = 1.5**attempt
                logger.warning(f"Retrying in {sleep_s:.1f}s")
                time.sleep(sleep_s)
                continue
            raise

    def v(key: str):
        value = data.get(key, {}).get("summaryScore", {}).get("value")
        # if value is not None:
        #     logger.debug(f"  {key}: {value:.4f}")
        return value

    logger.info("Extracting attribute scores from response")
    scores = {
        # Production attributes
        "toxicity": v("TOXICITY"),
        "severe_toxicity": v("SEVERE_TOXICITY"),
        "identity_attack": v("IDENTITY_ATTACK"),
        "insult": v("INSULT"),
        "profanity": v("PROFANITY"),
        "threat": v("THREAT"),
        "sexually_explicit": v("SEXUALLY_EXPLICIT"),
        "flirtation": v("FLIRTATION"),
        "obscene": v("OBSCENE"),
        "spam": v("SPAM"),
        "unsubstantial": v("UNSUBSTANTIAL"),
    }

    # Count how many scores were actually returned
    non_null_scores = sum(1 for v in scores.values() if v is not None)
    logger.info(
        f"Toxicity scoring complete: {non_null_scores}/{len(scores)} scores returned"
    )

    return scores
