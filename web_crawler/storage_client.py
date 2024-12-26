import json
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class StorageClient:
    """

    StorageClient is a simple in-memory storage client for storing and retrieving data associated with URLs.

    Attributes:
        storage (dict): A dictionary to store URLs and their associated data.
        output_file_path (Path): The path where the output file will be saved.
        output_file_name (str): The name of the output file.

    Methods:
        __init__():
            Initializes the StorageClient with an empty storage dictionary, output file path, and output file name.

        add(url, data=None):
            Adds a URL and its associated data to the storage.
            Args:
                url (str): The URL to be added.
                data (optional): The data to be associated with the URL.

        remove(url):
            Removes a URL and its associated data from the storage.
            Args:
                url (str): The URL to be removed.

        get(url):
            Retrieves the data associated with a URL from the storage.
            Args:
                url (str): The URL whose data is to be retrieved.
            Returns:
                The data associated with the URL, or None if the URL is not found.

        get_all():
            Retrieves the entire storage dictionary.
            Returns:
                dict: The storage dictionary containing all URLs and their associated data.

        write_to_file(filename):
            Writes the storage dictionary to a file in JSON format.
            Args:
                filename (str): The name of the file to write the storage data to.
    """

    def __init__(self, output_file_path: Path, output_file_name: str = "storage.json"):
        self.storage = {}
        self.output_file_path = output_file_path
        self.output_file_name = output_file_name
        # self.file_handle = open(self.output_file_path / self.output_file_name, "a")

    def add(self, url: str, data: List | None = None):
        """
        Adds a URL and its associated data to the storage.

        Args:
            url (str): The URL to be added to the storage.
            data (optional): The data associated with the URL. Defaults to None.
        """
        logger.info(f"Adding URL: {url} and data: {data}")
        self.storage[url] = data
        # self._write_line(url, data)

    # def _write_line(self, url, data):
    #     """
    #     Writes a line to the storage file.

    #     Args:
    #         url (str): The URL to be added to the storage.
    #         data (optional): The data associated with the URL. Defaults to None.
    #     """
    #     entry = {"url": url, "data": data}
    #     self.file_handle.write(json.dumps(entry) + "\n")
    #     self.file_handle.flush()

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

        Args:
            filename (str): The name of the file to write to.

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

    # def close(self):
    #     """
    #     Close the file handle.
    #     """
    #     if self.file_handle and not self.file_handle.closed:
    #         self.file_handle.close()

    # def __del__(self):
    #     self.close()
