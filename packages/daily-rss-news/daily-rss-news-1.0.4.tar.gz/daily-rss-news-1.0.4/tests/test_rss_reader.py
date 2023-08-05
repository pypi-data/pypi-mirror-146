import pytest
import requests

from rss_reader.rss_reader import RssReader
from .test_argparse import set_cli_args_options


rss_example = '''
        <rss version="2.0">
            <channel>
                <title>Feed title</title>
                <link>Feed link</link>
                <description>Feed description</description>
                <pubDate>Feed pubDate</pubDate>
                <image>
                    <title>Feed image title</title>
                    <link>Feed image link</link>
                    <url>Feed image url</url>
                </image>
                <item>
                    <title>Item 1 title</title>
                    <link>Item 1 link</link>
                    <pubDate>Item 1 pubDate</pubDate>
                </item>
                <item>
                    <title>Item 2 title</title>
                    <link>Item 2 link</link>
                    <pubDate>Item 2 pubDate</pubDate>
                </item>
            </channel>    
        </rss>
    '''


@pytest.fixture
def set_parser(set_cli_args_options):
    """ Accepts fixture from test_argparse that sets mocked cli arguments
     and assign them as RssReader object's parsed arguments """

    reader = RssReader()
    reader.parser.cli_args = set_cli_args_options
    return reader


def test_rss_reader(monkeypatch, set_parser):
    """ Tests rss news count and its item info """

    class MockResponse:
        """ class that acts as mock object """

        def __init__(self, rss):
            self.content = rss

    def mock_get(*args, **kwargs):
        """ function that returns mock object when requests.get method called """

        return MockResponse(rss_example)

    monkeypatch.setattr(requests, 'get', mock_get)
    reader = set_parser
    reader.get_news()
    assert len(reader.news) == 1
    news_1 = reader.news[0]
    assert news_1['title'] == 'Item 1 title'
    assert news_1['link'] == 'Item 1 link'
    assert news_1['pubDate'] == 'Item 1 pubDate'
