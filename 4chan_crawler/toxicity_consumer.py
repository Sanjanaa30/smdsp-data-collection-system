# toxicity_consumer.py
from utils.logger import Logger
from utils.perspective import score_text


logger = Logger("toxicity_consumer", "toxicity_consumer.log").get_logger()


def score_post_toxicity_handler(input_toxicity: list):
    """
    Handler registered with pyfaktory Consumer.
    Your producer sends args=[{'board_name': 'pol', 'post_no': 123}] by default.
    """
    logger.debug(f"Received job payload {len(input_toxicity)}")
    # board, post_no, lang = _extract_payload(args, kwargs)

    if len(input_toxicity) < 0:
        logger.warning("Invalid toxicity job payload")
        return

    for post in input_toxicity:
        logger.info(
            f"🆙 Scoring toxicity for post_no = {post.get_post_number()} board_name = {post.board_name}"
        )
        logger.debug(f"Processing toxicity score for Post Details: {post}")
        try:
            # scores = score_and_upsert(post)
            scores = score_text(post.get_comment())
            if scores is None:
                logger.warning(
                    "Post not found or empty text for %s/%s",
                    post.board_name,
                    post.post_no,
                )
                return

            logger.info(
                "Scored %s/%s: tox=%.3f sev=%.3f id=%.3f ins=%.3f thr=%.3f",
                post.board_name,
                post.post_no,
                (scores.get("toxicity") or 0.0),
                (scores.get("severe_toxicity") or 0.0),
                (scores.get("identity_attack") or 0.0),
                (scores.get("insult") or 0.0),
                (scores.get("threat") or 0.0),
            )
        except Exception as e:
            logger.error("Error scoring %s/%s: %s", post.board_name, post.post_no, e)
