import asyncio
import time
import logging
import httpx
import random
import argparse
from pathlib import Path
from typing import Set


from web_crawler.network_client import NetworkClient
from web_crawler.storage_client import StorageClient
from web_crawler.html_parser import HTMLParser
from web_crawler.url_filter import URLFilter
from web_crawler.url_deduplicator import URLDeDuplicator
from web_crawler.robot_parser import RobotParser
from web_crawler.url_container import URLContainer
from web_crawler.exceptions import (
    RateLimitException,
    RedirectException,
    NotFoundException,
    InvalidBaseURL,
    GenericCrawlerException,
)


logger = logging.getLogger(__name__)


class WebCrawler:
    """
    A web crawler that asynchronously navigates through web pages, extracts links, and stores the results.

    This crawler implements features such as:
    - Asynchronous crawling with multiple workers
    - Respect for robots.txt rules
    - Rate limiting handling with exponential backoff
    - URL filtering and deduplication
    - Persistent storage of crawled data

    Attributes:
        start_url (str): The initial URL where crawling begins
        network_client (NetworkClient): Client for making HTTP requests
        storage_client (StorageClient): Client for storing crawled data
        url_filter (URLFilter): Filter for validating and processing URLs
        robot_parser (RobotParser): Parser for handling robots.txt rules
        to_visit_queue (asyncio.Queue): Queue of URLs to be crawled
        num_workers (int): Number of concurrent crawler workers
        max_retries (int): Maximum number of retry attempts for failed requests
        backoff (int): Base time in seconds for exponential backoff

        InvalidBaseURL: If the starting URL is invalid
    """

    def __init__(
        self,
        start_url: str,
        network_client: NetworkClient = NetworkClient(),
        storage_client: StorageClient = StorageClient(
            output_file_path=Path(__file__).parent.parent,
            output_file_name="storage.json",
        ),
        num_workers: int = 1,
        max_retries: int = 3,
        backoff: int = 5,
    ):
        self.start_url = start_url
        self.network_client = network_client
        self.url_filter = URLFilter(self.start_url)
        # Validate URL
        if not self.url_filter.is_url_valid():
            logger.error(f"Crawler not proceeding, invalid URL: {self.start_url}")
            raise InvalidBaseURL(f"Invalid URL: {self.start_url}")

        self.robot_parser = RobotParser(self.start_url)

        self.storage_client = storage_client

        self.to_visit_queue = asyncio.Queue()
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.backoff = backoff

        logger.info(
            f"Web Crawler configuration - url: {self.start_url}, workers: {self.num_workers}, retries: {self.max_retries}, backoff: {self.backoff}"
        )

    async def crawl_with_workers(self):
        """
        Asynchronously crawls web pages using a specified number of worker tasks.

        This method initializes the crawling process by adding the start URL to the
        queue and then creates a number of worker tasks to process the URLs in the queue.
        The method waits for the queue to be fully processed before canceling the worker
        tasks and saving the results to a file.
        """
        await self.to_visit_queue.put(URLContainer(self.start_url))

        logger.info(f"Init URL: {self.start_url} added to queue ")
        logger.debug(f"Queue size: {self.to_visit_queue.qsize()}")

        # Worker creation
        workers = [
            asyncio.create_task(self.workers(), name=f"worker_{i}")
            for i in range(self.num_workers)
        ]

        # Wait for the queue to be fully processed
        await self.to_visit_queue.join()

        # Cancels workers once the queue is empty
        for worker in workers:
            worker.cancel()

        # Save to file - Caveat, if the program is interrupted before this point, the data will not be saved
        self.storage_client.write_to_file()

    async def workers(self):
        """
        Asynchronous worker method that continuously processes crawling units.

        This method logs the start of a worker, then enters an infinite loop where it:
        - Abides by the robots.txt crawling policy by sleeping for the specified crawl delay with additional jitter.
        - Triggers the processing

        If the worker is cancelled, it logs the cancellation and exits the loop.

        Raises:
            asyncio.CancelledError: If the worker is cancelled.
        """
        logger.info(f"Worker started: {asyncio.current_task().get_name()}")
        while True:
            try:
                # Abide by robots crawling policy
                await asyncio.sleep(
                    self.robot_parser.crawl_delay + random.uniform(0, 1)
                )
                await self.process()
            except asyncio.CancelledError:
                logger.error(
                    f"Worker: {asyncio.current_task().get_name()} has been cancelled"
                )
                return

    async def process(self):
        """
        Process URLs from the queue and handle crawling logic.

        This method continuously processes URLs from the queue, handling various scenarios and exceptions:
        - Checks if URL has already been crawled
        - Validates against robots.txt rules
        - Handles rate limiting with exponential backoff
        - Manages redirects
        - Retries failed requests up to max_retries
        Returns:
            None
        Raises:
            RateLimitException: When rate limit is hit, triggers backoff
            RedirectException: When URL redirects to another location
            NotFoundException: When page is not found (404)
            Exception: For other errors, will retry up to max_retries
        Queue Management:
            Marks the task as done in the queue after processing.
        """

        # Fetch URL from queue
        url_to_visit_container = await self.to_visit_queue.get()
        url_to_visit = url_to_visit_container.base_url

        logger.info(f"Visiting {url_to_visit_container.base_url}")
        logger.debug(f"Queue size: {self.to_visit_queue.qsize()}")
        try:
            # Check if link has already been crawled
            if self.storage_client.contains(url_to_visit):
                logger.info(f"URL already visited: {url_to_visit} - skipping")
                return
            # Check if we can fetch the URL based on robots.txt
            if self.robot_parser.can_fetch("*", url_to_visit):
                unique_urls = await self.crawling(url_to_visit)
                logger.debug(f"Unique urls found {len(unique_urls)}:\n {unique_urls}")
                for url in unique_urls:
                    await self.to_visit_queue.put(URLContainer(url))
            else:
                logging.info(f"Robots.txt prevents fetching {url_to_visit} - skipping")
        except RateLimitException as _exc:
            await self.handle_rate_limit(url_to_visit_container, self.backoff)
            await self.to_visit_queue.put(url_to_visit_container)
        except RedirectException as exc:
            logger.info(f"{url_to_visit} Redirected to {exc.redirect_url}")
            await self.to_visit_queue.put(URLContainer(exc.redirect_url))
        except NotFoundException as exc:
            logger.info(f"{exc} - Page not found for {url_to_visit}")
        except Exception as exc:
            if url_to_visit_container.tries < self.max_retries:
                logger.warning(
                    f"Retrying {url_to_visit} - try {url_to_visit_container.tries}"
                )
                await self.to_visit_queue.put(url_to_visit_container)
            else:
                logger.error(
                    f"Error processing {url_to_visit}: {exc} and Max retries reached - skipping"
                )
        finally:
            self.to_visit_queue.task_done()

    async def crawling(self, url: str) -> Set:
        """
        Crawls a given URL and extracts unique links from its HTML content.

        This asynchronous method performs web crawling by:
        1. Fetching HTML content from the URL
        2. Handling various HTTP status codes and exceptions
        3. Extracting links from the HTML
        4. Storing crawled URLs and their links
        5. Deduplicating extracted URLs
        Args:
            url (str): The URL to crawl
        Returns:
            Set: A set of unique URLs found in the page that haven't been crawled yet.
                Returns None if the HTML content is empty.
        Raises:
            NotFoundException: When the URL returns a 404 status code
            RateLimitException: When the crawler is being rate limited (429)
            RedirectException: When the URL redirects (301, 302)
            GenericCrawlerException: For other HTTP errors not explicitly handled
        """

        logger.info(f"Crawling {url}")

        # Get HTML content
        try:
            html_content = await self.network_client.query_html(url)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                self.storage_client.add(url)
                raise NotFoundException(f"Page not found for {url}")
            elif e.response.status_code == 429:
                raise RateLimitException(f"Rate limited for {url}")
            elif e.response.status_code in (301, 302):
                self.storage_client.add(url)
                raise RedirectException(
                    f"Redirected for {url}",
                    redirect_url=str(e.response.next_request.url),
                    status_code=e.response.status_code,
                )
            else:
                raise GenericCrawlerException(f"Generic Crawler Error: {e}")

        # Handle empty HTML pages
        if not html_content:
            self.storage_client.add(url)
            return None

        # Extract all links
        html_urls = HTMLParser().extract_links(
            self.url_filter.filter_links, html_content
        )

        # Save to storage all the links contained in the HTML
        self.storage_client.add(url, {"links": list(html_urls)})

        # filter out duplicates
        unique_urls = URLDeDuplicator().dedup_url(
            html_urls, set(self.storage_client.get_all_keys())
        )

        return unique_urls

    async def handle_rate_limit(self, url_container: URLContainer, backoff: int):
        """
        Handle rate limiting by implementing an exponential backoff strategy.

        This method applies a delay when rate limiting is detected, using an exponential
        backoff approach with some random jitter to prevent synchronized retries.

        Args:
            url_container (URLContainer): Container holding URL information and retry attempts
            backoff (int): Base backoff time in seconds

        Returns:
            None
        """
        back_pressure = (backoff + random.uniform(0, backoff)) * url_container.tries
        logger.warning(
            f"Rate limited - retrying {url_container.base_url} in {back_pressure} seconds"
        )
        await asyncio.sleep(back_pressure)
