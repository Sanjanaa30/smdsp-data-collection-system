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
from constants.errors_constants import ERROR429
from dotenv import load_dotenv
from utils.logger import Logger

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
logger = Logger("Perspective", "toxicity_consumer.log").get_logger()

_TAG = re.compile(r"<[^>]+>")


def clean_html(html_text: str) -> str:
    """Remove HTML tags from text."""
    no_tags = _TAG.sub("", html_text)

    # 2. Unescape HTML entities like &gt; and &#039;
    cleaned = html.unescape(no_tags)
    cleaned = re.sub(r'^>>?\d+', '', cleaned)
    cleaned = re.sub(r'^\d+', '', cleaned)
    logger.debug(f"Cleaned HTML Tags {cleaned}")
    logger.debug(f"Cleaned HTML: {len(html_text or '')} chars -> {len(cleaned)} chars")
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


def score_text(text: str) -> dict:
    """
    Calls Perspective for the attributes in PERSPECTIVE_ATTRS.
    Returns lowercase keys that match your DB columns.
    Retries a couple times on transient errors (429/5xx).
    """
    logger.info("Starting toxicity scoring for text")
    

    # text = trim_to_20kb(clean_html(text))

    

    api_key1 = os.getenv("PERSPECTIVE_API_KEY_ONE")
    api_key2 = os.getenv("PERSPECTIVE_API_KEY_TWO")
    if not api_key1:
        logger.error("PERSPECTIVE_API_KEY not set in environment variables")
        raise RuntimeError("PERSPECTIVE_API_KEY not set")

    lang = os.getenv(DEFAULT_LANG_ENV, "en")
    logger.debug(f"Using language: {lang}")

    # text = (text or "")[:2800]
    if len(text) == 0:
        logger.warning("Empty text provided, returning empty scores")
        return None

    payload = {
        "comment": {"text": text},
        "languages": [lang],
        "requestedAttributes": {attr: {} for attr in PERSPECTIVE_ATTRS},
        "doNotStore": True,
    }
    logger.debug(f"Requesting {len(PERSPECTIVE_ATTRS)} attributes from Perspective API")

    url = f"?key={api_key1}"
    current_api_key = api_key1

    # --- tiny retry loop for transient failures ---
    data = None
    for attempt in range(4):
        try:
            logger.info(f"Attempt {attempt + 1}/3: Calling Perspective API")
            client = ChanClient(PERSPECTIVE_ENDPOINT)
            response = client.make_post_request(
                endpoint=url, payload=payload, timeout=20
            )

            if response is ERROR429:
                logger.warning("Perspective API returned 429 to many requests")
                if attempt == 1:
                    sleep_s = 1.5**attempt
                    logger.warning(f"Retrying in {sleep_s:.1f}s")
                    time.sleep(sleep_s)
                if attempt == 2:
                    sleep_s = 2**attempt
                    logger.warning(f"Retrying in {sleep_s:.1f}s")
                    time.sleep(sleep_s)
                logger.info(f"API Key Changed: {current_api_key}")
                if current_api_key == api_key1:
                    current_api_key = api_key2
                    url = url = f"?key={api_key2}"
                    continue
                else:
                    current_api_key = api_key1
                    url = url = f"?key={api_key1}"
                    continue
            if response is None:
                return None
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

    if data is None:
        logger.error(
            "Failed to get valid response from Perspective API after all retries"
        )
        return None

    def v(key: str):
        try:
            value = data.get(key, {}).get("summaryScore", {}).get("value")
        except Exception as e:
            logger.warning(f"Error getting attribute {e}")
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
