#!/usr/bin/env python

from feed import Feed
from bs4 import BeautifulSoup
import tweepy, urllib,  os, json

# Twitter Account Keys
# Separate keys.py file holds secrets
from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

# Initialize the list of desired feeds
# Feed(Name, XML, Media, Hashtags)

# Define the net max length of the text portion of a tweet
TWEET_MAX_LENGTH = 280
TWEET_URL_LENGTH = 22
TWEET_IMG_LENGTH = 23
TWEET_NET_LENGTH = TWEET_MAX_LENGTH - TWEET_URL_LENGTH


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
                    media_ext = os.path.splitext(img_url)[1][0:4]  # e.g. .png?v=2 becomes just .png # TODO check againt .jpeg and other ext > 3
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


def post_tweet(payload):

    api = init_twitter()

    data_added = payload['dateAdded']['StringValue']
    url = payload['url']['StringValue']
    title = payload['title']['StringValue']
    description = payload['description']['StringValue']
    hashtags = payload['hashtags']['StringValue']

    hashtag_length = len(hashtags)
    title_length = len(title)
    body_length = TWEET_NET_LENGTH - title_length - hashtag_length

    tweet_desc = description[:body_length]
    tweet_text = "%s %s %s" % (title, url, hashtags)

    api.update_status(tweet_text)
    print("New Entry: "+tweet_text)


def lambda_handler(event, context):

    event = json.loads(event['Records'][0]['Sns']['Message'])
    servicename = event['servicename']
    payload = event['payload']
    post_tweet(payload)
