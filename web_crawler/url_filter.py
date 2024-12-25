import tldextract

from urllib.parse import urlparse, urljoin
import logging


logger = logging.getLogger(__name__)


class URLFilter:
    """
    A class to filter and validate URLs based on specified criteria.

    Attributes:
    -----------
    base_url : str
        The base URL to be used for resolving relative URLs.
    allowed_schemes : list
        A list of allowed URL schemes (e.g., "http", "https").

    Methods:
    --------
    __init__(base_url: str, allowed_schemes: list = ["http", "https"]):
        Initializes the URLFilter with a base URL and allowed schemes.

    filter_links(link: str) -> Optional[str]:
        Filters and validates a given link based on the allowed schemes and domain.
        Returns the resolved URL if valid, otherwise returns None.
    """

    def __init__(
        self,
        base_url: str,
        allowed_schemes: list = ["http", "https"],
    ):
        self.base_url = base_url
        self.allowed_domain = tldextract.extract(self.base_url).domain
        self.allowed_schemes = allowed_schemes

    def filter_links(self, link):
        """
        Filters and processes a given URL based on predefined rules.

        Args:
            link (str): The URL to be filtered and processed.

        Returns:
            str or None: The processed URL if it meets the criteria, otherwise None.

        The function performs the following checks:
        1. Returns None if the link is empty.
        2. Returns None if the link has a scheme that is not in the allowed schemes.
        3. Returns None if the link has a scheme but no hostname.
        4. Returns None if the link has no scheme but has a top-level domain suffix.
        5. Returns an absolute URL if the link is a relative path.
        6. Returns the link if it is an absolute URL within the allowed domain.
        """
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
