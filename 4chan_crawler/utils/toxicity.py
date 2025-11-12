# utils/toxicity.py
from __future__ import annotations
import datetime
from utils.logger import Logger
from utils.plsql import PLSQL
from utils.perspective import clean_html, score_text
from modal.post_toxicity import PostToxicity
from constants.plsql_constants import SELECT_LATEST_POST_TEXT, UPSERT_POST_TOXICITY
from utils.faktory import initialize_producer
from constants.constants import TOX_QUEUE, TOX_JOBTYPE   # <— use your constants

logger = Logger("Toxicity").get_logger()

def score_and_upsert(board_name: str, post_no: int, language: str | None = None) -> dict | None:
    """
    Fetch latest text for (board_name, post_no) -> call Perspective -> upsert into post_toxicity.
    Returns the scores dict or None if post not found or text is empty.
    """
    pl = PLSQL()
    try:
        rows = pl.get_data_from(SELECT_LATEST_POST_TEXT, (board_name, post_no))
        if not rows:
            logger.info("Post not found: %s/%s", board_name, post_no)
            return None

        _, _, html = rows[0]
        text = clean_html(html)

        # Skip empty text (saves quota, avoids API errors)
        if not text or not text.strip():
            logger.info("Empty/whitespace-only text for %s/%s; skipping score", board_name, post_no)
            return None

        scores = score_text(text, language)

        model = PostToxicity.from_scores(board_name, post_no, language, scores)
        pl.insert_into_db(UPSERT_POST_TOXICITY, model.to_upsert_tuple())
        logger.info("Upserted toxicity for %s/%s", board_name, post_no)
        return scores
    finally:
        pl.close_connection()

def enqueue_toxicity(board_name: str, post_no: int, delay_seconds: int = 0):
    """
    Enqueue a toxicity job using your pyfaktory wrapper.
    delay_seconds=0 means 'run now'.
    """
    delay = datetime.timedelta(seconds=delay_seconds)
    initialize_producer(
        queue=TOX_QUEUE,                 # <— constants
        jobtype=TOX_JOBTYPE,             # <— constants
        delayedTimer=delay,
        args=[{"board_name": board_name, "post_no": int(post_no)}],
    )
    logger.info("Enqueued job for %s/%s (delay=%ss)", board_name, post_no, delay_seconds)
