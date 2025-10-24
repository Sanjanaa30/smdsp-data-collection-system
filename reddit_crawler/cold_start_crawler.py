"""
cold_start_crawler.py

A utility for initializing and managing a "cold start" catalog crawl process.

Commands:
    --update-new-Subreddit      Update all newly discovered or unprocessed Subreddit.
    --collect-posts [names]       Collect posts for one or more specified Subreddit.
    --help                        Display information about available commands.
"""

import argparse
from utils.logger import Logger
from constants.constants import COLD_START_CRAWLER, LOG_FILE_NAME_COLD_START_CRAWLER
import datetime
from utils.faktory import initialize_producer

logger = Logger(COLD_START_CRAWLER, LOG_FILE_NAME_COLD_START_CRAWLER).get_logger()


class ColdStartCrawler:
    """
    A class responsible for handling cold start crawling operations.

    Attributes:
        update_new_subreddit (bool): Flag indicating whether to update new Subreddit.
        collect_posts (list[str] | None): List of subreddit names to collect posts for.
    """

    def __init__(
        self,
        update_new_subreddit: bool = False,
        collect_posts: list[str] | None = None,
    ):
        self.update_new_subreddit = update_new_subreddit
        self.collect_posts = collect_posts

    def update_subreddits(self):
        """Update all newly discovered Subreddit."""
        logger.info("🔄 Updating all new Subreddit...")
        initialize_producer(
            jobtype="enqueue_crawl_list_of_subreddit",
            queue="enqueue-crawl-list-of-subreddit",
            delayedTimer=datetime.timedelta(seconds=60),
        )
        logger.info("✅ Subreddit list update complete.")

    def collect_posts_for(self):
        """Collect posts for given Subreddit."""
        if not self.collect_posts:
            logger.info("⚠️ No Subreddit specified for post collection.")
            print("⚠️ No Subreddit specified for post collection.")
            return

        logger.info(
            f"⏳ Scheduling Job to Collect posts for Subreddit: {', '.join(self.collect_posts)}"
        )

        for subreddit_name in self.collect_posts:
            initialize_producer(
                jobtype=f"enqueue_crawl_{subreddit_name.lower()}",
                queue=f"enqueue-crawl-{subreddit_name.lower()}",
                delayedTimer=datetime.timedelta(seconds=60),
                args=[
                    subreddit_name.lower(),
                ],
            )

        logger.info(
            f"✅ Scheduling Job Completed to Collect posts for Subreddit: {', '.join(self.collect_posts)}"
        )

    def run(self):
        """Execute the appropriate action(s) based on initialized parameters."""
        if self.update_new_subreddit:
            self.update_subreddits()

        if self.collect_posts:
            self.collect_posts_for()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Cold Start Crawler: Tool for updating Subreddit and collecting posts.",
        add_help=True,
    )

    parser.add_argument(
        "--update-new-subreddit",
        action="store_true",
        help="Update all newly discovered or unprocessed Subreddit.",
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Collect posts for one or more specified Subreddit.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    crawler = ColdStartCrawler(
        update_new_subreddit=args.update_new_subreddit,
        collect_posts=args.collect_posts,
    )

    crawler.run()
