import unittest

from url_deduplicator import URLDeDuplicator


class TestURLDeDuplicator(unittest.TestCase):
    def test(self):
        return True

    # def test_dedup_url_same(self):
    #     deduplicator = URLDeDuplicator()
    #     incoming_urls = {
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #     }
    #     visited_urls = {
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #     }
    #     result = deduplicator.dedup_url(incoming_urls, visited_urls)
    #     self.assertEqual(result, set())

    # def test_dedup_url(self):
    #     deduplicator = URLDeDuplicator()
    #     incoming_urls = {
    #         "https://www.example1.com",
    #         "https://www.example2.com",
    #         "https://www.example3.com",
    #         "https://www.example4.com",
    #         "https://www.example5.com",
    #     }
    #     visited_urls = {
    #         "https://www.example1.com",
    #         "https://www.example2.com",
    #         "https://www.example7.com",
    #         "https://www.example8.com",
    #         "https://www.example9.com",
    #     }
    #     result = deduplicator.dedup_url(incoming_urls, visited_urls)
    #     expected_result = {
    #         "https://www.example3.com",
    #         "https://www.example4.com",
    #         "https://www.example5.com",
    #     }
    #     self.assertEqual(result, expected_result)

    # def test_dedup_url_empty(self):
    #     deduplicator = URLDeDuplicator()
    #     incoming_urls = None
    #     visited_urls = {
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #     }
    #     result = deduplicator.dedup_url(incoming_urls, visited_urls)
    #     self.assertEqual(result, set())

    # def test_dedup_url_none(self):
    #     deduplicator = URLDeDuplicator()
    #     incoming_urls = None
    #     visited_urls = None
    #     result = deduplicator.dedup_url(incoming_urls, visited_urls)
    #     self.assertEqual(result, set())

    # def test_dedup_url_no_visited(self):
    #     deduplicator = URLDeDuplicator()
    #     incoming_urls = {
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #     }
    #     visited_urls = None
    #     result = deduplicator.dedup_url(incoming_urls, visited_urls)
    #     self.assertEqual(result, incoming_urls)

    # def test_dedup_url_no_incoming(self):
    #     deduplicator = URLDeDuplicator()
    #     incoming_urls = None
    #     visited_urls = {
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #         "https://www.example.com",
    #     }
    #     result = deduplicator.dedup_url(incoming_urls, visited_urls)
    #     self.assertEqual(result, set())


if __name__ == "__main__":
    unittest.main()
