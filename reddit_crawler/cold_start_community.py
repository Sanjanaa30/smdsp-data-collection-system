
from dotenv import load_dotenv
from faktory import init_faktory_client
import datetime
from logger import logger 
load_dotenv()

if __name__ == "__main__":
    logger.info("Cold starting for board")
    # Default url for a Faktory server running locally
    init_faktory_client(
        role="producer",
        jobtype="enqueue_crawl_community",
        queue="enqueue-crawl-community",
        delayedTimer=datetime.timedelta(minutes=5),
    )