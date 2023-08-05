# Python RSS Reader
Final task for EPAM Python Training 2022.04.29

## Requirements
This program depends on some third party packages.
To use this program, first create virtual environment and go to the folder where requirements.txt reside and type
 
```shell
$ pip install -r requirements.txt
```
This will install all packages to run this program.

##Usage
To see usage of program, use -h option
```shell
$ python rss_reader.py -h                                                                                                                                                                                                                                       ─╯
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit ] source

Pure Python command-line RSS reader

positional arguments:
  source      RSS URL

optional arguments:
  -h, --help  show this help message and exit
  --version   Print version info
  --json      Print result as JSON in stdout
  --verbose   Outputs verbose status messages
  --limit []  Limit news topics if this parameter provided

```
If --version option is given, program prints its version to console and exits.

If --verbose option is given, outputs logs in a INFO level, default is WARNING

if --limit(N) option is given, N number of news, else all news is returned

if --json option is provided, program displays news to console in json format

--json output example:
```shell
{
    "title": "NYT > Top Stories",
    "pubDate": "Wed, 06 Apr 2022 10:13:52 +0000",
    "link": "https://www.nytimes.com",
    "description": null,
    "image": {
        "title": "NYT > Top Stories",
        "link": "https://www.nytimes.com",
        "url": "https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png"
    },
    "news": [
        {
            "title": "At Least 200 Feared Dead in Apartments Hit by Russia, Officials Say",
            "pubDate": "Tue, 05 Apr 2022 21:46:03 +0000",
            "link": "https://www.nytimes.com/2022/04/05/world/asia/ukraine-civilians-russia-borodyanka.html",
            "description": "After Russian forces withdrew from Borodyanka, a commuter town near Ukraine\u2019s capital, families are searching the rubble for bodies.",
            "image": "No info"
        },
        {
            "title": "Why Tracking Putin\u2019s Wealth Is So Difficult",
            "pubDate": "Wed, 06 Apr 2022 07:00:12 +0000",
            "link": "https://www.nytimes.com/2022/04/06/world/putin-russia-assets-wealth-sanctions.html",
            "description": "Amid speculation that oligarchs are holding cash and luxury assets for the Russian president, many of his extravagances can be traced elsewhere: the Russian state.",
            "image": "No info"
        }
    ]
}

```
## Tested Rss links
1.[http://feeds.wired.com/wired/index](http://feeds.wired.com/wired/index)
2.[http://feeds.nytimes.com/nyt/rss/Technology](http://feeds.nytimes.com/nyt/rss/Technology)
3.[http://feeds.nature.com/nature/rss/current](http://feeds.nature.com/nature/rss/current)
4.[http://newsrss.bbc.co.uk/rss/newsonline_world_edition/americas/rss.xml](http://newsrss.bbc.co.uk/rss/newsonline_world_edition/americas/rss.xml)
5.[http://feeds.nytimes.com/nyt/rss/HomePage](http://feeds.nytimes.com/nyt/rss/HomePage)
6.[https://news.yahoo.com/rss/](https://news.yahoo.com/rss/)
7.[http://www.nba.com/jazz/rss.xml](http://www.nba.com/jazz/rss.xml)
8.[http://feeds1.nytimes.com/nyt/rss/Sports](http://feeds1.nytimes.com/nyt/rss/Sports)
9.[http://rss.cnn.com/rss/edition.rss](http://rss.cnn.com/rss/edition.rss)

## Testing
Tested modules
   1. log.py
   2. rss_reader.py
   3. arg_parser.py

**Test coverage is 86 %**

To run tests go to root folder of program and type:
```shell
$ pytest 
```
to run tests in a specific module type:
```shell
$ pytest 'folder/modulename'
```

to check test coverage run :
```shell
$ coverage run -m pytest 
```
and
```shell
$ coverage report -m 
```
