from typing import List
from urllib.parse import urlparse, urljoin
import logging


import tldextract


logger = logging.getLogger(__name__)


class URLFilter:
    """
    A URL filtering class that validates and processes URLs based on predefined rules and a base URL.

    This class provides functionality to:
    - Validate URLs based on scheme and domain rules
    - Filter and process URLs according to specific criteria
    - Handle both relative and absolute URLs
    - Ensure URLs conform to allowed domains and schemes

    Attributes:
        base_url (str): The base URL used as a reference for processing relative URLs
        extracted_base_url (ExtractResult): Parsed components of the base URL using tldextract
        allowed_domain (str): The domain name that URLs are allowed to belong to
        allowed_schemes (List[str]): List of allowed URL schemes (default: ["http", "https"])
    """

    def __init__(
        self,
        base_url: str,
        allowed_schemes: List = ["http", "https"],
    ):
        self.base_url = base_url
        self.extracted_base_url = tldextract.extract(self.base_url)
        self.allowed_domain = self.extracted_base_url.domain
        self.allowed_schemes = allowed_schemes

    def is_url_valid(self) -> bool:
        """
        Check if a given link is valid.

        Args:
            link (str): The URL to be validated.

        Returns:
            bool: True if the URL is valid, otherwise False.
        """
        urlparse_result = urlparse(self.base_url)
        return (
            urlparse_result.hostname is not None
            and self.extracted_base_url.suffix != ""
            and urlparse_result.scheme in self.allowed_schemes
        )

    def filter_links(self, link: str) -> str | None:
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
