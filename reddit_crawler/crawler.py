#!/usr/bin/env python3
"""
crawler.py

A command-line tool for starting Faktory consumers that handle cold-start crawling tasks.

Commands:
    --update-new-subreddit      Start a consumer to enqueue jobs for updating new Subreddit.
    --collect-posts [names]     Start a consumer to enqueue jobs for collecting posts for given Subreddit.
    --collect-comments [names]  Start a consumer to enqueue jobs for collecting comments for given Subreddit.
    --score-toxicity            Enable toxicity scoring when scoring posts.
    --help                      Display available commands and usage.
"""

import argparse
import os

from comments_crawler import crawl_comments_for_subreddit
from constants.constants import REDDIT_CRAWLER, TOX_JOBTYPE, TOX_QUEUE
from posts_crawler import get_posts
from subreddit_crawler import get_list_of_subreddit
from utils.faktory import initialize_consumer, initialize_two_consumer
from utils.logger import Logger
from toxicity_consumer import score_post_toxicity_handler

logger = Logger(REDDIT_CRAWLER).get_logger()


class CrawlerConsumer:
    """
    Creates Faktory consumers for specified cold start crawler operations.
    """

    def __init__(
        self,
        update_new_subreddit: bool = False,
        collect_posts: list[str] | None = None,
        collect_comments: list[str] | None = None,
        score_toxicity: bool = False,
    ):
        self.update_new_subreddit = update_new_subreddit
        self.collect_posts = collect_posts
        self.collect_comments = collect_comments
        self.score_toxicity = score_toxicity

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
        logger.info(f"Score Toxicity {self.score_toxicity}")
        if not self.score_toxicity:
            initialize_consumer(
                queue=queue,
                jobtypes=jobtype,
                fn=get_posts,
                concurrency=int(concurrency),
            )
        if self.score_toxicity:
            toxicity_queue = [
                f"{TOX_QUEUE}-{boards_name.lower()}"
                for boards_name in self.collect_posts
            ]
            toxicity_job = [
                f"{TOX_JOBTYPE}_{boards_name.lower()}"
                for boards_name in self.collect_posts
            ]

            initialize_two_consumer(
                queue1=queue,
                jobtype1=jobtype,
                queue2=toxicity_queue,
                jobtype2=toxicity_job,
                fn1=get_posts,
                fn2=score_post_toxicity_handler,
            )

    def start_collect_comments_consumer(self):
        """Start Faktory consumer for collecting comments."""
        logger.info(
            f"🚀 Starting Faktory consumer for collecting comments: {self.collect_comments}"
        )
        queue = [
            f"enqueue-crawl-comments-{subreddit_name.lower()}"
            for subreddit_name in self.collect_comments
        ]
        jobtype = [
            f"enqueue_crawl_comments_{subreddit_name.lower()}"
            for subreddit_name in self.collect_comments
        ]

        concurrency = os.getenv("FAKTORY_CONCURRENCY", 2)
        if not self.score_toxicity:
            initialize_consumer(
                queue=queue,
                jobtypes=jobtype,
                fn=crawl_comments_for_subreddit,
                concurrency=int(concurrency),
            )
        if self.score_toxicity:
            toxicity_queue = [
                f"{TOX_QUEUE}-comment-{boards_name.lower()}"
                for boards_name in self.collect_comments
            ]
            toxicity_job = [
                f"{TOX_JOBTYPE}_comment_{boards_name.lower()}"
                for boards_name in self.collect_comments
            ]

            initialize_two_consumer(
                queue1=queue,
                jobtype1=jobtype,
                queue2=toxicity_queue,
                jobtype2=toxicity_job,
                fn1=crawl_comments_for_subreddit,
                fn2=score_post_toxicity_handler,
            )

    def run(self):
        """Run the appropriate Faktory consumer based on CLI arguments."""
        if self.update_new_subreddit:
            self.start_update_consumer()

        if self.collect_posts:
            self.start_collect_consumer()

        if self.collect_comments:
            self.start_collect_comments_consumer()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Start Faktory consumers for crawling subreddit, collecting posts, or collecting comments."
    )

    parser.add_argument(
        "--update-new-subreddit",
        action="store_true",
        help="Start a consumer to enqueue crawl jobs for new subreddit.",
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Start a consumer to enqueue crawl jobs for specified subreddit posts (space-separated).",
    )

    parser.add_argument(
        "--collect-comments",
        nargs="+",
        help="Start a consumer to enqueue crawl jobs for specified subreddit comments (space-separated).",
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
        update_new_subreddit=args.update_new_subreddit,
        collect_posts=args.collect_posts,
        collect_comments=args.collect_comments,
        score_toxicity=args.score_toxicity,
    )

    consumer.run()
