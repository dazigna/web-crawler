from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)


class RobotParser:
    def __init__(self, base_url, default_crawl_delay=1, default_request_rate=1):
        self.robot_url = urljoin(base_url, "robots.txt")
        self.robot_parser = RobotFileParser()
        self._default_crawl_delay = default_crawl_delay
        self._default_request_rate = default_request_rate
        self.parse()

    def parse(self):
        self.robot_parser.set_url(self.robot_url)
        self.robot_parser.read()

    def can_fetch(self, user_agent, url):
        return self.robot_parser.can_fetch(user_agent, url)

    @property
    def crawl_delay(self):
        return self.robot_parser.crawl_delay("*") or self._default_crawl_delay

    @property
    def request_rate(self):
        return self.robot_parser.request_rate("*") or self._default_request_rate
