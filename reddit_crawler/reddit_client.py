from constants import REDDIT_BASE_URL
import requests
from logger_factory import LoggerFactory
from constants import REDDIT_CRAWLER


class RedditClient:
    def __init__(self):
        self.base_url = REDDIT_BASE_URL
        self.logger = LoggerFactory(REDDIT_CRAWLER).get_logger()
        self.logger.info(f"Initialized RedditClient with base URL: {self.base_url}")

    def make_request(self, endpoint: str, limit: int = None):
        url = f"{self.base_url}{endpoint}"
        if limit is not None:
            separator = '?'
            url += f"{separator}limit={limit}"

        self.logger.info(f"Making request to: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            self.logger.info(f"Successfully fetched data from {endpoint}")
            return json_data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None

        except ValueError as e:
            self.logger.error(f"Failed to parse JSON from {url}: {e}")
            return None
