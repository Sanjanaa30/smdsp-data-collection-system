from chan_client import ChanClient
import logging
from typing import List, Dict, Any

class BoardCrawler:
    """
    Crawler for discovering and listing all 4chan boards.
    Uses ChanClient to make API requests to /boards.json endpoint.
    """
    
    def __init__(self):
        """Initialize the board crawler with a ChanClient instance."""
        self.client = ChanClient()
        self.logger = logging.getLogger(__name__)
    
    def get_all_boards(self) -> List[Dict[str, Any]]:
        """
        Fetch all boards from 4chan API.
        
        Returns:
            List of board dictionaries, empty list if failed
        """
        self.logger.info("Fetching all boards from 4chan API...")
        
        # Call the API through our client
        boards_data = self.client.get_boards()
        
        if boards_data is None:
            self.logger.error("Failed to fetch boards data")
            return []
        
        # Extract the boards array from the response
        boards = boards_data.get('boards', [])
        self.logger.info(f"Successfully fetched {len(boards)} boards")
        
        return boards
    
    def print_all_boards(self) -> None:
        """
        Fetch and print all boards to console in a formatted way.
        """
        boards = self.get_all_boards()
        
        if not boards:
            print("No boards found or API call failed!")
            return
        
        print("\n" + "="*60)
        print(f"4CHAN BOARDS LIST ({len(boards)} total boards)")
        print("="*60)
        
        for board in boards:
            board_code = board.get('board', 'N/A')
            board_title = board.get('title', 'No Title')
            work_safe = "SFW" if board.get('ws_board', 0) == 1 else "NSFW"
            pages = board.get('pages', 'N/A')
            
            print(f"/{board_code}/ - {board_title} [{work_safe}] ({pages} pages)")
        
        print("="*60)

if __name__ == "__main__":
    """
    Entry point for the board crawler script.
    """
    print("Starting 4chan Board Crawler...")
    
    # Create crawler instance
    crawler = BoardCrawler()
    
    # Get and print all boards
    crawler.print_all_boards()
    
    print("Board crawler finished!")
