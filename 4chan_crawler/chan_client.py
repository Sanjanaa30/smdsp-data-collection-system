import requests
import time
import logging
from typing import Dict, Any, Optional
from constants import FOURCHAN_BASE_URL

class ChanClient:
    
    def __init__(self):
        self.base_url = FOURCHAN_BASE_URL
        # self.session = requests.Session()
        # Set user agent as recommended by 4chan API docs
        # self.session.headers.update({
        #     'User-Agent': 'DataCollectionBot/1.0'
        # })
        
        # Setup logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    
    def make_request(self, endpoint: str) -> Optional[Dict[Any, Any]]:
        url = f"{self.base_url}{endpoint}"
        
        try:
            self.logger.info(f"Making request to: {url}")
            # response = self.session.get(url, timeout=10)
            
            # # Check if request was successful
            # response.raise_for_status()
            response = requests.get(url)
            response.raise_for_status()

            # Parse JSON response
            json_data = response.json()
            self.logger.info(f"Successfully fetched data from {endpoint}")
            self.logger.debug(f"Response data: {json_data}")
            return json_data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None
            return None
        except ValueError as e:
            # self.logger.error(f"Failed to parse JSON from {url}: {e}")
            print(f"Failed to parse JSON from {url}: {e}")
            return None
    
    def get_boards(self) -> Optional[Dict[Any, Any]]:

        return self.make_request("/boards.json")
    
    def get_catalog(self, board: str) -> Optional[Dict[Any, Any]]:

        return self.make_request(f"/{board}/catalog.json")
    
    def get_thread(self, board: str, thread_id: int) -> Optional[Dict[Any, Any]]:

        return self.make_request(f"/{board}/thread/{thread_id}.json")
