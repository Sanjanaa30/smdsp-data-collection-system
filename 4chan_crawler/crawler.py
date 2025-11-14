"""
crawler.py

A command-line tool for starting Faktory consumers that handle cold-start crawling tasks.

Commands:
    --update-new-boards         Start a consumer to enqueue jobs for updating new Boards.
    --collect-posts [names]     Start a consumer to enqueue jobs for scoring posts for given Boards.
    --score-toxicity            Enable toxicity scoring when scoring posts.
    --help                      Display available commands and usage.
"""

import argparse
import os

from board_crawler import fetch_and_save_boards
from constants.constants import (
    CHAN_CRAWLER,
    FAKTORY_CONCURRENCY,
    FAKTORY_CONSUMER_ROLE,
    FAKTORY_SERVER_URL,
    TOX_JOBTYPE,
    TOX_QUEUE,
)
from pyfaktory import Client, Consumer
from thread_crawler import ThreadCrawler
from toxicity_consumer import score_post_toxicity_handler
from utils.faktory import initialize_consumer
from utils.logger import Logger

# from posts_crawler import get_posts

logger = Logger(CHAN_CRAWLER).get_logger()


class CrawlerConsumer:
    """
    Creates Faktory consumers for specified cold start crawler operations.
    """

    def __init__(
        self,
        update_new_boards: bool = False,
        collect_posts: list[str] | None = None,
        score_toxicity: bool = False,
    ):
        self.update_new_boards = update_new_boards
        self.collect_posts = collect_posts
        self.score_toxicity = score_toxicity

    def start_update_consumer(self):
        """Start Faktory consumer for updating Boards."""
        logger.info("🚀 Starting Faktory consumer for updating Boards...")
        initialize_consumer(
            queue=["enqueue-crawl-list-of-boards"],
            jobtypes=["enqueue_crawl_list_of_boards"],
            fn=fetch_and_save_boards,
        )

    def start_collect_consumer(self):
        """Start Faktory consumer for scoring posts."""
        logger.info(
            f"🚀 Starting Faktory consumer for scoring posts: {self.collect_posts}"
        )
        queue_thread_listing = [
            f"enqueue-crawl-listing-{boards_name.lower()}"
            for boards_name in self.collect_posts
        ]
        jobtypes_thread_listing = [
            f"enqueue_crawl_listing_{boards_name.lower()}"
            for boards_name in self.collect_posts
        ]

        queue_thread_crawling = [
            f"enqueue-crawl-thread-{boards_name.lower()}"
            for boards_name in self.collect_posts
        ]

        jobtypes_thread_crawling = [
            f"enqueue_crawl_thread_{boards_name.lower()}"
            for boards_name in self.collect_posts
        ]
        faktory_server_url = os.getenv(FAKTORY_SERVER_URL)
        concurrency = int(os.getenv(FAKTORY_CONCURRENCY, 2))
        logger.info(f"Concurrency {concurrency}")
        thread_crawler = ThreadCrawler()
        try:
            with Client(
                faktory_url=faktory_server_url, role=FAKTORY_CONSUMER_ROLE
            ) as client:
                consumer = Consumer(
                    client=client,
                    queues=["default"] + queue_thread_listing + queue_thread_crawling,
                    concurrency=concurrency,
                )
                for jobtype in jobtypes_thread_listing:
                    consumer.register(jobtype, thread_crawler.get_threads_from_board)
                for jobtype in jobtypes_thread_crawling:
                    consumer.register(jobtype, thread_crawler.collect_and_store_posts)
                consumer.run()
        except Exception as e:
            logger.debug(f"Error connecting to Faktory server: {e}")

    def start_score_toxicity_consumer(self):
        """Start Faktory consumer for scoring toxicity."""
        logger.info(
            f"🚀 Starting Faktory consumer for scoring toxicity: {self.score_toxicity}"
        )
        toxicity_queue = [
            f"{TOX_QUEUE}-{boards_name.lower()}" for boards_name in self.collect_posts
        ]
        toxicity_job = [
            f"{TOX_JOBTYPE}_{boards_name.lower()}" for boards_name in self.collect_posts
        ]
        initialize_consumer(
            toxicity_queue, toxicity_job, score_post_toxicity_handler, 2
        )
        logger.info(
            f"🚀 Completed Starting Faktory consumer for scoring toxicity: {self.score_toxicity}"
        )

    def run(self):
        """Run the appropriate Faktory consumer based on CLI arguments."""
        # Validate that score_toxicity requires collect_posts
        if self.score_toxicity and not self.collect_posts:
            error_msg = "❌ Error: --score-toxicity can only be used with --collect-posts"
            logger.error(error_msg)
            print(error_msg)
            return

        if self.update_new_boards:
            self.start_update_consumer()

        if self.collect_posts:
            self.start_collect_consumer()

            if self.score_toxicity:
                self.start_score_toxicity_consumer()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Start Faktory consumers for crawling boards or scoring posts."
    )

    parser.add_argument(
        "--update-new-boards",
        action="store_true",
        help="Start a consumer to enqueue crawl jobs for new boards.",
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Start a consumer to enqueue crawl jobs for specified boards (space-separated).",
    )

    parser.add_argument(
        "--score-toxicity",
        action="store_true",
        help="Enable toxicity scoring for the boards specified in --collect-posts.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    consumer = CrawlerConsumer(
        update_new_boards=args.update_new_boards,
        collect_posts=args.collect_posts,
        score_toxicity=args.score_toxicity,
    )

    consumer.run()
