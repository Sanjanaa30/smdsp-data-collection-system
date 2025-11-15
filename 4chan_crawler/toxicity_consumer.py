# toxicity_consumer.py
from utils.logger import Logger
from utils.perspective import score_text, clean_html, trim_to_20kb
from constants.plsql_constants import INSERT_BULK_TOXICITY_DATA_QUERY
from modal.toxicity import Toxicity


logger = Logger("toxicity_consumer", "toxicity_consumer.log").get_logger()


def store_toxicity_into_db(toxicity_objects):
    from utils.plsql import PLSQL

    try:
        logger.info("Inserting new toxicity scores into the database.")
        db_client = PLSQL()

        # Convert Toxicity objects to tuples for bulk insert
        toxicity_records = [tox.to_tuple() for tox in toxicity_objects]

        db_client.insert_bulk_data_into_db(
            INSERT_BULK_TOXICITY_DATA_QUERY, toxicity_records
        )

        logger.info(
            f"Successfully inserted {len(toxicity_records)} new toxicity scores into the database."
        )
    except Exception as e:
        logger.error(f"Error inserting toxicity scores into the database: {e}")
    finally:
        db_client.close_connection()


def score_post_toxicity_handler(posts: list):
    """
    Handler registered with pyfaktory Consumer.
    Your producer sends args=[{'board_name': 'pol', 'post_no': 123}] by default.
    """
    logger.info("Calculating Toxicity Scores")
    logger.debug(f"Received job payload {len(posts)}")
    # board, post_no, lang = _extract_payload(args, kwargs)

    if len(posts) < 0:
        logger.warning("Invalid toxicity job payload")
        return

    scored_toxicity_objects = []
    count = 0
    for toxicity_dict in posts:
        count = count + 1
        toxicity = Toxicity(**toxicity_dict)
        
        logger.info(
            f"🆙 Scoring toxicity for post_no = {toxicity.get_post_number()} board_name = {toxicity.get_board_name()}"
        )
        logger.debug(f"Processing {count} out of {len(posts)}")
        logger.debug(
            f"Processing toxicity score for Post Details: {toxicity.to_dict()}"
        )
        try:
            # scores = score_and_upsert(post)
            logger.debug(f"Recieved Comment {toxicity.get_comment()}")

            toxicity.set_comment(trim_to_20kb(clean_html(toxicity.get_comment())))

            scores = score_text(toxicity.get_comment())
            if scores is None:
                logger.warning(
                    "Post not found or empty text for %s/%s",
                    toxicity.get_board_name(),
                    toxicity.get_post_number(),
                )
                continue

            logger.debug(
                "Scored %s/%s: tox=%.3f sev=%.3f id=%.3f ins=%.3f thr=%.3f",
                toxicity.board_name,
                toxicity.post_no,
                (scores.get("toxicity") or 0.0),
                (scores.get("severe_toxicity") or 0.0),
                (scores.get("identity_attack") or 0.0),
                (scores.get("insult") or 0.0),
                (scores.get("threat") or 0.0),
            )
            toxicity.set_scores(**scores)
            scored_toxicity_objects.append(toxicity)
            if len(scored_toxicity_objects) == 100:
                store_toxicity_into_db(scored_toxicity_objects)
                scored_toxicity_objects = []

        except Exception as e:
            logger.error(
                "Error scoring %s/%s: %s", toxicity.board_name, toxicity.post_no, e
            )

    if scored_toxicity_objects:
        store_toxicity_into_db(scored_toxicity_objects)
        logger.info(f"✅ Completed Calculating & Inserting Toxicity Scores for {len(posts)} posts to DB")
    else:
        logger.warning("No toxicity scores to insert into database")
