import pytest

from unittest.mock import AsyncMock, patch, MagicMock
from web_crawler.web_crawler import WebCrawler
from web_crawler.url_container import URLContainer
from web_crawler.html_parser import HTMLParser
from web_crawler.url_deduplicator import URLDeDuplicator

from web_crawler.web_crawler_exceptions import (
    RateLimitException,
    RedirectException,
    NotFoundException,
)


# ----------- Scheduling logic ------------


@pytest.mark.asyncio
async def test_process_crawling_unit_success():
    network_client = MagicMock()
    storage_client = MagicMock()
    storage_client.contains = MagicMock(return_value=False)
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(return_value=["https://example.com/page1"])

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)

    await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 1
    assert crawler.to_visit_queue.get_nowait().base_url == "https://example.com/page1"
    crawler.crawling.assert_awaited_once_with("https://example.com")


@pytest.mark.asyncio
async def test_process_crawling_unit_already_visited():
    network_client = MagicMock()
    storage_client = MagicMock()
    storage_client.contains = MagicMock(return_value=True)
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(return_value=["https://example.com/page1"])

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)

    await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 0
    crawler.crawling.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_crawling_unit_robots_txt_prevents_fetching():
    network_client = MagicMock()
    storage_client = MagicMock()
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = False

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(return_value=["https://example.com/page1"])

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)

    await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 0
    crawler.crawling.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_crawling_unit_rate_limit_exception():
    network_client = MagicMock()
    storage_client = MagicMock()
    storage_client.contains = MagicMock(return_value=False)

    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(side_effect=RateLimitException("hello"))

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)
    print(crawler.crawling)
    # Mocking asyncio.sleep to avoid waiting
    with pytest.raises(RateLimitException) as exc_info:
        with patch("asyncio.sleep", new_callable=AsyncMock):
            await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 1
    assert crawler.crawling.called()


@pytest.mark.asyncio
async def test_process_crawling_unit_http_status_error_4xx():
    network_client = MagicMock()
    storage_client = MagicMock()
    storage_client.contains = MagicMock(return_value=False)

    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Error", request=None, response=MagicMock(status_code=400)
        )
    )

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)

    # Mocking asyncio.sleep to avoid waiting
    with patch("asyncio.sleep", new_callable=AsyncMock):
        await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 0


@pytest.mark.asyncio
async def test_process_crawling_unit_http_status_error_429_exceeded_retries():
    network_client = MagicMock()
    storage_client = MagicMock()
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Error", request=None, response=MagicMock(status_code=429)
        )
    )

    url_container = URLContainer("https://example.com", _tries=3)
    await crawler.to_visit_queue.put(url_container)

    with patch("asyncio.sleep", new_callable=AsyncMock):
        await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 0


@pytest.mark.asyncio
async def test_process_crawling_unit_http_status_error_301():
    network_client = MagicMock()
    storage_client = MagicMock()
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Error", request=None, response=MagicMock(status_code=301)
        )
    )

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)

    # Mocking asyncio.sleep to avoid waiting
    with patch("asyncio.sleep", new_callable=AsyncMock):
        await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 0


@pytest.mark.asyncio
async def test_process_crawling_unit_general_exception():
    network_client = MagicMock()
    storage_client = MagicMock()
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(side_effect=Exception("General error"))

    url_container = URLContainer("https://example.com")
    await crawler.to_visit_queue.put(url_container)

    await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 1


@pytest.mark.asyncio
async def test_process_crawling_unit_general_exception_exceed_retries():
    network_client = MagicMock()
    storage_client = MagicMock()
    robot_parser = MagicMock()
    robot_parser.can_fetch.return_value = True

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.robot_parser = robot_parser
    crawler.crawling = AsyncMock(side_effect=Exception("General error"))

    url_container = URLContainer("https://example.com", _tries=3)
    await crawler.to_visit_queue.put(url_container)

    await crawler.process_crawling_unit()

    assert crawler.to_visit_queue.qsize() == 0


# ----------- Processing logic ------------


@pytest.mark.asyncio
async def test_crawling_success():
    network_client = MagicMock()
    storage_client = MagicMock()
    url_filter = MagicMock()
    html_parser = MagicMock()
    url_deduplicator = MagicMock()

    network_client.query_html = AsyncMock(return_value="<html></html>")
    html_parser.extract_links = MagicMock(return_value=["https://example.com/page1"])
    url_filter.filter_links = MagicMock()
    storage_client.get_all = MagicMock(return_value=[])
    url_deduplicator.dedup_url = MagicMock(return_value=["https://example.com/page1"])

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.url_filter = url_filter
    # accessing the method's descriptor to mock it
    crawler.crawling = WebCrawler.crawling.__get__(crawler)
    HTMLParser.extract_links = html_parser.extract_links
    URLDeDuplicator.dedup_url = url_deduplicator.dedup_url

    unique_urls = await crawler.crawling("https://example.com")

    assert unique_urls == ["https://example.com/page1"]
    network_client.query_html.assert_awaited_once_with("https://example.com")
    html_parser.extract_links.assert_called_once_with(
        url_filter.filter_links, "<html></html>"
    )
    storage_client.add.assert_called_once_with(
        "https://example.com", {"links": ["https://example.com/page1"]}
    )


@pytest.mark.asyncio
async def test_crawling_no_html_content():
    network_client = MagicMock()
    storage_client = MagicMock()

    network_client.query_html = AsyncMock(return_value=None)

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )

    unique_urls = await crawler.crawling("https://example.com")

    assert unique_urls is None
    network_client.query_html.assert_awaited_once_with("https://example.com")
    storage_client.add.assert_called_once_with("https://example.com")


@pytest.mark.asyncio
async def test_crawling_with_duplicates():
    network_client = MagicMock()
    storage_client = MagicMock()
    url_filter = MagicMock()
    html_parser = MagicMock()
    url_deduplicator = MagicMock()

    network_client.query_html = AsyncMock(return_value="<html></html>")
    html_parser.extract_links = MagicMock(
        return_value=["https://example.com/page1", "https://example.com/page1"]
    )
    url_filter.filter_links = MagicMock()
    storage_client.get_all = MagicMock(return_value=["https://example.com/page1"])
    url_deduplicator.dedup_url = MagicMock(return_value=[])

    crawler = WebCrawler(
        start_url="https://example.com",
        network_client=network_client,
        storage_client=storage_client,
    )
    crawler.url_filter = url_filter
    crawler.crawling = WebCrawler.crawling.__get__(crawler)
    HTMLParser.extract_links = html_parser.extract_links
    URLDeDuplicator.dedup_url = url_deduplicator.dedup_url

    unique_urls = await crawler.crawling("https://example.com")

    assert unique_urls == []
    network_client.query_html.assert_awaited_once_with("https://example.com")
    html_parser.extract_links.assert_called_once_with(
        url_filter.filter_links, "<html></html>"
    )
    storage_client.add.assert_called_once_with(
        "https://example.com",
        {"links": ["https://example.com/page1", "https://example.com/page1"]},
    )
