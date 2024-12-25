from dataclasses import dataclass


@dataclass
class URLContainer:
    """
    URLContainer class to manage a base URL and track the number of times it is accessed.

    Attributes:
        _base_url (str): The base URL.
        _tries (int): The number of times the base URL has been accessed.

    Properties:
        base_url (str): Gets the base URL and increments the access count.
        tries (int): Gets the number of times the base URL has been accessed.
    """

    _base_url: str
    _tries: int = 0

    @property
    def base_url(self):
        self._tries += 1
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def tries(self):
        return self._tries
