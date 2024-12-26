from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)


class RobotParser:
    """
    A class for parsing and interpreting robots.txt files from websites.

    This class handles the fetching and parsing of robots.txt files, and provides methods
    to check crawling permissions and retrieve crawling parameters like delays and request rates.

        base_url (str): The base URL of the website to crawl.
        default_crawl_delay (int, optional): Default delay between crawls in seconds if not specified
            in robots.txt. Defaults to 1.
        default_request_rate (int, optional): Default number of requests allowed per second if not
            specified in robots.txt. Defaults to 1.

    Attributes:
        robot_url (str): The complete URL to the robots.txt file.
        robot_parser (RobotFileParser): Parser object for handling robots.txt content.
        _default_crawl_delay (int): Default crawl delay if none specified in robots.txt.
        _default_request_rate (int): Default request rate if none specified in robots.txt.
    """

    def __init__(
        self, base_url: str, default_crawl_delay: int = 1, default_request_rate: int = 1
    ):
        self.robot_url = urljoin(base_url, "robots.txt")
        self.robot_parser = RobotFileParser()
        self._default_crawl_delay = default_crawl_delay
        self._default_request_rate = default_request_rate
        self.parse()

    def parse(self):
        """
        Parses the robots.txt file from the specified URL.

        This method sets the URL for the robot parser and reads the robots.txt file
        to determine the rules for web crawling.

        Raises:
            URLError: If there is an issue with accessing the robots.txt file.
        """
        self.robot_parser.set_url(self.robot_url)
        self.robot_parser.read()

    def can_fetch(self, user_agent: str, url: str) -> bool:
        """
        Check if a given user agent is allowed to fetch a specified URL according to the robots.txt rules.

        Args:
            user_agent (str): The user agent string to be checked.
            url (str): The URL to be fetched.

        Returns:
            bool: True if the user agent is allowed to fetch the URL, False otherwise.
        """
        return self.robot_parser.can_fetch(user_agent, url)

    @property
    def crawl_delay(self) -> int:
        """
        Returns the crawl delay for the web crawler.

        This method retrieves the crawl delay specified in the robots.txt file for all user agents ("*").
        If no crawl delay is specified, it returns a default crawl delay value.

        Returns:
            int: The crawl delay in seconds.
        """
        return self.robot_parser.crawl_delay("*") or self._default_crawl_delay

    @property
    def request_rate(self) -> int:
        """
        Retrieves the request rate for the web crawler.

        This method returns the request rate specified in the robots.txt file for all user agents.
        If no request rate is specified, it returns the default request rate.

        Returns:
            RequestRate: The request rate for the web crawler.
        """
        return self.robot_parser.request_rate("*") or self._default_request_rate
