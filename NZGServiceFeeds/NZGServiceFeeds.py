#!/usr/bin/env python

#from feed import Feed
from bs4 import BeautifulSoup
import tweepy, feedparser, urllib, sqlite3, time, os, json
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError





# Define the net max length of the text portion of a tweet
TWEET_MAX_LENGTH = 280
TWEET_URL_LENGTH = 22
TWEET_IMG_LENGTH = 23
TWEET_NET_LENGTH = TWEET_MAX_LENGTH - TWEET_URL_LENGTH - TWEET_IMG_LENGTH



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


def post_tweet(payload):

    # Get the service resource
    snsmessage = {"alert": "TweetInQueue"}
    snsclient = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('NZGazTweet')

    url = payload['url']['StringValue']
    print("Feed from SQS: "+url)

    parsed_feed = feedparser.parse(url)

    for entry in parsed_feed.entries:

        gazTime = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed), "%Y-%m-%d %H:%M:%S")

        if datetime.now() - gazTime < timedelta(days=1):
            print("Got Tweet within 24 hours of now: %s" % time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed))
            try:
                response = table.get_item(
                    Key={
                        'url': entry.link,
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])

            if 'Item' not in response:
    #            data = (entry.link, entry.title, entry.description, time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed))

                print("New Entry: "+entry.link)
                table.put_item(
                    Item={
                        'url': entry.link,
                        'title': entry.title,
                        'desc': entry.description,
                        'dateAdded': time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed),
                    }
                )
                attributes = {
                                    'title': {
                                        'StringValue': str(entry.title),
                                        'DataType': 'String'
                                    },
                                    'url': {
                                        'StringValue': str(entry.link),
                                        'DataType': 'String'
                                    },
                                    'description': {
                                        'StringValue': str(entry.description),
                                        'DataType': 'String'
                                    },
                                    'hashtags': {
                                        'StringValue': str(payload['tags']['StringValue']),
                                        'DataType': 'String'
                                    },
                                    'dateAdded': {
                                        'StringValue': str(time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed)),
                                        'DataType': 'String'
                                    },
                                }

                snsmessage = json.dumps({'servicename': 'NZGServiceFeeds', 'payload': attributes})
    #            print(snsmessage)
                snsresponse = snsclient.publish(
                    TargetArn='arn:aws:sns:ap-southeast-2:435562053273:NewTweetOnQueue',
                    Message=snsmessage
                )


def lambda_handler(event, context):

    event = json.loads(event['Records'][0]['Sns']['Message'])
    servicename = event['servicename']
    payload = event['payload']
    post_tweet(payload)
