import datetime

# import logging
from typing import Any, Dict, List

from chan_client import ChanClient
from constants.plsql_constants import (
    INSERT_BULK_BOARD_DATA_QUERY,
    SELECT_BOARD_CODE_QUERY,
)
from constants.constants import (
    CHAN_CRAWLER,
)
from constants.api_constants import FOURCHAN_BASE_URL
from dotenv import load_dotenv
from utils.faktory import initialize_producer
from utils.logger import Logger
from utils.plsql import PLSQL

load_dotenv()

logger = Logger(CHAN_CRAWLER).get_logger()


class BoardCrawler:
    """
    Crawler for discovering and listing all 4chan boards.
    Uses ChanClient to make API requests to /boards.json endpoint.
    """

    def __init__(self):
        """Initialize the board crawler with a ChanClient instance."""
        self.client = ChanClient(FOURCHAN_BASE_URL)

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
    boards = crawler.get_all_boards()
    values = []
    plsql = PLSQL()
    current_boards_raw = plsql.get_data_from(SELECT_BOARD_CODE_QUERY)
    # logger.debug(f"current_boards_raw {current_boards_raw}")
    current_boards = {row[0] for row in current_boards_raw}
    logger.debug(f"Current Boards {current_boards}")
    for board in boards:
        board_code = board.get("board", "N/A")
        if board_code not in current_boards:
            board_title = board.get("title", "No Title")
            board_meta_description = board.get(
                "meta_description", "No Meta Description"
            )
            ws_board = board.get("ws_board", 0)
            values.append((board_code, board_title, board_meta_description, ws_board))
    if len(values) == 0:
        logger.info("No New Boards found")
    else:
        logger.info(f"Total New Boards found {len(values)}")
        plsql.insert_bulk_data_into_db(INSERT_BULK_BOARD_DATA_QUERY, values)
        plsql.close_connection()

    initialize_producer(
        queue="enqueue-crawl-list-of-boards",
        jobtype="enqueue_crawl_list_of_boards",
        delayedTimer=datetime.timedelta(days=30),
    )
