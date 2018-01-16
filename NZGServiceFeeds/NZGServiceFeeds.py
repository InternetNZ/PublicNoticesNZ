#!/usr/bin/env python

#from feed import Feed
from bs4 import BeautifulSoup
import tweepy, feedparser, urllib, sqlite3, time, os, json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError



DATABASE = '../database/rss_entries.db'

# Initialize the list of desired feeds
# Feed(Name, XML, Media, Hashtags)



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
    sqs = boto3.resource('sqs')
    snsmessage = {"alert": "TweetInQueue"}
    snsclient = boto3.client('sns')

    # Get the queue
 #   feedqueue = sqs.get_queue_by_name(QueueName='NZGFeedsQueue')




    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('NZGazTweet')



#    feed = feedqueue.receive_messages()
#    if (len(feed) ==0):
#        print("No messages available from queue ")
#        return

#    url = feed[0].body
    url = payload
    print("Feed from SQS: "+url)




    parsed_feed = feedparser.parse(url)

    for entry in parsed_feed.entries:



        try:
            response = table.get_item(
                Key={
                    'url': entry.link,
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

        if not 'Item' in response:
            data = (entry.link, entry.title, entry.description, time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed))

            #hashtag_length = len(feed.get_hashtag())
            #body_length = TWEET_NET_LENGTH - hashtag_length

#            tweet_body = entry.title.encode('utf-8')
#                tweet_desc = entry.description.encode('utf-8')[:body_length]
#            tweet_url = entry.link.encode('utf-8')
#            tweet_hashtag = feed.get_hashtag()
#            tweet_text = "%s %s" % (tweet_body, tweet_url)
#            tweet_media = media(feed, entry)

#            if tweet_media is not None:
#                api.update_with_media(tweet_media, tweet_text)
#            else:
#                api.update_status(tweet_text)
            print("New Entry"+entry.link)
#            print ( " ", time.strftime("%c"), "-", tweet_text )

            # Get the queue
            #tweetqueue = sqs.get_queue_by_name(QueueName='NZGTweetQueue')


            body = str(entry.link)
            attributes =  {
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
                                    'StringValue': str('#testing'),
                                    'DataType': 'String'
                                },
                                'dateAdded': {
                                    'StringValue': str(time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed)),
                                    'DataType': 'String'
                                },
                            }


            snsmessage = json.dumps({'servicename': 'NZGServiceFeeds', 'payload': attributes})
            print(snsmessage)
            snsresponse = snsclient.publish(
                TargetArn='arn:aws:sns:ap-southeast-2:435562053273:NewTweetOnQueue',
                Message=snsmessage
            )
            print(snsresponse)

            #tweetresponse = tweetqueue.send_message(MessageBody=body,MessageAttributes=attributes)

            # table.put_item(
            #     Item={
            #         'url': entry.link,
            #         'title': entry.title,
            #         'desc': entry.description,
            #         'dateAdded': time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed),
            #     }
            # )



def lambda_handler(event, context):

    event = json.loads(event['Records'][0]['Sns']['Message'])
    servicename = event['servicename']
    payload = event['payload']
    post_tweet(payload)
