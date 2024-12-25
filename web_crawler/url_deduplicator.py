from typing import Set


class URLDeDuplicator:
    """
    A class used to deduplicate URLs.
    Can be leverage to implement different comparison methods, such as cosine similarity or Jacard similarity
    """

    def __init__(self):
        pass

    def dedup_url(self, incoming_urls: Set, visited_urls: Set) -> Set:
        """
        Remove URLs that have already been visited from the set of incoming URLs.

        Args:
            incoming_urls (set): A set of URLs to be processed.
            visited_urls (set): A set of URLs that have already been visited.

        Returns:
            set: A set of URLs that have not been visited yet. If incoming_urls is None, returns an empty set.
                 If visited_urls is None, returns the incoming_urls set.
        """
        if incoming_urls is None:
            return set()
        if visited_urls is None:
            return incoming_urls

        return incoming_urls - visited_urls
