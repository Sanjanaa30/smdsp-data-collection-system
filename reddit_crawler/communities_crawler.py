from reddit_client import RedditClient
from constants import SUBREDDIT_URL, REDDIT_CRAWLER
from logger_factory import LoggerFactory

logger = LoggerFactory(REDDIT_CRAWLER).get_logger()
redditClient = RedditClient()


def get_communities():
    logger.info("Getting reddit subreddit communities")
    response = redditClient.make_request(SUBREDDIT_URL)
    if response:
        next_page = response["data"].get("after", [])
        children = response["data"].get("children", [])
        logger.debug(f"Next Page :{next_page}")


get_communities()
