# toxicity_consumer.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from dotenv import load_dotenv
from utils.logger import Logger
from utils.faktory import initialize_consumer
from utils.toxicity import score_and_upsert
from constants.constants import (
    TOX_QUEUE,
    TOX_JOBTYPE,
    DEFAULT_LANG_ENV,
    FAKTORY_SERVER_URL,   # for logging the faktory URL
)

# Load the package .env (same pattern as other utils)
load_dotenv(Path(__file__).resolve().parent / ".env")

logger = Logger("toxicity_consumer").get_logger()


def _extract_payload(args: tuple, kwargs: dict) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    """
    Accepts either kwargs or args and extracts:
      board_name (str), post_no (int), language (str|None)

    Supported job shapes:
      args=[{'board_name':'pol','post_no':123,'language':'en'}]
      args=['pol', 123]      # optional fallback
      kwargs={'board_name':'pol','post_no':123,'language':'en'}
    """
    board = None
    post_no = None
    lang = None

    # Prefer kwargs if present
    if kwargs:
        board = kwargs.get("board_name") or kwargs.get("board")
        post_no = kwargs.get("post_no") or kwargs.get("no")
        lang = kwargs.get("language")

    # Fallback to args
    if (board is None or post_no is None) and args:
        if len(args) == 1 and isinstance(args[0], dict):
            d: Dict[str, Any] = args[0]
            board = board or d.get("board_name") or d.get("board")
            post_no = post_no or d.get("post_no") or d.get("no")
            lang = lang or d.get("language")
        elif len(args) >= 2 and isinstance(args[0], str):
            board = board or args[0]
            try:
                post_no = post_no or int(args[1])
            except Exception:
                pass

    # Normalize post_no if it's a digit string
    if isinstance(post_no, str) and post_no.isdigit():
        post_no = int(post_no)

    return board, post_no, lang


def score_post_toxicity_handler(*args, **kwargs):
    """
    Handler registered with pyfaktory Consumer.
    Your producer sends args=[{'board_name': 'pol', 'post_no': 123}] by default.
    """
    logger.debug("Received job payload args=%r kwargs=%r", args, kwargs)
    board, post_no, lang = _extract_payload(args, kwargs)

    if not board or post_no is None:
        logger.warning("Invalid toxicity job payload: args=%r kwargs=%r", args, kwargs)
        return

    if not lang:
        lang = os.getenv(DEFAULT_LANG_ENV, "en")

    logger.info("Scoring toxicity for %s/%s (lang=%s)", board, post_no, lang)
    try:
        scores = score_and_upsert(board, int(post_no), lang)
        if scores is None:
            logger.warning("Post not found or empty text for %s/%s", board, post_no)
            return

        logger.info(
            "Scored %s/%s: tox=%.3f sev=%.3f id=%.3f ins=%.3f thr=%.3f",
            board,
            post_no,
            (scores.get("toxicity") or 0.0),
            (scores.get("severe_toxicity") or 0.0),
            (scores.get("identity_attack") or 0.0),
            (scores.get("insult") or 0.0),
            (scores.get("threat") or 0.0),
        )
    except Exception as e:
        logger.error("Error scoring %s/%s: %s", board, post_no, e)


if __name__ == "__main__":
    # Fail fast if critical env vars are missing
    missing = [k for k in ("DATABASE_URL", "PERSPECTIVE_API_KEY") if not os.getenv(k)]
    if missing:
        logger.error("Missing required env vars: %s", ", ".join(missing))
        raise SystemExit(1)

    # Conservative default to protect your Perspective quota
    try:
        concurrency = int(os.getenv("FAKTORY_CONCURRENCY", "1"))
    except ValueError:
        concurrency = 1

    # Helpful log: which Faktory URL are we using?
    logger.info("Faktory URL: %s", os.getenv(FAKTORY_SERVER_URL, "<not set>"))
    logger.info(
        "Starting toxicity consumer: queue=%s, jobtype=%s, concurrency=%d",
        TOX_QUEUE, TOX_JOBTYPE, concurrency
    )

    initialize_consumer(
        queue=[TOX_QUEUE],
        jobtypes=[TOX_JOBTYPE],
        fn=score_post_toxicity_handler,
        concurrency=concurrency,
    )
