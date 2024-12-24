import httpx
import uuid
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class NetworkClient:
    def __init__(
        self,
        client=httpx.AsyncClient(
            timeout=5, transport=httpx.AsyncHTTPTransport(retries=3)
        ),
    ):
        self.client = client

    async def query_html(self, url: str) -> str:
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

    async def query_html_rate_limiting(self, url: str, limit) -> str:
        async with limit:
            self.query_html(url)
