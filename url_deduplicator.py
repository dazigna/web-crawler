# Can be leverage to implement different comparison methods, such as cosine similarity or Jacard similarity
class URLDeDuplicator:
    def __init__(self):
        pass

    def dedup_url(self, incoming_urls, visited_urls) -> set:
        if incoming_urls is None:
            return set()

        return incoming_urls - visited_urls
