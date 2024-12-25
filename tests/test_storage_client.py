from storage_client import StorageClient


def test_add():
    storage_client = StorageClient()
    storage_client.add("https://www.example.com", "example")

    assert storage_client.get("https://www.example.com") == "example"


def test_add_none():
    storage_client = StorageClient()
    storage_client.add("https://www.example.com")

    assert storage_client.get("https://www.example.com") is None
