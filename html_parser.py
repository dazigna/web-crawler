import logging

logger = logging.getLogger(__name__)


class HTMLParser:
    def __init__(self):
        pass

    # Use a decorator maybe?
    def extract_links(self, filtering_method, html_content: str) -> set:
        # Extract all href links
        all_links = html_content.find_all("a")
        filtered_links = set()

        for href_link in all_links:
            link = href_link.get("href", "")

            link = filtering_method(link)
            if link:
                filtered_links.add(link)

        return filtered_links
