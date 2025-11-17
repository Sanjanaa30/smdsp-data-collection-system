from constants.constants import TOX_JOBTYPE, TOX_QUEUE
from constants.plsql_constants import SELECT_UNSCORED_POSTS
from toxicity_consumer import score_post_toxicity_handler
from utils.faktory import initialize_consumer, initialize_producer
from utils.logger import Logger
from utils.plsql import PLSQL

logger = Logger("backfill_enqueue_unscored", "back_fill_toxicity.log").get_logger()


# This class fills in missing toxicity data for posts that don't have any.
def main(boards_name, limit: int = 5000):
    db = PLSQL()
    try:
        rows = db.get_data_from(SELECT_UNSCORED_POSTS, (boards_name, limit))
        logger.info("Backfill: found %d unscored posts", len(rows))
        post_data = []
        for board_name, post_no, resto, comment in rows:
            if len(comment) < 1:
                continue
            title_or_comment = ""
            if resto == 0:
                title_or_comment = "POST"
            else:
                title_or_comment = "COMMENT"
            post_data.append(
                {
                    "board_name": board_name,
                    "titleOrComment": title_or_comment,
                    "post_no": int(post_no),
                    "comment": comment,
                }
            )
        toxicity_queue = f"{TOX_QUEUE}-{boards_name.lower()}"
        toxicity_job = f"{TOX_JOBTYPE}_{boards_name.lower()}"
        initialize_producer(
            queue=toxicity_queue,
            jobtype=toxicity_job,
            delayedTimer=None,  # run now
            args=[post_data],
        )
        initialize_consumer(
            queue=[toxicity_queue],
            jobtypes=[toxicity_job],
            fn=score_post_toxicity_handler,
            concurrency=3,
        )
        logger.info("Backfill: enqueued %d jobs", len(rows))
    except Exception as e:
        logger.error(f"while scheduling job for back filling {e}")
    finally:
        db.close_connection()


if __name__ == "__main__":
    board_name = input("Enter Board Name\n")
    limit = int(input("Enter the limit"))
    main(board_name, limit)
