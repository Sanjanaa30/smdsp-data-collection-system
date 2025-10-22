from dotenv import load_dotenv
from utils.faktory import init_faktory_client
import datetime
from utils.logger import Logger 
from constants.constants import REDDIT_CRAWLER, FAKTORY_PRODUCER_ROLE
load_dotenv()

logger = Logger(REDDIT_CRAWLER).get_logger()
if __name__ == "__main__":
    logger.info("Cold starting for Communities CRAWLER")
    # Default url for a Faktory server running locally
    init_faktory_client(
        role=FAKTORY_PRODUCER_ROLE,
        queue="enqueue-crawl-community",
        jobtype="enqueue_crawl_community",
        delayedTimer=datetime.timedelta(seconds=30),
    )
    logger.info("Completed cold starting for Communities CRAWLER")
