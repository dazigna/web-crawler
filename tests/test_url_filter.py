import unittest
from url_filter import URLFilter


class TestUrlFilter(unittest.TestCase):

    def test_filter_links_none(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = None

        result = url_filter.filter_links(link)

        self.assertIsNone(result)

    def test_filter_links_empty(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = ""

        result = url_filter.filter_links(link)

        self.assertIsNone(result)

    def test_filter_links_invalid_scheme(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = "ftp://example.com"

        result = url_filter.filter_links(link)

        self.assertIsNone(result)

    def test_filter_links_invalid_hostname(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = "https:///about"

        result = url_filter.filter_links(link)

        self.assertIsNone(result)

    def test_filter_links_invalid_domain(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = "example.com/about"

        result = url_filter.filter_links(link)

        self.assertIsNone(result)

    def test_filter_links_relative_path(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = "/about"

        result = url_filter.filter_links(link)

        self.assertEqual(result, "https://example.com/about")

    def test_filter_links_absolute_url_same_domain(self):
        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = "https://example.com/about"

        result = url_filter.filter_links(link)

        self.assertEqual(result, "https://example.com/about")

    def test_filter_links_absolute_url_different_domain(self):

        base_url = "https://example.com"
        url_filter = URLFilter(base_url)

        link = "https://otherdomain.com/about"

        result = url_filter.filter_links(link)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
