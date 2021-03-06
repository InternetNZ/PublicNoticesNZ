# NZ Gazette Tweeter / Public Notices

Applies [feedr](https://github.com/housed/feedr) to generate a Twitter feed of notices from the [NZ Gazette](https://gazette.govt.nz/), which is where the NZ Government officially announces things.

Currently works to get feeds, but is likely to dump lots of tweets at once in a way that we might not want.

## Gazette copyright and terms of use

All Gazette content, including the rss feeds we draw from, is [copyright](https://gazette.govt.nz/footer/copyright/) Department of Internal Affairs, CC-BY 3.0 NZ.

The open [terms of use](https://gazette.govt.nz/footer/terms-of-use/), and CC-BY copyright, are a great example of New Zealand's Government making information available for use under the [NZGOAL framework](https://www.ict.govt.nz/guidance-and-resources/open-government/new-zealand-government-open-access-and-licensing-nzgoal-framework/).

We thank the Department of Internal Affairs, and the New Zealand Government for moving to open up information like the NZ Gazette!

# Feedr project self-description:

feedr will read RSS feeds that you specify and then it will determine if there's new content since last checked. If there is, then it will publish a post on your Twitter account on your behalf for each new content update.

As is, feedr will add the following information to a tweet:
* Title of the new content entry
* URL to the new content entry
* Relevant hashtag(s)
* Relevant image

Here's [an example of feedr in action](https://twitter.com/ValveTime/status/552918907053674496)...

![Feedr tweet example](https://raw.githubusercontent.com/housed/feedr/master/doc/img/example_tweet.png)

## Required Packages ##

* [Python 2.7](https://www.python.org/downloads/)
* [Tweepy 3.1.0](http://www.tweepy.org/)
* [feedparser 5.1.3](https://pypi.python.org/pypi/feedparser)
* [beautifulsoup4 4.4.1](http://www.crummy.com/software/BeautifulSoup/)

## Getting Started is Easy ##

Instructions for getting started with feedr can be found on [the Wiki](https://www.github.com/housed/feedr/wiki/Getting-Started-with-feedr).

Follow me on Twitter [@TheDylanHouse](https://www.twitter.com/TheDylanHouse).


## Make Lambda Packages
```
make-lambda-package  --repo-source-files "*.py"  --requirements-file ./requirements.txt .
```
