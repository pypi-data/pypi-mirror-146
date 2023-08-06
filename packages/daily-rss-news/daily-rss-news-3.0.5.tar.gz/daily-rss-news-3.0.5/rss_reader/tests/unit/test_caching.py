import datetime

import pytest

from rss_reader.utils.caching import CacheDB, NoNewsError, NotCachedError


feed_example = {
    'title': 'Some title',
    'link': 'Some link',
    'description': 'Some description',
    'pubDate': '2022-04-10',
    'image': 'Some image'
}

news_example = {
    'title': 'news title',
    'link': 'news link',
    'description': 'news description',
    'pubDate': '2022-04-11',
    'image': 'No info'
}

source = 'Some source'


def test_cache_source():
    cache = CacheDB(source)
    cache.save(feed_example.copy())
    date = datetime.datetime.strptime(news_example['pubDate'], '%Y-%m-%d')
    with pytest.raises(NoNewsError):
        cache.get(date, 1)
    with pytest.raises(NotCachedError):
        cache = CacheDB('not cached source')
        cache.get(date, 1)
        cache.remove('not cached source')

    cache = CacheDB(source)
    cache.save(news_example.copy())
    date = datetime.datetime.strptime(news_example['pubDate'], '%Y-%m-%d')
    news_info = cache.get(date, None)
    feed, news = news_info[0]
    assert len(news) == 1
    print(news)
    cache.remove(source)
