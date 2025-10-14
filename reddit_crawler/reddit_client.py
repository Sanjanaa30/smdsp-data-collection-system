from constants import REDDIT_BASE_URL
from logger import logger
import requests

class RedditClient:
    def __init__(self):
        self.base_url = REDDIT_BASE_URL
        logger.info(f"Initialized RedditClient with base URL: {self.base_url}")

    def make_request(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making request to: {url}")
        print(url)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            logger.info(f"Successfully fetched data from {endpoint}")
            return json_data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        
        except ValueError as e:
            logger.error(f"Failed to parse JSON from {url}: {e}")
            return None
        