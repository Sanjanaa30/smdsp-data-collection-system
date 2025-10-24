#!/usr/bin/env python3
"""
crawler.py

A command-line tool for starting Faktory consumers that handle cold-start crawling tasks.

Commands:
    --update-new-subreddit      Start a consumer to enqueue jobs for updating new Subreddit.
    --collect-posts [names]       Start a consumer to enqueue jobs for collecting posts for given Subreddit.
    --help                        Display available commands and usage.
"""

import argparse
import os
from constants.constants import REDDIT_CRAWLER
from utils.faktory import initialize_consumer
from utils.logger import Logger
from subreddit_crawler import get_list_of_subreddit
from posts_crawler import get_posts

logger = Logger(REDDIT_CRAWLER).get_logger()


class CrawlerConsumer:
    """
    Creates Faktory consumers for specified cold start crawler operations.
    """

    def __init__(
        self,
        update_new_subreddit: bool = False,
        collect_posts: list[str] | None = None,
    ):
        self.update_new_subreddit = update_new_subreddit
        self.collect_posts = collect_posts

    def start_update_consumer(self):
        """Start Faktory consumer for updating Subreddit."""
        logger.info("🚀 Starting Faktory consumer for updating Subreddit...")
        initialize_consumer(
            queue=["enqueue-crawl-list-of-subreddit"],
            jobtypes=["enqueue_crawl_list_of_subreddit"],
            fn=get_list_of_subreddit,
        )

    def start_collect_consumer(self):
        """Start Faktory consumer for collecting posts."""
        logger.info(
            f"🚀 Starting Faktory consumer for collecting posts: {self.collect_posts}"
        )
        # logger.info(self.collect_posts)
        queue = [
            f"enqueue-crawl-{subreddit_name.lower()}"
            for subreddit_name in self.collect_posts
        ]
        jobtype = [
            f"enqueue_crawl_{subreddit_name.lower()}"
            for subreddit_name in self.collect_posts
        ]

        # logger.info(queue, jobtype)
        concurrency = os.getenv("FAKTORY_CONCURRENCY", 2)
        initialize_consumer(
            queue=queue, jobtypes=jobtype, fn=get_posts, concurrency=int(concurrency)
        )

    def run(self):
        """Run the appropriate Faktory consumer based on CLI arguments."""
        if self.update_new_subreddit:
            self.start_update_consumer()

        if self.collect_posts:
            self.start_collect_consumer()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Start Faktory consumers for crawling subreddit or collecting posts."
    )

    parser.add_argument(
        "--update-new-subreddit",
        action="store_true",
        help="Start a consumer to enqueue crawl jobs for new subreddit.",
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Start a consumer to enqueue crawl jobs for specified subreddit (space-separated).",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    consumer = CrawlerConsumer(
        update_new_subreddit=args.update_new_subreddit,
        collect_posts=args.collect_posts,
    )

    consumer.run()
