import time
from typing import List, Optional
from reddit_client import RedditClient
from constants.constants import REDDIT_CRAWLER, COMMENT_FIELDS, COMMENT_DETAILS_FIELDS
from modal.comment import Comment, CommentDetails
from utils.logger import Logger
from utils.plsql import PLSQL
from utils.faktory import initialize_producer
from constants.plsql_constants import (
    BULK_INSERT_COMMENTS,  # bulk insert SQL for comments
    SELECT_UNIQUE_ID_COMMENTS,  # returns rows of existing unique comment IDs
)
import datetime

logger = Logger(REDDIT_CRAWLER).get_logger()
reddit_client = RedditClient()


def fetch_subreddit_comments(subreddit_name: str, after: Optional[str] = None):
    """
    Fetches a page of recent comments for a given subreddit.
    Returns a list of Comment objects and the 'after' cursor for pagination.
    """

    params = {"limit": 100}
    if after:
        params["after"] = after

    # Make API request to fetch comments for the subreddit
    response = reddit_client.make_request(
        f"r/{subreddit_name}/comments/", params=params
    )

    comments: List[Comment] = []

    if response:
        try:
            data = response.get("data", {})
            after = data.get("after", None)
            children = data.get("children", [])  # list of t1 (comment) objects

            logger.debug(f"[{subreddit_name}] Next Page: {after}")

            for child in children:
                data = child["data"]

                comment_detailed_data_dict = {
                    field: data.get(field, "") for field in COMMENT_DETAILS_FIELDS
                }

                comment_data_dict = {
                    field: data.get(field, "") for field in COMMENT_FIELDS
                }

                detailedComment = CommentDetails(**comment_detailed_data_dict)
                comment_data_dict["comment_details"] = detailedComment
                # Create subreddit object using the dictionary
                comment = Comment(**comment_data_dict)
                # logger.debug(f"Post Data: {post.to_string()}")
                # logger.debug(f"Detailed Post Data: {detailedPost.to_string()}")
                comments.append(comment)

            logger.debug(f"Total Records fetched: {len(comments)}")
            return comments, after

        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"Error parsing comment data: {e}")

    return [], None


def store_comments_in_db(comments: List[Comment]) -> None:
    """
    Inserts new comments into DB via bulk insert.
    Deduplicates against existing unique IDs (e.g., comment 'id' or fullname 't1_xxx').
    """
    if not comments:
        logger.info("No comments to store")
        return

    plsql = PLSQL()

    # Expect this query to return one column with the unique comment identifier (e.g., 'id' or 'name')
    existing_ids_rows = plsql.get_data_from(SELECT_UNIQUE_ID_COMMENTS)
    existing_ids = {row[0] for row in existing_ids_rows}

    new_comment_rows = [
        c.to_tuple()
        for c in comments
        if c.get_comment_id()
        not in existing_ids  # method should mirror your Subreddit model
    ]

    if not new_comment_rows:
        logger.info("No New Comments Found")
    else:
        plsql.insert_bulk_data_into_db(BULK_INSERT_COMMENTS, new_comment_rows)
        logger.info(f"Inserted {len(new_comment_rows)} new comments")

    plsql.close_connection()


def crawl_comments_for_subreddit(subreddit_name: str) -> None:
    """
    Paginates through recent comments for each post_id,
    making requests and storing comments until no more pages are available.
    """

    logger.info(f"Collecting comments for {subreddit_name} posts")
    logger.info(f"Starting SubReddit: {subreddit_name} Posts fetch cycle")
    after = None
    finished = False

    while not finished:
        logger.info("Starting new 1-minute cycle with 4 requests")
        for i in range(2):
            logger.info(f"Fetching batch {i + 1}/2")
            comments, after = fetch_subreddit_comments(subreddit_name, after)
            if comments:
                store_comments_in_db(comments)
                logger.info(f"Stored batch {i + 1} with {len(comments)} posts")
            else:
                logger.warning(f"No data fetched on batch {i + 1}")

            if not after:
                logger.info("No more pages available, finished fetching all data")
                finished = True
                break
            if i < 2:  # Sleep only between requests, not after last one
                logger.info("Sleeping for 30 seconds before next request")
                time.sleep(30)

    logger.info("Scheduling Job for collecting comments")
    initialize_producer(
        queue=f"enqueue-crawl-comments-{subreddit_name}",
        jobtype=f"enqueue_crawl_comments_{subreddit_name}",
        delayedTimer=datetime.timedelta(minutes=5),
        args=[subreddit_name.lower()],
    )
    logger.info(f"Completed Scheduling Job for collecting {subreddit_name}")


# crawl_comments_for_subreddit("technology", [])
