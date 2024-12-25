import json
import logging

logger = logging.getLogger(__name__)


class StorageClient:
    """
    StorageClient is a simple in-memory storage client for storing and retrieving data associated with URLs.

    Methods:
        __init__():
            Initializes the StorageClient with an empty storage dictionary.

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

    def __init__(self):
        self.storage = {}

    def add(self, url, data=None):
        """
        Adds a URL and its associated data to the storage.

        Args:
            url (str): The URL to be added to the storage.
            data (optional): The data associated with the URL. Defaults to None.
        """
        self.storage[url] = data

    def remove(self, url):
        """
        Remove a URL from the storage.

        Args:
            url (str): The URL to be removed from the storage.

        Raises:
            KeyError: If the URL is not found in the storage.
        """
        self.storage.pop(url)

    def get(self, url):
        """
        Retrieve data from storage for the given URL.

        Args:
            url (str): The URL for which to retrieve the data.

        Returns:
            The data associated with the given URL from storage.
        """
        return self.storage.get(url)

    def get_all(self):
        """
        Retrieve all items from the storage.

        Returns:
            list: A list containing all items in the storage.
        """
        return self.storage

    def write_to_file(self, filename):
        """
        Writes the contents of the storage to a file in JSON format.

        Args:
            filename (str): The name of the file to write to.

        Raises:
            IOError: If the file cannot be opened or written to.
        """
        with open(filename, "w") as f:
            f.write(json.dumps(self.storage, indent=4))
