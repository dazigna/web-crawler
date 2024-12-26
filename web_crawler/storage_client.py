import json
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class StorageClient:
    """
    A class that provides storage functionality for URLs and their associated data.
    This class implements a simple key-value storage system where URLs serve as keys
    and can be associated with arbitrary data. The storage can be persisted to a JSON file.
    Attributes:
        storage (dict): Dictionary storing URL-data pairs
        output_file_path (Path): Directory path where storage file will be saved
        output_file_name (str): Name of the storage file

    """

    def __init__(self, output_file_path: Path, output_file_name: str = "storage.json"):
        self.storage = {}
        self.output_file_path = output_file_path
        self.output_file_name = output_file_name

    def add(self, url: str, data: List | None = None):
        """
        Adds a URL and its associated data to the storage.

        Args:
            url (str): The URL to be added to the storage.
            data (optional): The data associated with the URL. Defaults to None.
        """
        logger.info(f"Adding URL: {url} and data: {data}")
        self.storage[url] = data

    def remove(self, url: str):
        """
        Remove a URL from the storage.

        Args:
            url (str): The URL to be removed from the storage.

        Raises:
            KeyError: If the URL is not found in the storage.
        """
        self.storage.pop(url)

    def get(self, url: str):
        """
        Retrieve data from storage for the given URL.

        Args:
            url (str): The URL for which to retrieve the data.

        Returns:
            The data associated with the given URL from storage.
        """
        return self.storage.get(url)

    def get_all(self) -> Dict:
        """
        Retrieve all items from the storage.

        Returns:
            list: A list containing all items in the storage.
        """
        return self.storage

    def get_all_keys(self) -> List:
        """
        Retrieve all keys from the storage.

        Returns:
            list: A list containing all keys in the storage.
        """
        logger.info(f"Retrieving all keys from storage{self.storage.keys()}")
        return self.storage.keys()

    def write_to_file(self):
        """
        Writes the contents of the storage to a file in JSON format.

        Raises:
            IOError: If the file cannot be opened or written to.
        """
        output_file_path = self.output_file_path / self.output_file_name
        with open(output_file_path, "w") as f:
            f.write(json.dumps(self.storage, indent=4))

    def contains(self, url: str) -> bool:
        """
        Check if the storage contains a given URL.

        Args:
            url (str): The URL to check for in the storage.

        Returns:
            bool: True if the URL is found in the storage, False otherwise.
        """
        return url in self.storage.keys()
