#!/usr/bin/env python3
"""
crawler.py

A command-line tool for starting Faktory consumers that handle cold-start crawling tasks.

Commands:
    --update-new-boards      Start a consumer to enqueue jobs for updating new Boards.
    --collect-posts [names]       Start a consumer to enqueue jobs for collecting posts for given Boards.
    --help                        Display available commands and usage.
"""

import argparse
import os
from constants.constants import CHAN_CRAWLER
from utils.faktory import initialize_consumer
from utils.logger import Logger
from board_crawler import fetch_and_save_boards
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
    ):
        self.update_new_boards = update_new_boards
        self.collect_posts = collect_posts

    def start_update_consumer(self):
        """Start Faktory consumer for updating Boards."""
        logger.info("🚀 Starting Faktory consumer for updating Boards...")
        initialize_consumer(
            queue=["enqueue-crawl-list-of-boards"],
            jobtypes=["enqueue_crawl_list_of_boards"],
            fn=fetch_and_save_boards,
        )

    def start_collect_consumer(self):
        """Start Faktory consumer for collecting posts."""
        logger.info(
            f"🚀 Starting Faktory consumer for collecting posts: {self.collect_posts}"
        )
        logger.info(self.collect_posts)
        queue = [
            f"enqueue-crawl-{boards_name.lower()}"
            for boards_name in self.collect_posts
        ]
        jobtype = [
            f"enqueue_crawl_{boards_name.lower()}"
            for boards_name in self.collect_posts
        ]

        logger.info(queue, jobtype)
        concurrency = os.getenv("FAKTORY_CONCURRENCY", 2)
        # initialize_consumer(
        #     queue=queue, jobtypes=jobtype, fn=get_posts, concurrency=int(concurrency)
        # )

    def run(self):
        """Run the appropriate Faktory consumer based on CLI arguments."""
        if self.update_new_boards:
            self.start_update_consumer()

        if self.collect_posts:
            self.start_collect_consumer()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Start Faktory consumers for crawling boards or collecting posts."
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

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    consumer = CrawlerConsumer(
        update_new_boards=args.update_new_boards,
        collect_posts=args.collect_posts,
    )

    consumer.run()