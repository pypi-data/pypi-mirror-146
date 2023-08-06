import datetime

import pytest

from ..caching import CacheDB, NoNewsError, NotCachedError


news_example = {
    'title': 'Some title',
    'link': 'Some link',
    'description': 'Some description',
    'pubDate': '2022-04-10',
    'image': 'Some image'
}

source = 'Some source'


def test_cache_source():
    cache = CacheDB(source)
    cache.save(news_example.copy())
    date = datetime.datetime.strptime(news_example['pubDate'], '%Y-%m-%d')
    news = cache.get(date, 1)
    assert len(news) == 1
    date = datetime.datetime.strptime('2025-06-12', '%Y-%m-%d')
    with pytest.raises(NoNewsError):
        news = cache.get(date, 1)
    with pytest.raises(NotCachedError):
        cache = CacheDB('not cached source')
        cache.get(date, 1)
