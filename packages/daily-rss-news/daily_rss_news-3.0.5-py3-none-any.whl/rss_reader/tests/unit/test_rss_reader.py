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
                <pubDate>2022-04-10</pubDate>
                <image>
                    <title>Feed image title</title>
                    <link>Feed image link</link>
                    <url>Feed image url</url>
                </image>
                <item>
                    <title>Item 1 title</title>
                    <link>Item 1 link</link>
                    
                </item>
                <item>
                    <title>Item 2 title</title>
                    <link>Item 2 link</link>
                    <pubDate>2022-04-10</pubDate>
                    
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
        """ Class that acts as mock object """

        def __init__(self, rss):
            self.content = rss

    def mock_get(*args, **kwargs):
        """ Function that returns mock object when requests.get method called """

        return MockResponse(rss_example)

    monkeypatch.setattr(requests, 'get', mock_get)
    reader = set_parser
    reader.get_news()
    assert len(reader.news) == 2
    news_1 = reader.news[0]
    assert news_1['title'] == 'Item 1 title'
    assert news_1['link'] == 'Item 1 link'
    assert news_1['pubDate'] == 'No info'
    news_2 = reader.news[1]
    assert news_2['title'] == 'Item 2 title'
    assert news_2['link'] == 'Item 2 link'
    assert news_2['pubDate'] == '2022-04-10'
