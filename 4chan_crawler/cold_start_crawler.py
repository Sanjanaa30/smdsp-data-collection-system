"""
cold_start_crawler.py

A utility for initializing and managing a "cold start" catalog crawl process.

Commands:
    --update-new-boards      Update all newly discovered or unprocessed boards.
    --collect-posts [names]       Collect posts for one or more specified boards.
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
        update_new_boards (bool): Flag indicating whether to update new boards.
        collect_posts (list[str] | None): List of boards names to collect posts for.
    """

    def __init__(
        self,
        update_new_boards: bool = False,
        collect_posts: list[str] | None = None,
    ):
        self.update_new_boards = update_new_boards
        self.collect_posts = collect_posts

    def update_boards(self):
        """Update all newly discovered boards."""
        logger.info("🔄 Updating all new boards...")
        initialize_producer(
            jobtype="enqueue_crawl_list_of_boards",
            queue="enqueue-crawl-list-of-boards",
            delayedTimer=datetime.timedelta(seconds=60),
        )
        logger.info("✅ Boards list update complete.")

    def collect_posts_for(self):
        """Collect posts for given Boards."""
        if not self.collect_posts:
            logger.info("⚠️ No Boards specified for post collection.")
            print("⚠️ No Boards specified for post collection.")
            return

        logger.info(
            f"⏳ Scheduling Job to Collect posts for Boards: {', '.join(self.collect_posts)}"
        )

        for board_name in self.collect_posts:
            initialize_producer(
                queue=f"enqueue-crawl-listing-{board_name.lower()}",
                jobtype=f"enqueue_crawl_listing_{board_name.lower()}",
                delayedTimer=datetime.timedelta(seconds=60),
                args=[
                    board_name.lower(),
                ],
            )

        logger.info(
            f"✅ Scheduling Job Completed to Collect posts for Boards: {', '.join(self.collect_posts)}"
        )

    def run(self):
        """Execute the appropriate action(s) based on initialized parameters."""
        if self.update_new_boards:
            self.update_boards()

        if self.collect_posts:
            self.collect_posts_for()


def parse_arguments():
    """Parse command-line arguments and return parsed values."""
    parser = argparse.ArgumentParser(
        description="Cold Start Crawler: Tool for updating Boards and collecting posts.",
        add_help=True,
    )

    parser.add_argument(
        "--update-new-boards",
        action="store_true",
        help="Update all newly discovered or unprocessed Boards.",
    )

    parser.add_argument(
        "--collect-posts",
        nargs="+",
        help="Collect posts for one or more specified Boards.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    crawler = ColdStartCrawler(
        update_new_boards=args.update_new_boards,
        collect_posts=args.collect_posts,
    )

    crawler.run()