from chan_client import ChanClient
from typing import List, Dict, Any
from utils.logger import Logger
from constants.constants import CHAN_CRAWLER
from constants.api_constants import THREADS_JSON
from urllib.parse import urljoin

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
        
        Args:
            board: Board name (e.g., 'pol', 'g', 'a')
            
        Returns:
            List of thread dictionaries, empty list if failed
        """
        logger.info(f"Fetching threads from {board} board...")
        
        # Make API call to get threads
        threads_data = self.client.make_request(urljoin(board, THREADS_JSON))
        
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
        
        print("\n" + "="*80)
        print(f"THREADS FROM /{board.upper()}/ BOARD ({len(threads)} total threads)")
        print("="*80)
        
        for i, thread in enumerate(threads[:20], 1):  # Show first 20 threads
            thread_id = thread.get('no', 'N/A')
            last_modified = thread.get('last_modified', 'N/A')
            replies = thread.get('replies', 0)
            images = thread.get('images', 0)
            page = thread.get('page', 'N/A')
            
            # Get thread subject/comment preview if available
            subject = thread.get('sub', '')
            comment = thread.get('com', '')
            
            # Clean up HTML tags and truncate
            if comment:
                import re
                comment = re.sub('<[^<]+?>', '', comment)  # Remove HTML tags
                comment = comment[:100] + '...' if len(comment) > 100 else comment
            
            print(f"{i:2d}. Thread #{thread_id} (Page {page})")
            if subject:
                print(f"    Subject: {subject}")
            if comment:
                print(f"    Preview: {comment}")
            print(f"    Replies: {replies}, Images: {images}, Last Modified: {last_modified}")
            print()
        
        if len(threads) > 20:
            print(f"... and {len(threads) - 20} more threads")
        
        print("="*80)
    
    def get_active_threads(self, board: str, min_replies: int = 5) -> List[Dict[str, Any]]:
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
            thread for thread in all_threads 
            if thread.get('replies', 0) >= min_replies
        ]
        
        logger.info(f"Found {len(active_threads)} active threads (>={min_replies} replies) in /{board}/")
        return active_threads

if __name__ == "__main__":
    """
    Entry point - this runs when you execute: python thread_crawler.py
    """
    logger.info("Starting 4chan Thread Crawler...")
    
    # Create crawler instance
    crawler = ThreadCrawler()

    board_name = "a"
    logger.info(f"\nFetching threads from /{board_name}/ board...")

    crawler.get_threads_from_board(board_name)
    
    # Get and print all threads
    # crawler.print_threads_from_board(board_name)
    
    # # Also show active threads
    # print(f"\nActive threads (>=10 replies) in /{board_name}/:")
    # active = crawler.get_active_threads(board_name, min_replies=10)
    # print(f"Found {len(active)} active threads")
    
    logger.info("Thread crawler finished!")