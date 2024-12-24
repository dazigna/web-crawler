# from unittest import IsolatedAsyncioTestCase
# from unittest.mock import patch, MagicMock
# from web_crawler import WebCrawler
# import httpx


# class WebCrawlerTest(IsolatedAsyncioTestCase):

#     @patch("web_crawler.RobotFileParser")
#     def test_get_and_parse_robots_txt(self, MockRobotFileParser):
#         # Arrange
#         mock_rp = MockRobotFileParser.return_value
#         mock_rp.crawl_delay.return_value = 10
#         mock_rp.request_rate.return_value = 5
#         mock_rp.can_fetch.return_value = True

#         start_url = "https://example.com"
#         crawler = WebCrawler(start_url)

#         # Act
#         result = crawler.get_and_parse_robots_txt(start_url)

#         # Assert
#         assert result["crawl_delay"] == 10
#         assert result["request_rate"] == 5
#         assert result["robot_parser"] == mock_rp

#         mock_rp.read.assert_called()

#     def test_filter_links_relative_path(self):
#         # Arrange
#         start_url = "https://example.com"
#         crawler = WebCrawler(start_url)
#         link = "/about"

#         # Act
#         result = crawler.filter_links(link)

#         # Assert
#         self.assertEqual(result, "https://example.com/about")

#     def test_filter_links_absolute_url_same_domain(self):
#         # Arrange
#         start_url = "https://example.com"
#         crawler = WebCrawler(start_url)
#         link = "https://example.com/about"

#         # Act
#         result = crawler.filter_links(link)

#         # Assert
#         self.assertEqual(result, "https://example.com/about")

#     def test_filter_links_absolute_url_different_domain(self):
#         # Arrange
#         start_url = "https://example.com"
#         crawler = WebCrawler(start_url)
#         link = "https://otherdomain.com/about"

#         # Act
#         result = crawler.filter_links(link)

#         # Assert
#         self.assertIsNone(result)

#     def test_filter_links_no_scheme(self):
#         # Arrange
#         start_url = "https://example.com"
#         crawler = WebCrawler(start_url)
#         link = "example.com/about"

#         # Act
#         result = crawler.filter_links(link)

#         # Assert
#         self.assertIsNone(result)

#     def test_filter_links_no_hostname(self):
#         # Arrange
#         start_url = "https://example.com"
#         crawler = WebCrawler(start_url)
#         link = "https:///about"

#         # Act
#         result = crawler.filter_links(link)

#         # Assert
#         self.assertIsNone(result)


# if __name__ == "__main__":
#     unittest.main()
