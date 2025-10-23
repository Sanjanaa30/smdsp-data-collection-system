"""
cold_start_crawler.py

A utility for initializing and managing a "cold start" catalog crawl process.

Commands:
    --update-new-communities      Update all newly discovered or unprocessed communities.
    --collect-posts [names]       Collect posts for one or more specified communities.
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
        update_new_communities (bool): Flag indicating whether to update new communities.
        collect_posts (list[str] | None): List of community names to collect posts for.
    """

    def __init__(
        self,
        update_new_communities: bool = False,
        collect_posts: list[str] | None = None,
    ):
        self.update_new_communities = update_new_communities
        self.collect_posts = collect_posts

    def update_communities(self):
        """Update all newly discovered communities."""
        print("🔄 Updating all new communities...")
        # TODO: Implement logic for updating new communities
        print("✅ Community update complete.")

    def collect_posts_for(self):
        """Collect posts for given communities."""
        # if not self.collect_posts:
        #     print("⚠️ No communities specified for post collection.")
        #     return

        logger.info(
            f"⏳ Scheduling Job to Collect posts for communities: {', '.join(self.collect_posts)}"
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
            f"✅ Scheduling Job Completed to Collect posts for communities: {', '.join(self.collect_posts)}"
        )

    def run(self):
        """Execute the appropriate action(s) based on initialized parameters."""
        if self.update_new_communities:
            self.update_communities()

        if self.collect_posts:
            self.collect_posts_for()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Cold Start Crawler: Tool for updating communities and collecting posts.",
        add_help=True,
    )

    parser.add_argument(
        "--update-new-communities",
        action="store_true",
        help="Update all newly discovered or unprocessed communities.",
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Collect posts for one or more specified communities.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    crawler = ColdStartCrawler(
        update_new_communities=args.update_new_communities,
        collect_posts=args.collect_posts,
    )

    crawler.run()
