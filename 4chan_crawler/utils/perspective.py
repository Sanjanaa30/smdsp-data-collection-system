# utils/perspective.py
import os, re, time, requests
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import Logger
from constants.api_constants import PERSPECTIVE_ENDPOINT
from constants.constants import DEFAULT_LANG_ENV, PERSPECTIVE_ATTRS

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
logger = Logger("Perspective").get_logger()

_TAG = re.compile(r"<[^>]+>")

def clean_html(html: str) -> str:
    return _TAG.sub("", html or "")

def score_text(text: str, lang: str | None = None) -> dict:
    """
    Calls Perspective for the attributes in PERSPECTIVE_ATTRS.
    Returns lowercase keys that match your DB columns.
    Retries a couple times on transient errors (429/5xx).
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY not set")

    lang = lang or os.getenv(DEFAULT_LANG_ENV, "en")
    text = (text or "")[:2800]

    payload = {
        "comment": {"text": text},
        "languages": [lang],
        "requestedAttributes": {attr: {} for attr in PERSPECTIVE_ATTRS},
        "doNotStore": True,
    }
    url = f"{PERSPECTIVE_ENDPOINT}?key={api_key}"

    # --- tiny retry loop for transient failures ---
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, timeout=20)
            r.raise_for_status()
            data = r.json().get("attributeScores", {})
            break
        except requests.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            # backoff on 429/5xx
            if status in (429, 500, 502, 503, 504) and attempt < 2:
                sleep_s = 1.5 ** attempt
                logger.warning("Perspective %s; retrying in %.1fs", status, sleep_s)
                time.sleep(sleep_s)
                continue
            raise
    # ---------------------------------------------

    def v(key: str):
        return data.get(key, {}).get("summaryScore", {}).get("value")

    return {
        "toxicity":        v("TOXICITY"),
        "severe_toxicity": v("SEVERE_TOXICITY"),
        "identity_attack": v("IDENTITY_ATTACK"),
        "insult":          v("INSULT"),
        "threat":          v("THREAT"),
    }
