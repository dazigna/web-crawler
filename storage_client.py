import json
import logging

logger = logging.getLogger(__name__)


# Maybe implement some kind of streaming to file ?
class StorageClient:
    def __init__(self):
        self.storage = {}

    def add(self, url, data=None):
        self.storage[url] = data

    def remove(self, url):
        self.storage.pop(url)

    def get(self, url):
        return self.storage.get(url)

    def get_all(self):
        return self.storage

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(json.dumps(self.storage, indent=4))
