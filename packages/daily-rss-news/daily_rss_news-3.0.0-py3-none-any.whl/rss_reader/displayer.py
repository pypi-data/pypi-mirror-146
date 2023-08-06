import json


class RssDisplayer:
    """ Class that gives functionality to display news in a special format """

    def __init__(self):
        self.DISPLAY_FORMAT = '\n\t\tTitle:\t\t\t{title}\n\t\tPublished at:\t\t{pubDate}' \
                              '\n\t\tLink:\t\t\t{link}\n\t\tDesc:\t\t\t{description}\n\t\tImage:\t\t\t{image}' \
                              '\n\t\tSource:\t\t\t{source}\n{hyphen}'

    def display_news(self, entries):
        """ Displays news in stdout"""

        print('\t\t\t\tNews\n', f'{"-" * 100}')
        for entry in entries:
            print(self.DISPLAY_FORMAT.format(hyphen='-' * 100, **entry))

    @staticmethod
    def display_news_json(entries):
        """ Displays news in stdout in json format """

        data = json.dumps(entries, indent=4)
        print(data)
