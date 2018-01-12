#!/usr/bin/env python

from feed import Feed
from bs4 import BeautifulSoup
import tweepy, feedparser, urllib, sqlite3, time, os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import keys


#Separate keys.py file holds secrets
from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

DATABASE = '../database/rss_entries.db'

# Initialize the list of desired feeds
# Feed(Name, XML, Media, Hashtags)

FEEDS = [    Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=aw&rss=1', '', '#liquidations #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=aa&rss=1', '', '#appointmentreleaseofadministrators #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=al&rss=1', '', '#appointmentreleaseofliquidators #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ar&rss=1', '', '#appointmentreleaseofrecieversmanagers #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ba&rss=1', '', '#bankrupcy #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=cb&rss=1', '', '#cessation #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ct&rss=1', '', '#charitabletrusts #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=fs&rss=1', '', '#FriendlySocietiesCreditUnions #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=gn&rss=1', '', '#GeneralNotices #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=is&rss=1', '', '#IncorporatedSocieties #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=lt&rss=1', '', '#LandTransfers #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=md&rss=1', '', '#MeetingLastDates #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ot&rss=1', '', '#Other #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=pn&rss=1', '', '#Partnerships #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ds&rss=1', '', '#Removals #commercial #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=au&rss=1', '', '#Authorities #Government #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=dl&rss=1', '', '#DelegatedLegislation #Government #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=go&rss=1', '', '#Departmental #Government #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=gs&rss=1', '', '#General #Government #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ln&rss=1', '', '#LandNotices #Government #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ps&rss=1', '', '#Parliamentary #Government #OpenGovt #gazetteNZ'),
	     # Feed('New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=vr&rss=1', '', '#ViceRegal #Government #OpenGovt #gazetteNZ'),
	         ]


# Define the net max length of the text portion of a tweet
TWEET_MAX_LENGTH = 280
TWEET_URL_LENGTH = 22
TWEET_IMG_LENGTH = 23
TWEET_NET_LENGTH = TWEET_MAX_LENGTH - TWEET_URL_LENGTH - TWEET_IMG_LENGTH

# Twitter Account Keys

def html_doc(entry):
        if hasattr(entry, 'content'):
                return entry.content[0].value
        elif hasattr(entry, 'description'):
                return entry.description
        else:
                return None

def img_src(soup):
        img = soup.find("img")
        if img is not None:
                return img["src"]
        else:
                return None

def media(feed, entry):
        doc = html_doc(entry)
        if doc is not None:
                soup = BeautifulSoup(doc, "html.parser")
                img_url = img_src(soup)
                if img_url is not None:
                    media_root = feed.get_media_root()
                    media_ext = os.path.splitext(img_url)[1][0:4] # e.g. .png?v=2 becomes just .png # TODO check againt .jpeg and other ext > 3
                    media_path = media_root + media_ext
                    urllib.urlretrieve(img_url, media_path)
                    return media_path
                else:
                        return None
        else:
                return None

def init_twitter():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	return api

def post_tweet(api):

    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('NZGazTweet')

    for feed in FEEDS:
        parsed_feed = feedparser.parse(feed.get_url())

        for entry in parsed_feed.entries:
            print(entry.link)


            try:
                response = table.get_item(
                    Key={
                        'url': entry.link,
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])

            if not 'Item' in response:
                data = (entry.link, entry.title, time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed))
                table.put_item(
                    Item={
                        'url': entry.link,
                        'title': entry.title,
                        'dateAdded': time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed),
                    }
                )
                hashtag_length = len(feed.get_hashtag())
                body_length = TWEET_NET_LENGTH - hashtag_length

                tweet_body = entry.title.encode('utf-8')[:body_length]
                tweet_url = entry.link.encode('utf-8')
                tweet_hashtag = feed.get_hashtag()
                tweet_text = "%s %s %s" % (tweet_body, tweet_url, tweet_hashtag)
                tweet_media = media(feed, entry)

#                if tweet_media is not None:
#                    api.update_with_media(tweet_media, tweet_text)
#                else:
#                    api.update_status(tweet_text)

                print ( " ", time.strftime("%c"), "-", tweet_text )

if __name__ == '__main__':
	api = init_twitter()
	post_tweet(api)
