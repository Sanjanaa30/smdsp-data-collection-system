import requests
from typing import Dict, Any, Optional
from constants.api_constants import CATALOG_JSON, FOURCHAN_BASE_URL, THREADS, DOT_JSON
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
            # Check if request was successful
            response = requests.get(url)
            if response.status_code == 404:
                logger.warning(f"Resource not found: {url} (404)")
                return None
            response.raise_for_status()

            # Parse JSON response
            json_data = response.json()
            logger.info(f"Successfully fetched data from {endpoint}")
            logger.debug(f"Response data: {json_data}")
            return json_data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

        except ValueError as e:
            logger.error(f"Failed to parse JSON from {url}: {e}")
            return None

    def get_boards(self) -> Optional[Dict[Any, Any]]:
        """Fetch all 4chan boards."""
        return self.make_request("/boards.json")

    def get_threads(self, board: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch all threads from a specific board using threads.json
        """
        return self.make_request(f"/{board}/{THREADS}{DOT_JSON}")

    def get_catalog(self, board: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch catalog (thread overview) from a specific board using catalog.json
        """
        # For testing purposes, using mock data # return self.make_request(f"/{board}/catalog.json")
        # response = "[{\"page\":1,\"threads\":[{\"no\":503281217,\"last_modified\":1745613336,\"replies\":1},{\"no\":519496220,\"last_modified\":1761097906,\"replies\":3},{\"no\":519492417,\"last_modified\":1761097904,\"replies\":203},{\"no\":519486692,\"last_modified\":1761097903,\"replies\":22},{\"no\":519490182,\"last_modified\":1761097902,\"replies\":37},{\"no\":519485421,\"last_modified\":1761097902,\"replies\":260},{\"no\":519494250,\"last_modified\":1761097900,\"replies\":10}]}]"
        # response = json.loads(response)
        # return response
        return self.make_request(f"/{board}/{CATALOG_JSON}")

    def get_thread_posts(self, board: str, thread_id: int) -> Optional[Dict[Any, Any]]:
        """
        Fetch all posts from a specific thread using thread/{id}.json
        """
        return self.make_request(f"/{board}/thread/{thread_id}.json")
