from url_deduplicator import URLDeDuplicator


def test_dedup_url_same():
    deduplicator = URLDeDuplicator()
    incoming_urls = {
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
    }
    visited_urls = {
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
    }
    result = deduplicator.dedup_url(incoming_urls, visited_urls)
    assert result == set()


def test_dedup_url():
    deduplicator = URLDeDuplicator()
    incoming_urls = {
        "https://www.example1.com",
        "https://www.example2.com",
        "https://www.example3.com",
        "https://www.example4.com",
        "https://www.example5.com",
    }
    visited_urls = {
        "https://www.example1.com",
        "https://www.example2.com",
        "https://www.example7.com",
        "https://www.example8.com",
        "https://www.example9.com",
    }
    result = deduplicator.dedup_url(incoming_urls, visited_urls)
    expected_result = {
        "https://www.example3.com",
        "https://www.example4.com",
        "https://www.example5.com",
    }
    assert result == expected_result


def test_dedup_url_empty():
    deduplicator = URLDeDuplicator()
    incoming_urls = None
    visited_urls = {
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
    }
    result = deduplicator.dedup_url(incoming_urls, visited_urls)
    assert result == set()


def test_dedup_url_none():
    deduplicator = URLDeDuplicator()
    incoming_urls = None
    visited_urls = None
    result = deduplicator.dedup_url(incoming_urls, visited_urls)
    assert result == set()


def test_dedup_url_no_visited():
    deduplicator = URLDeDuplicator()
    incoming_urls = {
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
    }
    visited_urls = None
    result = deduplicator.dedup_url(incoming_urls, visited_urls)
    assert result == incoming_urls


def test_dedup_url_no_incoming():
    deduplicator = URLDeDuplicator()
    incoming_urls = None
    visited_urls = {
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
        "https://www.example.com",
    }
    result = deduplicator.dedup_url(incoming_urls, visited_urls)
    assert result == set()
