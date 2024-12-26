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
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "--url", type=str, help="The URL to start crawling from", required=True
    )
    optional.add_argument(
        "--workers",
        type=int,
        nargs="?",
        const=1,
        default=1,
        help="Number of workers to use for crawling - default to 1 worker",
    )
    optional.add_argument(
        "--retries",
        type=int,
        nargs="?",
        const=3,
        default=3,
        help="Number of retries to attempt for each URL - default is 3 tries",
    )
    optional.add_argument(
        "--backoff",
        nargs="?",
        const=5,
        default=5,
        type=int,
        help="Backoff time in seconds between retries - default is 5 seconds",
    )

    args = parser.parse_args()
    logger.info(f"Starting web crawler with current args:\n {args}")
    # Check for arguments validity
    if args.workers < 1:
        logger.error("Number of workers must be greater than 0")
        exit(1)
    if args.retries < 1:
        logger.error("Number of retries must be greater than 0")
        exit(1)
    if args.backoff < 0:
        logger.error("Backoff time must be greater than or equal to 0")
        exit(1)
    if args.url == "":
        logger.error("URL cannot be empty")
        exit(1)

    asyncio.run(main(args.url, args.workers, args.retries, args.backoff))
