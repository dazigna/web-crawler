from pathlib import Path
from web_crawler.storage_client import StorageClient


def test_add():
    storage_client = StorageClient(output_file_path=Path(__file__).parent)
    storage_client.add("https://www.example.com", "example")

    assert storage_client.get("https://www.example.com") == "example"


def test_add_none():
    storage_client = StorageClient(output_file_path=Path(__file__).parent)
    storage_client.add("https://www.example.com")

    assert storage_client.get("https://www.example.com") is None


def test_get_all_keys():
    storage_client = StorageClient(output_file_path=Path(__file__).parent)
    storage_client.add("https://www.example.com", "example")
    storage_client.add("https://www.test.com", "test")

    keys = storage_client.get_all_keys()
    assert "https://www.example.com" in keys
    assert "https://www.test.com" in keys
    assert len(keys) == 2


def test_get_all_keys_empty():
    storage_client = StorageClient(output_file_path=Path(__file__).parent)
    keys = storage_client.get_all_keys()
    assert len(keys) == 0
