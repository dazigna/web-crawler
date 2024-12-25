import httpx
import uuid
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class NetworkClient:
    """
    NetworkClient is a class that provides asynchronous methods to query HTML content from a given URL using the httpx library.

    Attributes:
        client (httpx.AsyncClient): An instance of httpx.AsyncClient used to make HTTP requests.

    Methods:
        __init__(client=httpx.AsyncClient): Initializes the NetworkClient with an optional httpx.AsyncClient instance.
        query_html(url: str) -> str: Asynchronously queries the given URL and returns the HTML content.

    Example:
        client = NetworkClient()
        html_content = await client.query_html("https://example.com")
    """

    def __init__(
        self,
        client=httpx.AsyncClient(
            timeout=5, transport=httpx.AsyncHTTPTransport(retries=3)
        ),
    ):
        self.client = client

    async def query_html(self, url: str) -> str:
        """
        Asynchronously queries the given URL and returns the HTML content.

        Args:
            url (str): The URL to query.

        Returns:
            str: The HTML content of the page.

        Raises:
            httpx.RequestError: If an error occurs while making the request.
            httpx.HTTPStatusError: If the response status code indicates an error.

        Note:
            The function sends a GET request to the specified URL with a unique User-Agent header.
            It follows redirects and raises an exception if the request fails.
        """
        headers = {
            "User-Agent": f"local-{uuid.uuid4()}",
        }
        try:
            # Do a Head first to check if content is HTML and do get only if content is valid - this may not be necessary
            # resp_head = await self.client.head(url, headers=headers, timeout=5)
            # if not ("text/html" in resp_head.headers.get("Content-Type", "")):
            #     logger.warning(f"Content type is not HTML for {url}")
            #     return
            resp = await self.client.get(url, headers=headers, follow_redirects=True)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc} for {exc.request}.")
        # except httpx.HTTPStatusError as exc:
        #     logger.error(
        #         f"Error response {exc.response.status_code} headers {exc.response.headers} while requesting {exc.request.url!r}."
        #     )
