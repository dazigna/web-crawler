import unittest
from html_parser import HTMLParser
from bs4 import BeautifulSoup
from pathlib import Path


class TestHtmlParser(unittest.TestCase):
    def test_parse(self):
        fixture_path = Path(__file__).parent / "fixtures" / "fixture_html.html"
        with open(fixture_path) as f:
            html_content = BeautifulSoup(f.read(), "html.parser")
        links = HTMLParser().extract_links(lambda x: x, html_content)
        expected_links = {
            "/test",
            "#section1",
            "/submit",
            "https://www.subdomain.example.com",
            "https://www.example.com",
        }
        self.assertEqual(links, expected_links)


if __name__ == "__main__":
    unittest.main()
