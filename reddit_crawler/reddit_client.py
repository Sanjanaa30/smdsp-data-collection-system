from constants.api_constants import REDDIT_BASE_URL
import requests
from utils.logger import Logger
from constants.constants import REDDIT_CRAWLER

logger = Logger(REDDIT_CRAWLER).get_logger()
class RedditClient:
    def __init__(self):
        self.base_url = REDDIT_BASE_URL

    def make_request(self, endpoint: str, limit: int = None):
        url = f"{self.base_url}{endpoint}"
        if limit is not None:
            separator = '?'
            url += f"{separator}limit={limit}"

        logger.info(f"Making request to: {url}")

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
