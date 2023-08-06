# Python RSS Reader
Final task for EPAM Python Training 2022.04.29
# Installation
To install this package type 

```shell
$ pip install daily-rss-news
```

If you do not want to install it , you can source code from gitlab

```shell
$ git clone https://gitlab.com/Ilhom_Xusanov/RSS-parser.git
```

## Requirements
This program depends on some third party packages.
If you downloaded it from gitlab, first create virtual environment 
and go to the folder where requirements.txt resides and type
 
```shell
$ pip install -r requirements.txt
```
This will install all packages to run this program.

# Usage
If you installed this packages by pip, you can use it everywhere
by typing
```shell
$ rss-reader [options]
```
or

```shell
$ python -m rss_reader [options]
```


If you downloaded from gitlab, go to root folder where rss_reader.py is,
and you can run python with rss_reader.py module.
#### Note
if you are in different folder specify full path to rss_reader.py to run with python

```shell
$ python rss_reader.py [options]
```

To see help message type
```shell
$ rss-reader -h
```
or
```shell
$ python rss_reader.py -h 
```
output is:
```shell
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
  --date []   Published date of news in format YYYYMMDD
  --clear-cache  Clears all news from cache

```
If --version option is given, program prints its version to console and exits.

If --verbose option is given, outputs logs in a INFO level, default is WARNING

if --limit(N) option is given, N number of news, else all news is returned

if --date option is provided with date in format YYYYMMDD , then news published that date will be returned

if -- date option is provided with given source , then only news published in a given date from that source will be returned

if --json option is provided, program displays news to console in json format

--json output example:
```shell
[
    {
        "title": "China makes semi-secret delivery of missiles to Serbia",
        "pubDate": "2022-04-10T13:38:01Z",
        "link": "https://news.yahoo.com/china-makes-semi-secret-delivery-133801459.html",
        "description": "No info",
        "image": "No info",
        "source": "https://news.yahoo.com/rss/"
    },
    {
        "title": "Chris Rock said he won't speak on controversial Oscars slap 'until I get paid,' report says",
        "pubDate": "2022-04-09T19:50:31Z",
        "link": "https://news.yahoo.com/chris-rock-said-wont-speak-195031643.html",
        "description": "No info",
        "image": "No info",
        "source": "https://news.yahoo.com/rss/"
    }
]
```
## Caching
Retrieved news are cached. Cached file is in home directory called 'cache.db'.
Caching technique is accomplished via shelve library. To get news from cache internet connection is not required.
Each source is the key of shelve file 'cache.db'. Its value is list of news.

Cache is going to grow in size continuously when you read news from rss sources.
To clear cache type 
```shell
$ python -m rss_reader --clear-cache
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

**Test coverage is 79%**

To run tests go to root folder of program and type:
```shell
$ python -m pytest 
```
to run tests in a specific module type:
```shell
$ python -m pytest 'folder/modulename'
```

to check test coverage run :
```shell
$ python -m pytest --cov=rss_reader/ 
```

