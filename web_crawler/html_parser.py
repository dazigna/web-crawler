from collections.abc import Callable
from typing import Set
import logging

logger = logging.getLogger(__name__)


class HTMLParser:
    """
    A class to parse HTML content and extract links.
    """

    def __init__(self):
        pass

    def extract_links(self, filtering_method, html_content: str) -> Set:
        """
        Extracts and filters links from the provided HTML content.

        Args:
            filtering_method (function): A function that takes a link as input and returns the filtered link.
            html_content (str): The HTML content from which to extract links.

        Returns:
            set: A set of filtered links.
        """
        # Extract all href links
        all_links = html_content.find_all("a")
        filtered_links = set()

        for href_link in all_links:
            link = href_link.get("href", "")

            link = filtering_method(link)
            if link:
                filtered_links.add(link)

        return filtered_links
