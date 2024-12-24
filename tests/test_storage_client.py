import unittest
from storage_client import StorageClient


class TestStorageClient(unittest.TestCase):
    def test_add(self):
        storage_client = StorageClient()
        storage_client.add("https://www.example.com", "example")
        self.assertEqual(storage_client.get("https://www.example.com"), "example")

    def test_add_none(self):
        storage_client = StorageClient()
        storage_client.add("https://www.example.com")
        self.assertEqual(storage_client.get("https://www.example.com"), None)


if __name__ == "__main__":
    unittest.main()
