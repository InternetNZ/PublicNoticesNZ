#!/usr/bin/env python


import urllib, time, os
import boto3
from botocore.exceptions import ClientError


# Initialize the list of desired feeds
# Feed(Name, XML, Media, Hashtags)

FEEDS = [    [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=aw&rss=1', '', '#liquidations #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=aa&rss=1', '', '#appointmentreleaseofadministrators #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=al&rss=1', '', '#appointmentreleaseofliquidators #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ar&rss=1', '', '#appointmentreleaseofrecieversmanagers #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ba&rss=1', '', '#bankrupcy #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=cb&rss=1', '', '#cessation #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ct&rss=1', '', '#charitabletrusts #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=fs&rss=1', '', '#FriendlySocietiesCreditUnions #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=gn&rss=1', '', '#GeneralNotices #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=is&rss=1', '', '#IncorporatedSocieties #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=lt&rss=1', '', '#LandTransfers #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=md&rss=1', '', '#MeetingLastDates #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ot&rss=1', '', '#Other #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=pn&rss=1', '', '#Partnerships #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ds&rss=1', '', '#Removals #commercial #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=au&rss=1', '', '#Authorities #Government #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=dl&rss=1', '', '#DelegatedLegislation #Government #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=go&rss=1', '', '#Departmental #Government #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=gs&rss=1', '', '#General #Government #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ln&rss=1', '', '#LandNotices #Government #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=ps&rss=1', '', '#Parliamentary #Government #OpenGovt #gazetteNZ'],
	      [ 'New Zealand Gazette', 'https://gazette.govt.nz/home/NoticeSearch?noticeType=vr&rss=1', '', '#ViceRegal #Government #OpenGovt #gazetteNZ'],
	         ]




def lambda_handler(event, context):

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='NZGFeedsQueue')

for feed in FEEDS:
    # Create a new message
    body = feed[1]
    attributes =  {
                        'tags': {
                            'StringValue': feed[3],
                            'DataType': 'String'
                        }
                    }

#    print(body)
#    print(attributes)

    response = queue.send_message(MessageBody=body,MessageAttributes=attributes)

    # The response is NOT a resource, but gives you a message ID and MD5
#    print(response.get('MessageId'))
#    print(response.get('MD5OfMessageBody'))
