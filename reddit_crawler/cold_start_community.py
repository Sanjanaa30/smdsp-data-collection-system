
from dotenv import load_dotenv
from reddit_crawler.utils.faktory import init_faktory_client
import datetime
from utils.logger import Logger 
from constants.constants import REDDIT_CRAWLER
load_dotenv()

logger = Logger(REDDIT_CRAWLER).get_logger()
if __name__ == "__main__":
    logger.info("Cold starting for board")
    # Default url for a Faktory server running locally
    init_faktory_client(
        role="producer",
        jobtype="enqueue_crawl_community",
        queue="enqueue-crawl-community",
        delayedTimer=datetime.timedelta(minutes=5),
    )