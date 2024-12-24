from dataclasses import dataclass


@dataclass
class URLContainer:
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
