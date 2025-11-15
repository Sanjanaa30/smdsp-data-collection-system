import datetime
from typing import Any, Dict, List

from chan_client import ChanClient
from constants.api_constants import DOT_JSON, FOURCHAN_BASE_URL, THREAD, THREADS
from constants.constants import CHAN_CRAWLER, POSTS_FIELDS, TOX_JOBTYPE, TOX_QUEUE
from constants.plsql_constants import (
    CHECK_EXISTING_POSTS_QUERY,
    INSERT_BULK_POSTS_DATA_QUERY,
)
from modal.posts import Posts
from utils.faktory import initialize_producer
from utils.logger import Logger

logger = Logger(CHAN_CRAWLER).get_logger()


class ThreadCrawler:
    """
    Crawler for collecting all threads from a specific 4chan board.
    Uses ChanClient to make API requests to /{board}/threads.json endpoint.
    """

    def __init__(self):
        """Initialize the thread crawler with a ChanClient instance."""
        self.client = ChanClient(FOURCHAN_BASE_URL)

    def threads_json_to_thread_number(self, thread_list, old_threads):
        all_threads = set()

        # Convert old_threads list of dicts to a single dict for easy lookup
        old_threads_dict = {}
        for thread_dict in old_threads:
            old_threads_dict.update(thread_dict)

        for page in thread_list:
            # print(f"{page['page']}")
            for thread in page["threads"]:
                thread_no = thread["no"]
                last_modified = thread["last_modified"]

                # Check if thread exists in old_threads and if last_modified has changed
                if thread_no in old_threads_dict:
                    if old_threads_dict[thread_no] == last_modified:
                        # Thread hasn't changed, skip it
                        logger.debug(
                            f"Skipping thread {thread_no} - no changes since last crawl"
                        )
                        continue
                    else:
                        logger.debug(
                            f"Thread {thread_no} has been modified - adding to crawl queue"
                        )

                # Add thread to all_threads (either new or modified)
                threads = {thread_no: last_modified}
                all_threads.add(thread_no)
                old_threads_dict.update(threads)

        # Convert old_threads_dict back to list of individual dicts format
        old_threads_list = [{k: v} for k, v in old_threads_dict.items()]
        
        return list(all_threads), old_threads_list

    def get_threads_from_board(
        self, board: str, old_threads=[], score_toxicity: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Fetch all threads from a specific board.

        Args:
            board: Board name (e.g., 'pol', 'g', 'a')

        Returns:
            List of thread dictionaries, empty list if failed
        """
        logger.info(f"Fetching threads from {board} board...")

        # test
        # threads_data = '[{"page":1,"threads":[{"no":503281217,"last_modified":1745613336,"replies":1},{"no":519496220,"last_modified":1761097906,"replies":3},{"no":519492417,"last_modified":1761097904,"replies":203},{"no":519486692,"last_modified":1761097903,"replies":22},{"no":519490182,"last_modified":1761097902,"replies":37},{"no":519485421,"last_modified":1761097902,"replies":260},{"no":519494250,"last_modified":1761097900,"replies":10}]}]'
        # import json

        # threads_data = json.loads(threads_data)
        # Make API call to get threads
        threads_data = self.client.make_request(f"{board}/{THREADS}{DOT_JSON}")

        if threads_data is None:
            logger.error(f"No threads found from /{board}/ board")
            return []

        all_threads, old_threads = self.threads_json_to_thread_number(
            threads_data, old_threads
        )
        logger.debug(f"Old Threads {old_threads}")
        initialize_producer(
            queue=f"enqueue-crawl-thread-{board}",
            jobtype=f"enqueue_crawl_thread_{board}",
            delayedTimer=datetime.timedelta(seconds=15),
            args=[board, all_threads, score_toxicity],
        )

        initialize_producer(
            queue=f"enqueue-crawl-listing-{board}",
            jobtype=f"enqueue_crawl_listing_{board}",
            delayedTimer=datetime.timedelta(minutes=5),
            args=[board, old_threads, score_toxicity],
        )

    def fetch_thread_posts(self, board_name, thread_ids):
        """
        Fetch all posts from the given list of thread IDs for a specific board.
        """
        logger.info("Starting post retrieval from threads")
        all_posts = []

        # Define default values for different field types
        field_defaults = {
            "no": 0,
            "name": "",
            "sub": "",
            "com": "",
            "filename": "",
            "ext": "",
            "time": 0,
            "resto": 0,
            "country": "",
            "country_name": "",
            "replies": 0,
            "images": 0,
            "archived": 0,
            "bumplimit": 0,
            "archived_on": 0,
        }

        for thread_id in thread_ids:
            logger.debug(f"Fetching posts from thread {thread_id}")
            response = self.client.make_request(
                f"{board_name}/{THREAD}/{thread_id}{DOT_JSON}"
            )

            if not response:
                logger.warning(f"No response received for thread {thread_id}")
                continue

            try:
                for post_data in response.get("posts", []):
                    post_fields = {
                        field: post_data.get(field, field_defaults.get(field, ""))
                        for field in POSTS_FIELDS
                        if field != "board_name"
                    }
                    post_fields["board_name"] = board_name  # Add extra metadata

                    post_obj = Posts(**post_fields)
                    all_posts.append(post_obj)

            except (KeyError, TypeError, ValueError) as e:
                logger.error(f"Error parsing posts from thread {thread_id}: {e}")

        return all_posts

    def save_posts_to_database(self, board_name, posts: list):
        """
        Saves a list of Posts objects to the database using a bulk insert.
        Checks for existing post_no's in the database and only inserts new ones.
        """
        if not posts:
            logger.info("No new posts to insert into the database.")
            return

        from utils.plsql import PLSQL

        db_client = PLSQL()

        # Get all post numbers from the posts list
        post_nos = [post.get_post_number() for post in posts]

        logger.debug(
            f"Checking which of {len(post_nos)} posts do not exist in database for board '{board_name}'."
        )

        try:
            # Query returns only post numbers that DO NOT exist in the database
            non_existing_posts = db_client.get_data_from(
                CHECK_EXISTING_POSTS_QUERY, (post_nos, board_name)
            )

            # Extract the post_no values from the result (returns list of tuples)
            non_existing_post_nos = set(row[0] for row in non_existing_posts)

            logger.info(
                f"Found {len(non_existing_post_nos)} new posts that need to be inserted."
            )

            if not non_existing_post_nos:
                logger.info(
                    "All posts already exist in database. No new posts to insert."
                )
                return

            # Filter to only include posts that don't exist in the database
            new_posts = [
                post
                for post in posts
                if post.get_post_number() in non_existing_post_nos
            ]

            # Convert new posts to tuples for bulk insert
            post_records = [post.to_tuple() for post in new_posts]
            logger.info(
                f"Preparing to insert {len(post_records)} new posts into the database."
            )

            db_client.insert_bulk_data_into_db(
                INSERT_BULK_POSTS_DATA_QUERY, post_records
            )
            logger.info(
                f"Successfully inserted {len(post_records)} new posts into the database."
            )
            return new_posts
        except Exception as e:
            logger.error(f"Error inserting posts into the database: {e}")
        finally:
            db_client.close_connection()

    def collect_and_store_posts(
        self, board_name, thread_ids: list, score_toxicity: bool = False
    ):
        """
        Fetches posts for the given board and thread list, then stores them in the database.
        """
        if not thread_ids:
            logger.warning("No thread IDs provided. Skipping post collection.")
            return

        logger.info(
            f"Collecting posts for board '{board_name}' from {len(thread_ids)} threads."
        )

        posts = self.fetch_thread_posts(board_name, thread_ids)
        if posts:
            logger.info(f"Fetched {len(posts)} posts from {len(thread_ids)} threads.")
            new_posts = self.save_posts_to_database(board_name, posts)

            if score_toxicity:
                logger.info(f"Scoring toxicity for {board_name}")
                delay = datetime.timedelta(seconds=30)
                input_toxicity = [
                    post.get_attributes_for_toxicity()
                    for post in new_posts
                    if post.comment
                ]
                initialize_producer(
                    queue=f"{TOX_QUEUE}-{board_name.lower()}",
                    jobtype=f"{TOX_JOBTYPE}_{board_name.lower()}",
                    delayedTimer=delay,
                    args=[input_toxicity],
                )
                logger.debug(
                    f"Scheduled collect toxicuty job with a total payload: {len(input_toxicity)}"
                )
        else:
            logger.warning(f"No posts retrieved for board '{board_name}'.")

    def print_threads_from_board(self, board: str) -> None:
        """
        Fetch and print all threads from a board in a formatted way.

        Args:
            board: Board name (e.g., 'pol', 'g', 'a')
        """
        threads = self.get_threads_from_board(board)

        if not threads:
            print(f"No threads found in /{board}/ or API call failed!")
            return

        print("\n" + "=" * 80)
        print(f"THREADS FROM /{board.upper()}/ BOARD ({len(threads)} total threads)")
        print("=" * 80)

        for i, thread in enumerate(threads[:20], 1):  # Show first 20 threads
            thread_id = thread.get("no", "N/A")
            last_modified = thread.get("last_modified", "N/A")
            replies = thread.get("replies", 0)
            images = thread.get("images", 0)
            page = thread.get("page", "N/A")

            # Get thread subject/comment preview if available
            subject = thread.get("sub", "")
            comment = thread.get("com", "")

            # Clean up HTML tags and truncate
            if comment:
                import re

                comment = re.sub("<[^<]+?>", "", comment)  # Remove HTML tags
                comment = comment[:100] + "..." if len(comment) > 100 else comment

            print(f"{i:2d}. Thread #{thread_id} (Page {page})")
            if subject:
                print(f"    Subject: {subject}")
            if comment:
                print(f"    Preview: {comment}")
            print(
                f"    Replies: {replies}, Images: {images}, Last Modified: {last_modified}"
            )
            print()

        if len(threads) > 20:
            print(f"... and {len(threads) - 20} more threads")

        print("=" * 80)

    def get_active_threads(
        self, board: str, min_replies: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get only active threads (with minimum number of replies).

        Args:
            board: Board name (e.g., 'pol', 'g', 'a')
            min_replies: Minimum number of replies to consider thread active

        Returns:
            List of active thread dictionaries
        """
        all_threads = self.get_threads_from_board(board)

        active_threads = [
            thread for thread in all_threads if thread.get("replies", 0) >= min_replies
        ]

        logger.info(
            f"Found {len(active_threads)} active threads (>={min_replies} replies) in /{board}/"
        )
        return active_threads
