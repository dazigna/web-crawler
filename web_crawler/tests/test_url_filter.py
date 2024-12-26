from web_crawler.url_filter import URLFilter


def test_filter_links_none():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = None

    result = url_filter.filter_links(link)
    assert result is None


def test_filter_links_empty():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = ""

    result = url_filter.filter_links(link)

    assert result is None


def test_filter_links_invalid_scheme():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = "ftp://example.com"

    result = url_filter.filter_links(link)

    assert result is None


def test_filter_links_invalid_hostname():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = "https:///about"

    result = url_filter.filter_links(link)

    assert result is None


def test_filter_links_invalid_domain():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = "example.com/about"

    result = url_filter.filter_links(link)

    assert result is None


def test_filter_links_relative_path():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = "/about"

    result = url_filter.filter_links(link)

    assert result == "https://example.com/about"


def test_filter_links_absolute_url_same_domain():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = "https://example.com/about"

    result = url_filter.filter_links(link)

    assert result == "https://example.com/about"


def test_filter_links_absolute_url_different_domain():
    base_url = "https://example.com"
    url_filter = URLFilter(base_url)

    link = "https://otherdomain.com/about"

    result = url_filter.filter_links(link)
    assert result is None
