import datetime
import os
import shelve
from dateutil.parser import parse as dateutil_parser


class NotCachedError(Exception):
    """ Raise when given source is not cached yet but --date option is given with source """
    pass


class NoNewsError(Exception):
    """ Raise when there is no news in a given date and source """
    pass


class CacheDB:
    """ Class that caches news  """

    def __init__(self, source=None):
        self.db = os.path.join(os.path.expanduser('~'), 'cache.db')
        self.source = source

    def save(self, news):
        with shelve.open(self.db, writeback=True) as db:
            date = news['pubDate']
            news['pubDate'] = date if date == 'No info' else dateutil_parser(date).strftime('%Y%m%d')
            if self.source in db:
                temp = db[self.source]
                temp.append(str(news))
                db[self.source] = temp
            else:
                db[self.source] = []
                temp = db[self.source]
                temp.append(str(news))
                db[self.source] = temp

    def get(self, date, limit):
        if self.source:
            with shelve.open(self.db) as db:
                try:
                    news_list = db[self.source]
                except KeyError:
                    msg = f'News from source {self.source} are not cached yet'
                    raise NotCachedError(msg)

                filtered_news = []
                for news in news_list:
                    news = eval(news)
                    if news['pubDate'] == date.strftime('%Y%m%d'):
                        date_obj = datetime.datetime.strptime(news['pubDate'], '%Y%M%d')
                        news['pubDate'] = date_obj.strftime('%d %b, %Y ')
                        filtered_news.append(news)
                if len(filtered_news) == 0:
                    raise NoNewsError
                else:
                    return filtered_news[:limit]
        else:
            db = shelve.open(self.db)
            all_sources = db.keys()
            filtered_news = []
            for source in all_sources:
                for news in db[source]:
                    news = eval(news)
                    if news['pubDate'] == date.strftime('%Y%m%d'):
                        filtered_news.append(news)

            if len(filtered_news) == 0:
                raise NoNewsError
            else:
                return filtered_news[:limit]

    def clear(self):
        with shelve.open(self.db) as db:
            db.clear()
            print('Cached news was removed')




