import os
import time
from typing import Dict, Optional
from urllib.parse import urljoin

import requests
from constants.constants import REDDIT_CRAWLER
from constants.errors_constants import ERROR429
from requests import Response
from utils.logger import Logger

logger = Logger(REDDIT_CRAWLER).get_logger()


class RedditClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = float(os.getenv("REDDIT_TIMEOUT", "10"))
        self.max_retries = int(os.getenv("REDDIT_MAX_RETRIES", "3"))
        self.backoff_factor = float(os.getenv("REDDIT_BACKOFF_FACTOR", "1.5"))
        self.default_delay = 1
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        user_agent = os.getenv(
            "REDDIT_USER_AGENT",
            "data-collection-system-socialmediaavengers/0.1 (contact: karthik@binghamton.edu)",
        )
        return {"User-Agent": user_agent}

    def _respect_rate_limit(self, response: Optional[Response], attempt: int) -> None:
        wait_time = self.backoff_factor**attempt
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    wait_time = max(wait_time, float(retry_after))
                except ValueError:
                    logger.debug("Invalid Retry-After header '%s'", retry_after)
        wait_time = max(wait_time, self.default_delay)
        logger.warning("Rate limit encountered; sleeping for %.2f seconds", wait_time)
        time.sleep(wait_time)

    def make_request(self, endpoint: str, params: dict[str, str] = None):
        url = urljoin(self.base_url, endpoint)
        params = params or {}

        from requests.models import PreparedRequest

        req = PreparedRequest()
        req.prepare_url(url, params)
        logger.debug(f"Final prepared request URL: {req.url}")

        logger.info("Making request to: %s", url)
        logger.debug("Params: %s", params)

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(
                    url,
                    params=params or None,
                    headers=self.headers,
                    timeout=self.timeout,
                )

                if response.status_code == 429:
                    logger.error("Received 429 Too Many Requests for %s", url)
                    if attempt == self.max_retries:
                        break
                    self._respect_rate_limit(response, attempt)
                    continue

                response.raise_for_status()
                json_data = response.json()
                logger.info("Successfully fetched data from %s", endpoint)
                return json_data

            except requests.exceptions.RequestException as exc:
                logger.error(
                    "Request failed for %s on attempt %d/%d: %s",
                    url,
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt == self.max_retries:
                    break
                self._respect_rate_limit(None, attempt)

            except ValueError as exc:
                logger.error("Failed to parse JSON from %s: %s", url, exc)
                return None

        logger.error("Exceeded maximum retries for %s", url)
        return None

    def make_post_request(self, endpoint, payload, timeout):
        url = urljoin(self.base_url, endpoint)
        logger.info(f"Fetching data from {url}")
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            if response.status_code == 404:
                logger.warning(f"Resource not found: {url} (404)")
                return None
            response.raise_for_status()
            # Parse JSON response
            json_data = response.json()
            logger.info(f"Successfully fetched data from {url}")
            logger.debug(f"Response data: {json_data}")
            return json_data
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Raising warning for to many requests  {url}: {e}")
            return ERROR429
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

        except ValueError as e:
            logger.error(f"Failed to parse JSON from {url}: {e}")
            return None
