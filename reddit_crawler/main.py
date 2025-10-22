from reddit_crawler.utils.faktory import init_faktory_client
from utils.logger import Logger 
from constants.constants import REDDIT_CRAWLER, FAKTORY_CONSUMER_ROLE
from communities_crawler import get_communities

logger = Logger(REDDIT_CRAWLER).get_logger()

def main():
    logger.info("Starting Reddit Crawler...")
    init_faktory_client(
        role=FAKTORY_CONSUMER_ROLE,
        jobtype="enqueue_crawl_community",
        queue="enqueue-crawl-community",
        fn=get_communities,
    )
    # init_community_crawler()


if __name__ == "__main__":
    main()
