import pytest
from web_crawler.network_client import NetworkClient
import httpx


@pytest.mark.asyncio
async def test_query_html_200():
    # Arrange
    transport = httpx.MockTransport(
        handler=lambda request: httpx.Response(
            200, headers={"Content-type": "text/html"}, text="<html></html>"
        )
    )
    network_client = NetworkClient(client=httpx.AsyncClient(transport=transport))
    url = "https://example.com"

    result = await network_client.query_html(url)

    assert str(result) == "<html></html>"


@pytest.mark.asyncio
async def test_query_html_429():
    # Arrange
    transport = httpx.MockTransport(
        handler=lambda request: httpx.Response(
            429, headers={"Content-type": "text/html"}, text="<html></html>"
        )
    )
    network_client = NetworkClient(client=httpx.AsyncClient(transport=transport))
    url = "https://example.com"

    with pytest.raises(httpx.HTTPStatusError) as exc:
        await network_client.query_html(url)

    assert exc.value.response.status_code == 429
