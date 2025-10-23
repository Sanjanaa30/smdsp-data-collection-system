#!/usr/bin/env python3
"""
crawler.py

A command-line tool for starting Faktory consumers that handle cold-start crawling tasks.

Commands:
    --update-new-communities      Start a consumer to enqueue jobs for updating new communities.
    --collect-posts [names]       Start a consumer to enqueue jobs for collecting posts for given communities.
    --help                        Display available commands and usage.
"""

import argparse
import os

# Example imports — replace with actual project paths
from utils.faktory import initialize_consumer
from subreddit_crawler import get_posts


class CrawlerConsumer:
    """
    Creates Faktory consumers for specified cold start crawler operations.
    """

    def __init__(self, update_new_communities: bool = False, collect_posts: list[str] | None = None):
        self.update_new_communities = update_new_communities
        self.collect_posts = collect_posts

    def start_update_consumer(self):
        """Start Faktory consumer for updating communities."""
        print("🚀 Starting Faktory consumer for updating communities...")
        # init_faktory_client(
        #     role=FAKTORY_CONSUMER_ROLE,
        #     queue="update-new-communities",
        #     jobtype="update_new_communities",
        #     fn=get_posts,
        # )

    def start_collect_consumer(self):
        """Start Faktory consumer for collecting posts."""
        print(f"🚀 Starting Faktory consumer for collecting posts: {self.collect_posts}")
        print(self.collect_posts)
        queue = [
            f"enqueue-crawl-{subreddit_name.lower()}"
            for subreddit_name in self.collect_posts
        ]
        jobtype = [
            f"enqueue_crawl_{subreddit_name.lower()}"
            for subreddit_name in self.collect_posts
        ]

        print(queue, jobtype)
        concurrency = os.getenv("FAKTORY_CONCURRENCY", 2)
        initialize_consumer(
            queue=queue,
            jobtypes=jobtype,
            fn=get_posts,
            concurrency=int(concurrency)
        )

    def run(self):
        """Run the appropriate Faktory consumer based on CLI arguments."""
        if self.update_new_communities:
            self.start_update_consumer()

        if self.collect_posts:
            self.start_collect_consumer()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Start Faktory consumers for crawling communities or collecting posts."
    )

    parser.add_argument(
        "--update-new-communities",
        action="store_true",
        help="Start a consumer to enqueue crawl jobs for new communities."
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Start a consumer to enqueue crawl jobs for specified communities (space-separated)."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    consumer = CrawlerConsumer(
        update_new_communities=args.update_new_communities,
        collect_posts=args.collect_posts,
    )

    consumer.run()
