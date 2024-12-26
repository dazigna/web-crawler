import asyncio
import time
import logging
import argparse

from web_crawler.web_crawler import WebCrawler

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    encoding="utf-8",
    handlers=[logging.FileHandler("debug.log", mode="w"), logging.StreamHandler()],
)

logger = logging.getLogger("web_crawler")
logging.getLogger("chardet.charsetprober").disabled = True


async def main(url: str, num_workers: int, max_retries: int, backoff: int):
    start_time = time.perf_counter()
    wc = WebCrawler(
        url, num_workers=num_workers, max_retries=max_retries, backoff=backoff
    )
    await wc.crawl_with_workers()
    elapsed = time.perf_counter() - start_time
    logger.info(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        help="The URL to start crawling from",
    )
    parser.add_argument(
        "--workers",
        type=int,
        nargs="?",
        const=1,
        default=1,
        help="Number of workers to use for crawling - default to 1 worker",
    )
    parser.add_argument(
        "--retries",
        type=int,
        nargs="?",
        const=3,
        default=3,
        help="Number of retries to attempt for each URL - default is 3 tries",
    )
    parser.add_argument(
        "--backoff",
        nargs="?",
        const=5,
        default=5,
        type=int,
        help="Backoff time in seconds between retries - default is 5 seconds",
    )

    # Start the web crawler
    domain = "https://overstory.com"
    # domain = "https://crawler-test.com"
    # domain = "https://realpython.github.io/fake-jobs/"
    # domain = "https://webscraper.io/test-sites/e-commerce/allinone"
    # domain = "https://quotes.toscrape.com/"
    args = parser.parse_args()
    logger.info(f"Starting web crawler with current args:\n {args}")
    asyncio.run(main(args.url or domain, args.workers, args.retries, args.backoff))
