import datetime
import os

# import logging
from typing import Any, Dict, List

from chan_client import ChanClient
from constants import INSERT_BULK_BOARD_DATA_QUERY, SELECT_ALL_BOARDS_QUERY
from dotenv import load_dotenv
from faktory import init_faktory_client
from logger import logger
from plsql import PLSQL

load_dotenv()


class BoardCrawler:
    """
    Crawler for discovering and listing all 4chan boards.
    Uses ChanClient to make API requests to /boards.json endpoint.
    """

    def __init__(self):
        """Initialize the board crawler with a ChanClient instance."""
        self.client = ChanClient()

    def get_all_boards(self) -> List[Dict[str, Any]]:
        """
        Fetch all boards from 4chan API.

        Returns:
            List of board dictionaries, empty list if failed
        """
        logger.info("Fetching all boards from 4chan API...")

        # Call the API through our client
        boards_data = self.client.get_boards()

        if boards_data is None:
            logger.error("Failed to fetch boards data")
            return []

        # Extract the boards array from the response
        boards = boards_data.get("boards", [])
        logger.info(f"Successfully fetched {len(boards)} boards")

        return boards

    def print_all_boards(self) -> None:
        """
        Fetch and print all boards to console in a formatted way.
        """
        boards = self.get_all_boards()

        if not boards:
            print("No boards found or API call failed!")
            return

        print("\n" + "=" * 60)
        print(f"4CHAN BOARDS LIST ({len(boards)} total boards)")
        print("=" * 60)

        for board in boards:
            board_code = board.get("board", "N/A")
            board_title = board.get("title", "No Title")
            work_safe = "SFW" if board.get("ws_board", 0) == 1 else "NSFW"
            pages = board.get("pages", "N/A")

            print(f"/{board_code}/ - {board_title} [{work_safe}] ({pages} pages)")

        print("=" * 60)


def fetch_and_save_boards():
    """
    Job handler function to fetch and print all boards.
    This function is intended to be called by the Faktory consumer.
    """
    crawler = BoardCrawler()
    # if (os.getenv("LOG_LEVEL") == "DEBUG"):
    #     crawler.print_all_boards()
    # else:
    boards = crawler.get_all_boards()
    values = []
    for board in boards:
        board_code = board.get("board", "N/A")
        board_title = board.get("title", "No Title")
        values.append((board_code, board_title))

    plsql = PLSQL()

    current_boards = plsql.get_data_from(SELECT_ALL_BOARDS_QUERY)
    if (current_boards == values):
        logger.info("No new boards to insert.")
        plsql.close_connection()
    else:
        # insert_boards_into_db(crawler.get_all_boards())
        plsql.insert_bulk_data_into_db(INSERT_BULK_BOARD_DATA_QUERY, values)
        plsql.close_connection()

    init_faktory_client(
        role="producer",
        jobtype="enqueue_crawl_boards",
        queue="enqueue-crawl-boards",
        delayedTimer=datetime.timedelta(days=30),
    )


if __name__ == "__main__":
    """
    Entry point for the board crawler script.
    """
    logger.info("Starting 4chan Board Crawler...")
    init_faktory_client(
        role="consumer",
        queue="enqueue-crawl-boards",
        jobtype="enqueue_crawl_boards",
        fn=fetch_and_save_boards,
    )
