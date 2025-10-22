import datetime
from dotenv import load_dotenv
from constants.constants import CHAN_CRAWLER
from utils.faktory import init_faktory_client
from utils.logger import Logger

load_dotenv()

logger = Logger(CHAN_CRAWLER).get_logger()

if __name__ == "__main__":
    logger.info("Cold starting for threads")
    # Default url for a Faktory server running locally
    init_faktory_client(
        role="producer",
        jobtype="enqueue_crawl_threads",
        queue="enqueue-crawl-threads",
        delayedTimer=datetime.timedelta(seconds=60),
    )
