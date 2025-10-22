
from dotenv import load_dotenv
from utils.faktory import init_faktory_client
from utils.logger import Logger
import datetime
from constants.constants import CHAN_CRAWLER, FAKTORY_PRODUCER_ROLE
load_dotenv()


logger = Logger(CHAN_CRAWLER).get_logger()

if __name__ == "__main__":
    logger.info("Cold starting for board")
    # Default url for a Faktory server running locally
    datetime.timedelta(days=10)
    init_faktory_client(
        role=FAKTORY_PRODUCER_ROLE,
        jobtype="enqueue_crawl_boards",
        queue="enqueue-crawl-boards",
        delayedTimer=datetime.timedelta(seconds=60),
    )