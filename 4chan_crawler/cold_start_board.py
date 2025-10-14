
from dotenv import load_dotenv
from faktory import init_faktory_client
import datetime
from logger import logger 
load_dotenv()

if __name__ == "__main__":
    logger.info("Cold starting for board")
    # Default url for a Faktory server running locally
    datetime.timedelta(days=10)
    init_faktory_client(
        role="producer",
        jobtype="enqueue_crawl_boards",
        queue="enqueue-crawl-boards",
        delayedTimer=datetime.timedelta(seconds=60),
    )