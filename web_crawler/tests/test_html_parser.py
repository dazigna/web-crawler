from web_crawler.html_parser import HTMLParser
from bs4 import BeautifulSoup
from pathlib import Path


def test_parse():
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
    assert links == expected_links
