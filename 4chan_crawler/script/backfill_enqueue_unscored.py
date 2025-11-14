import os
import sys
from pathlib import Path

# Make sure Python can find the 4chan_crawler package (one level up from /script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from utils.logger import Logger
from utils.plsql import PLSQL
from constants.plsql_constants import SELECT_UNSCORED_POSTS
from utils.faktory import initialize_producer

logger = Logger("backfill_enqueue_unscored").get_logger()

def main(limit: int = 5000):
    db = PLSQL()
    try:
        rows = db.get_data_from(SELECT_UNSCORED_POSTS, (limit,))
        logger.info("Backfill: found %d unscored posts", len(rows))
        for board_name, post_no in rows:
            initialize_producer(
                queue="toxicity",
                jobtype="score_post_toxicity",
                delayedTimer=None,          # run now
                args=[{"board_name": board_name, "post_no": int(post_no)}],
            )
        logger.info("Backfill: enqueued %d jobs", len(rows))
    finally:
        db.close_connection()

if __name__ == "__main__":
    lim = int(os.getenv("BACKFILL_LIMIT", "5000"))
    main(limit=lim)
