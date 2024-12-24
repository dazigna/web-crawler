import sys
import asyncio
import time
from dataclasses import dataclass
import logging
import httpx
import random

from network_client import NetworkClient
from storage_client import CrawlerStorage
from html_parser import HTMLParser
from url_filter import URLFilter
from url_deduplicator import URLDeDuplicator
from robot_parser import RobotParser


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger = logging.getLogger("web_crawler")
logging.getLogger("chardet.charsetprober").disabled = True


@dataclass
class URLContainer:
    _base_url: str
    _tries: int = 0

    @property
    def base_url(self):
        self._tries += 1
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def tries(self):
        return self._tries


class WebCrawler:
    def __init__(
        self,
        start_url: str,
        network_client: NetworkClient = NetworkClient(),
        storage_client: CrawlerStorage = CrawlerStorage(),
        num_workers: int = 2,
        max_retries: int = 3,
        backoff: int = 5,
    ):

        # Use Tldextract to account for different TLDs
        self.start_url = start_url

        # Robot parsing
        self.network_client = network_client
        self.url_filter = URLFilter(self.start_url)
        self.robot_parser = RobotParser(self.start_url)

        self.storage_client = storage_client

        self.to_visit_queue = asyncio.Queue()
        self.currently_visiting = set()
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.backoff = backoff

    async def crawl_with_workers(self):
        logger.info(f"Starting crawling with {self.num_workers} workers")
        await self.to_visit_queue.put(URLContainer(self.start_url))

        logger.info(
            f"{self.start_url} added to queue, queue size: {self.to_visit_queue.qsize()}"
        )

        # Worker creation
        workers = [
            asyncio.create_task(self.workers(), name=f"worker_{i}")
            for i in range(self.num_workers)
        ]

        await self.to_visit_queue.join()

        for worker in workers:
            worker.cancel()

        # Save to file
        self.storage_client.write_to_file("storage.json")

    async def workers(self):
        logger.info(f"Starting worker {asyncio.current_task().get_name()}")
        while True:
            try:
                # Abide by robots crawling policy
                await asyncio.sleep(self.robot_parser.crawl_delay)
                await self.process_crawling_unit()
            except asyncio.CancelledError:
                logger.error(f"Cancelled worker {asyncio.current_task().get_name()}")
                return

    async def process_crawling_unit(self):
        # Fetch URL from queue
        url_to_visit_container = await self.to_visit_queue.get()
        url_to_visit = url_to_visit_container.base_url

        logger.info(f"Visiting {url_to_visit}")
        try:
            # Check if we can fetch the URL based on robots.txt
            if self.robot_parser.can_fetch("*", url_to_visit):
                unique_urls = await self.crawling(url_to_visit)
                logger.info(f"Unique urls found: {len(unique_urls)}")
                for url in unique_urls:
                    await self.to_visit_queue.put(URLContainer(url))
            else:
                logging.warning(f"Robots.txt prevents fetching {url_to_visit}")

        # need to handle 429 error
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error processing {url_to_visit}: {exc}")
            # Poor man's back pressure - add Jitter to avoid synchronous behavior
            if exc.response.status_code == 429 and url_to_visit_container.tries < 3:

                back_pressure = (
                    self.backoff + random.uniform(0, self.backoff)
                ) * url_to_visit_container.tries
                logger.error(
                    f"Rate limited - retrying {url_to_visit} in {back_pressure} seconds"
                )
                await asyncio.sleep(back_pressure)
                await self.to_visit_queue.put(url_to_visit_container)

        except Exception as e:
            logger.error(f"Error processing {url_to_visit}: {e}")
            # Stop retrying link after max_retries
            if url_to_visit_container.tries < self.max_retries:
                logger.info(
                    f"Retrying {url_to_visit} - try {url_to_visit_container.tries}"
                )
                await self.to_visit_queue.put(url_to_visit_container)
            else:
                logger.error(f"Max retries reached for {url_to_visit} - skipping")
        finally:
            # WHY AM I DOING THIS?
            self.to_visit_queue.task_done()

    # Crawling unit
    async def crawling(self, url):
        logger.info(f"Crawling {url}")

        # Get HTML content
        html_content = await self.network_client.query_html(url)

        # Parse HTML content
        if not html_content:
            self.storage_client.add(url)
            return

        # Extract all links
        html_urls = HTMLParser().extract_links(
            self.url_filter.filter_links, html_content
        )

        # filter out duplicates
        unique_urls = URLDeDuplicator().dedup_url(
            html_urls, set(self.storage_client.get_all())
        )

        # Save to storage all the links contained in the HTML
        self.storage_client.add(url, {"links": list(html_urls)})

        return unique_urls


async def main():
    start_time = time.perf_counter()
    # Start the web crawler
    # domain = "https://www.overstory.com"
    # domain = "https://crawler-test.com"
    domain = "https://realpython.github.io/fake-jobs/"
    # domain = "https://webscraper.io/test-sites/e-commerce/allinone"
    # domain = "https://quotes.toscrape.com/"
    wc = WebCrawler(domain)
    await wc.crawl_with_workers()
    elapsed = time.perf_counter() - start_time
    logger.info(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
