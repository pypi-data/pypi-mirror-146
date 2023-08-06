import json


class RssDisplayer:
    """ Class that gives functionality to display news in a special format """

    def __init__(self):
        self.DISPLAY_FORMAT = '\n\t\tTitle:\t\t\t\t{title}\n\t\tPublished at:\t\t\t{pubDate}' \
                              '\n\t\tLink:\t\t\t\t{link}\n\t\tImage:\t\t\t\t{image}\n\t\t' \
                              'Description:\t\t\t{description}\n{hyphen}'

    def display_news(self, feed_info):
        """ Displays news in stdout"""
        if type(feed_info) == dict:
            entries = feed_info.pop('news_list')
            print('\t\t\t\tFeed')
            print('-' * 100)
            print(self.DISPLAY_FORMAT.format(hyphen='-' * 100, **feed_info))

            print('\t\t\t\tNews\n', f'{"-" * 100}')
            for entry in entries:
                print(self.DISPLAY_FORMAT.format(hyphen='-' * 100, **entry))
        else:
            for feed, entries in feed_info:
                print('\t\t\t\tFeed')
                print('-' * 100)
                print(self.DISPLAY_FORMAT.format(hyphen='-' * 100, **feed))

                print('\t\t\t\tCached News\n', f'{"-" * 100}')
                for entry in entries:
                    print(self.DISPLAY_FORMAT.format(hyphen='-' * 100, **entry))

    @staticmethod
    def display_news_json(feed_info):
        """ Displays news in stdout in json format """

        if type(feed_info) == dict:
            data = json.dumps(feed_info, indent=4)
            print(data)
        else:
            for feed, entries in feed_info:
                feed_copy = feed.copy()
                feed_copy.pop('news_list')
                feed_copy['cached_news'] = entries
                data = json.dumps(feed_copy, indent=4)
                print(data)
