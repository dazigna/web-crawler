from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock
from web_crawler import NetworkClient
import httpx


class WebCrawlerTest(IsolatedAsyncioTestCase):

    async def test_query_html_200(self):
        # Arrange
        transport = httpx.MockTransport(
            handler=lambda request: httpx.Response(
                200, headers={"Content-type": "text/html"}, text="<html></html>"
            )
        )
        network_client = NetworkClient(client=httpx.AsyncClient(transport=transport))
        url = "https://example.com"

        result = await network_client.query_html(url)

        self.assertEqual(str(result), "<html></html>")

    async def test_query_html_429(self):
        # Arrange
        transport = httpx.MockTransport(
            handler=lambda request: httpx.Response(
                429, headers={"Content-type": "text/html"}, text="<html></html>"
            )
        )
        network_client = NetworkClient(client=httpx.AsyncClient(transport=transport))
        url = "https://example.com"

        with self.assertRaises(httpx.HTTPStatusError) as exc:
            await network_client.query_html(url)

        self.assertEqual(exc.exception.response.status_code, 429)


if __name__ == "__main__":
    unittest.main()
