from reddit_client import RedditClient
from constants.api_constants import SUBREDDIT_URL
from constants.constants import REDDIT_CRAWLER
from modal.communities import Communities
from utils.logger import Logger

logger = Logger(REDDIT_CRAWLER).get_logger()
redditClient = RedditClient()


def get_communities():
    logger.info("Getting reddit subreddit communities")
    response = redditClient.make_request(SUBREDDIT_URL)
    if response:
        next_page = response["data"].get("after", [])
        childrens = response["data"].get("children", [])
        logger.debug(f"children :{childrens}")
        logger.debug(f"Next Page :{next_page}")
        for children in childrens:
            data = children.get("data")
            data.get
            Communities(children)

get_communities()
