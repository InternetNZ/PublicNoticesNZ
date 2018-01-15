# NZ Gazette Tweeter / Public Notices

Applies [feedr](https://github.com/housed/feedr) to generate a Twitter feed of notices from the NZ Gazette, which is where the NZ Government officially announces things.

Currently works to get feeds, but is likely to dump lots of tweets at once in a way that we might not want.

# 15/01/2018 - giving each category a different Tweet template
Gazette categories sometimes have the useful information in the title, and other times it's in the description. This info below will try to determine which is which. 

| Code   | Category   | Attribute | T=0 D= 1 3= ambiguous|
|-------|-------------|---------------------|------|
|aa| Appointment-Release of Administrators| Title | 0 |
|gs |General Section| Title| 0|
|cb |Cessation of Business in New Zealand| Title|0|
|is |Incorporated Societies| Title| 3
|am |General Meetings| RETIRED | 4|
|al |Appointment-Release of Liquidators| Title |0 |
|vr |Vice Regal| Title| 0|
|ar |Appointment-Release of Receivers & Managers| Title| 0|
|au |Authorities-Other Agencies of State| Useless| 3|
|aw |Applications for Winding up-Liquidations| Description|1 |
|vw |Winding up-Liquidations| RETIRED| 4|
|go |Departmental| Title| 3|
|gn |General Notices| Description| 1|
|cu |Customs| RETIRED| 4|
|ct |Charitable Trusts| Title | 3 | Note that this is a tricky one, but too much info is in desc to be useful. 
|ps |Parliamentary| Title| 0|
|rs |Regulation Summary| RETIRED| 4|
|ln |Land Notices| Title| 0|
|pb |Private Bills| Title| 0|
|lt |Land Transfers-Joint Family Homes| completely useless, too much text| na|
|pn |Partnerships| Title| 0|
|dl |Delegated Legislation| Description| 1|
|fs |Friendly Societies and Credit Unions| Description|3| Note: this is not consistent
|ba |Bankruptcies| Description| 1|
|ds |Removals| Title| 0|
|md |Meetings-Last Dates for Debts & Claims| Title| 0|
|ot |Other| Description| 1|

On attributes:
0: Clear use of title attribute
1: clear use of dexcription attribute
3: need this to be QA'd as uncertain
4: Retired category no longer in use, ignore from project. 

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
