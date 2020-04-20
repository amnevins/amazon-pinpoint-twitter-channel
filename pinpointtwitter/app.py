from time import sleep
import boto3, json, os, uuid, logging, random, string, re

import twitter

token = os.environ['TOKEN']
tokenSecret = os.environ['TOKEN_SECRET']
consumerKey = os.environ['CONSUMER_KEY']
consumerSecret = os.environ['CONSUMER_SECRET']

twitter_api = twitter.Api(consumer_key=consumerKey,
                      consumer_secret=consumerSecret,
                      access_token_key=token,
                      access_token_secret=tokenSecret)

# This function can be used within an Amazon Pinpoint Campaign or Amazon Pinpoint Journey.
# When invoked by the Amazon Pinpoint service the code below will utilize the DirectMessage API of Twitter to send a user a private twitter message.

def lambda_handler(event, context):

    print(event)
    # print the payload the Lambda was invoked with

    if 'Endpoints' not in event:
        return "Function invoked without endpoints."
    # A valid invocation of this channel by the Pinpoint Service will include Endpoints in the event payload

    endpoints = event['Endpoints']

    for endpoint_id in endpoints:

        endpoint_profile = endpoints[endpoint_id]
        # the endpoint profile contains the entire endpoint definition.
        # Attributes and UserAttributes can be interpolated into your message for personalization.

        address = int(endpoints[endpoint_id]['Address'])
        # address is expected to be a Twitter userid e.g. 1251680867954462721 which is a numeric value but stored in Pinpoint as a string.

        message = "Hello World!  -Pinpoint Twitter Channel"
        # construct your message here.  You have access to the endpoint profile to personalize the message with Attributes.
        # e.g. message = "Hello {name}!  -Pinpoint Twitter Channel".format(name=endpoint_profile["Attributes"]["FirstName"])

        print(endpoint_id)
        print(endpoint_profile)
        print(address)
        print(message)

        try:
            # Twitter Direct Message docs - https://developer.twitter.com/en/docs/direct-messages/sending-and-receiving/api-reference/new-event
            # Note: In order for a user to receive a direct message they must have a conversation history with your application or allow direct messages.
            result = twitter_api.PostDirectMessage(text=message, user_id=endpoint_id, return_json=True)
            print(result)

            # To utilize other Twitter APIs here see Twitters API documentation - https://developer.twitter.com/en/docs/basics/getting-started

        except Exception as e:
            print(e)
            # see a list of exceptions returned from the api here - https://developer.twitter.com/en/docs/basics/response-codes
            print("Error trying to send a Twitter message")

        sleep(1)
        # Sleep 1 second between calls to avoid rate limiting

    print("Complete")
    return "Complete"
