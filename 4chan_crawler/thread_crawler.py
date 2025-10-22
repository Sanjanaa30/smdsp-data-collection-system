import datetime
from dotenv import load_dotenv
from constants.plsql_constants import (
    INSERT_BULK_THREAD_DATA_QUERY, 
    SELECT_THREAD_IDS_QUERY
)
from utils.plsql import PLSQL
from chan_client import ChanClient
from typing import List, Dict, Any
from utils.logger import Logger
from utils.faktory import init_faktory_client
from constants.constants import CHAN_CRAWLER
from constants.api_constants import THREADS_JSON


load_dotenv()

logger = Logger(CHAN_CRAWLER).get_logger()


class ThreadCrawler:
    """
    Crawler for collecting all threads from a specific 4chan board.
    Uses ChanClient to make API requests to /{board}/threads.json endpoint.
    """
    
    def __init__(self):
        """Initialize the thread crawler with a ChanClient instance."""
        self.client = ChanClient()
    
    def get_threads_from_board(self, board: str) -> List[Dict[str, Any]]:
        """
        Fetch all threads from a specific board.
        """
        logger.info(f"Fetching threads from {board} board...")
        
        # Make API call to get threads (use THREADS_JSON as-is)
        threads_data = self.client.get_threads(board)
        
        if threads_data is None:
            logger.error(f"No threads found from /{board}/ board")
            return []
        
        # Extract all threads from all pages
        all_threads = []
        
        # threads.json returns array of pages, each page has threads array
        for page in threads_data:
            page_number = page.get('page', 'Unknown')
            threads = page.get('threads', [])
            logger.info(f"Found {len(threads)} threads on page {page_number}")
            
            # Add page info to each thread for reference
            for thread in threads:
                thread['page'] = page_number
            
            all_threads.extend(threads)
        
        logger.info(f"Total threads found in /{board}/: {len(all_threads)}")
        return all_threads


def fetch_and_save_threads(board: str = "pol"):
    """
    Job handler function to fetch and save threads from a specific board.
    This function is intended to be called by the Faktory consumer.
    """
    crawler = ThreadCrawler()
    threads = crawler.get_threads_from_board(board)
    plsql = PLSQL()
    
    current_thread_ids_raw = plsql.get_data_from(SELECT_THREAD_IDS_QUERY, (board,))
    # Convert to set for fast lookup  
    current_thread_ids = {row[0] for row in current_thread_ids_raw} 
    logger.debug(f"Current thread IDs for /{board}/: {len(current_thread_ids)}")
    
    if not threads:
        logger.warning(f"No threads to save from /{board}/")
        return
    
    # Prepare data for bulk insert
    thread_records = []
    
    for thread in threads:
        thread_id = thread.get('no')
        if thread_id not in current_thread_ids:  # Only save new threads
            # Map 4chan API fields to database columns
            thread_title = thread.get('sub', None)           # Thread subject/title
            com = thread.get('com', None)                    # Comment text
            created_time = thread.get('time')                # Unix timestamp when created
            last_modified = thread.get('last_modified')      # Unix timestamp of last activity
            replies = thread.get('replies', 0)               # Number of replies
            semantic_url = thread.get('semantic_url', None)  # Readable URL
            images = thread.get('images', 0)                 # Number of images
            
            thread_records.append((
                thread_id,      # thread_id
                board,          # board_code
                thread_title,   # thread_title
                com,            # com
                created_time,   # created_time
                last_modified,  # last_modified
                replies,        # replies
                semantic_url,   # semantic_url
                images          # images (created_at will be auto-generated)
            ))
    
    if len(thread_records) == 0:
        logger.info(f"No new threads found for /{board}/")
    else:
        logger.info(f"New threads found for /{board}/: {len(thread_records)}")
        plsql.insert_bulk_data_into_db(INSERT_BULK_THREAD_DATA_QUERY, thread_records)
        logger.info(f"Inserted {len(thread_records)} threads into database from /{board}/")
    
    plsql.close_connection()
    
    # Schedule next job (runs every 5 minutes for fresh thread data)
    init_faktory_client(
        role="producer",
        jobtype="enqueue_crawl_threads",
        queue="enqueue-crawl-threads", 
        delayedTimer=datetime.timedelta(minutes=5),
    )


if __name__ == "__main__":
    logger.info("Starting 4chan Thread Crawler...")
    init_faktory_client(
        role="consumer",
        queue="enqueue-crawl-threads",
        jobtype="enqueue_crawl_threads",
        fn=fetch_and_save_threads,
    )