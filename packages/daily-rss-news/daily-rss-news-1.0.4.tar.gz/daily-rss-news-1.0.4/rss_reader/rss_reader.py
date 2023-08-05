from bs4 import BeautifulSoup
import requests
import os.path
import sys; sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import log
import arg_parser
import displayer


class RssReader:
    """ Main class that gets news, parses it and runs as main the program """

    def __init__(self):
        self.news = []
        self.parser = arg_parser.ArgParser()
        self.format = displayer.RssDisplayer()
        self.system_log = log.SystemLog()

        if self.parser.cli_args.loglevel:
            self.system_log.set_level(self.parser.cli_args.loglevel)
        self.system_log.logger.info(f'Setting command line argument options : source = {self.parser.cli_args.source};'
                                    f' json = {self.parser.cli_args.json}; limit = {self.parser.cli_args.limit}')

    def parse_url(self):
        """ Accepts source and parses it"""

        res = requests.get(self.parser.cli_args.source, timeout=5)
        self.soup = BeautifulSoup(res.content, 'xml')
        self.feed = self.soup.find('channel')
        self.system_log.logger.info(f'Parsed given source {self.parser.cli_args.source}')

    def get_tag_string(self, entry, idx):
        """ Collects entry's tag string if there is, else marks it as no info """

        entry_info = {}
        # entry tags that should be displayed
        tags = ['title', 'pubDate', 'link', 'description', 'image']
        for tag in tags:
            try:
                if tag == 'image':
                    entry_info[tag] = {'title': entry.find(tag).title.string,
                                       'link': entry.find(tag).link.string,
                                       'url': entry.find(tag).url.string}
                else:
                    entry_info[tag] = entry.find(tag).string
            except AttributeError:
                entry_info[tag] = 'No info'
                self.system_log.logger.info(f'entry {idx + 1} has no {tag} tag')

        return entry_info

    def get_news(self):
        """ Return all news in a given source.
         If limit is set, then return news as the limit size """

        self.parse_url()
        entries = self.soup.find_all('item', limit=self.parser.cli_args.limit)

        for idx, entry in enumerate(entries):
            entry_info = self.get_tag_string(entry, idx)
            self.news.insert(idx, entry_info)

        self.system_log.logger.info(f'Returned {len(self.news)} news')

    def display(self):
        """ Display news in a given format """

        self.get_news()
        feed = self.get_tag_string(self.feed, 0)
        if self.parser.cli_args.json:
            self.format.display_news_json(feed=feed, entries=self.news)
        else:
            self.format.display_news(feed=feed, entries=self.news)


def main():
    rss_reader = RssReader()
    try:
        rss_reader.display()
    except requests.ConnectionError:
        print('Rss reader could not establish connection with server.'
              'Check your internet connection or try again a bit later!')


if __name__ == '__main__':
    main()
