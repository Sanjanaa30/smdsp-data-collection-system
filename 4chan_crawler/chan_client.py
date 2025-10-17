import requests
from typing import Dict, Any, Optional
from constants.api_constants import FOURCHAN_BASE_URL
from constants.constants import CHAN_CRAWLER
from utils.logger import Logger
from urllib.parse import urljoin


logger = Logger(CHAN_CRAWLER).get_logger()

class ChanClient:
    
    def __init__(self):
        self.base_url = FOURCHAN_BASE_URL
    
    def make_request(self, endpoint: str) -> Optional[Dict[Any, Any]]:
        url = urljoin(self.base_url, endpoint)
        logger.info(f"Fetching data from {url}")
        try:
            # # Check if request was successful
            # response.raise_for_status()
            response = requests.get(url)
            response.raise_for_status()

            # Parse JSON response
            json_data = response.json()
            logger.info(f"Successfully fetched data from {endpoint}")
            logger.debug(f"Response data: {json_data}")
            return json_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Failed to parse JSON from {url}: {e}")
            return None
    
    def get_boards(self) -> Optional[Dict[Any, Any]]:

        return self.make_request("/boards.json")
    
    def get_catalog(self, board: str) -> Optional[Dict[Any, Any]]:

        return self.make_request(f"/{board}/catalog.json")
    
    def get_thread(self, board: str, thread_id: int) -> Optional[Dict[Any, Any]]:

        return self.make_request(f"/{board}/thread/{thread_id}.json")
