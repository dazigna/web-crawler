import tldextract

from urllib.parse import urlparse, urljoin
import logging


logger = logging.getLogger(__name__)


class URLFilter:
    def __init__(
        self,
        base_url: str,
        allowed_schemes: list = ["http", "https"],
    ):
        self.base_url = base_url
        self.allowed_domain = tldextract.extract(self.base_url).domain
        self.allowed_schemes = allowed_schemes

    def filter_links(self, link):
        url_parsed = urlparse(link)

        # Defense
        if not link:
            return None

        # Avoid links with wrong scheme (ftp, mailto, etc)
        if url_parsed.scheme and url_parsed.scheme not in self.allowed_schemes:
            return None
        # Avoid link this one "https:///about"
        if url_parsed.scheme and not url_parsed.hostname:
            return None

        # Avoid link like this "example.com/about"
        if not url_parsed.scheme and tldextract.extract(link).suffix:
            return None

        # if link is a path -> Relative url
        # link like this /about
        if not url_parsed.hostname and url_parsed.path:
            return urljoin(self.base_url, url_parsed.path)
        # if link is in domain -> Absolute url
        elif (
            url_parsed.scheme
            and url_parsed.hostname
            and self.allowed_domain in url_parsed.hostname
        ):
            return link

        return None
