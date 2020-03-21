import tweepy
import pymongo
from pymongo import MongoClient
import dns
from pymongo.errors import ConnectionFailure


try:
    ##connecting to the database
    client = MongoClient("mongodb://bertaKar:bertaKarpwd@127.0.0.1:27017")
    db = client["CoronaDB"]
    collection = db["CoronaTweets"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            hashtagsToStore = []
            userMentions = []

            ##Check if the tweet is extended and if so retrieve the data from "extended_tweet" entity if not then retrieve data regular tweet
            if status.truncated == True:
                tweet = {'_id': status.id, 'text': status.extended_tweet["full_text"], 'created_at': status.created_at, 'username': status.author.screen_name, 'author_id': status.author.id}
                extended_entities = status.extended_tweet["entities"]
                hashtags = extended_entities["hashtags"]
                user_mentions = extended_entities["user_mentions"]
            else:
                tweet = {'_id': status.id, 'text': status.text, 'created_at': status.created_at, 'username': status.author.screen_name, 'author_id': status.author.id}
                hashtags = status.entities["hashtags"]
                user_mentions = status.entities["user_mentions"]

            ## Check if tweet is a reply and store it appropriately
            if status.in_reply_to_screen_name:
                tweet["reply"] = True
                tweet["replyTo"] = status.in_reply_to_screen_name
            else:
                tweet["reply"] = False

            ## Check if tweet is a retweet and store it appropriately
            if hasattr(status, 'retweeted_status'):
                tweet["retweeted"] = True
                retweetStatus = status.retweeted_status
                originalTweeter = retweetStatus.user
                tweet["original_author"] = originalTweeter.screen_name
            else:
                tweet["retweeted"] = False


            ## Check if tweet is a quote and store it appropriately
            if hasattr(status, 'quoted_status'):
                tweet["quoted"] = True
                quotedStatus = status.quoted_status
                originalTweeter = quotedStatus.user
                tweet["original_author"] = originalTweeter.screen_name

            else:
                tweet["quoted"] = False


            ## Store the hashtags

            for tag in hashtags:
                hashtagsToStore.append(tag["text"])

            ## Store user mentions

            for mention in user_mentions:
                userMentions.append(mention["screen_name"])

            tweet["hashtags"] = hashtagsToStore
            tweet["userMentions"] = userMentions

            ##Insert tweet into the database collection

            collection.insert_one(tweet)
        except pymongo.errors.DuplicateKeyError:
            pass

    def on_error(self, status_code):
        print(status_code)


## tweepy authorisation

auth = tweepy.OAuthHandler('kqjc5TSwIvwM3pk0eLQx5qHP4', 'iKL4xesvaqjQqlbxRxuulhf7KWoCXIeQMKrbu9X9XFzpJwloTw')

access_key = '1560674708-yV09daJp2h3JgpYQJ6t2gMkAAor01UFfIg8y8KJ'
access_secret = 'lj2NHgtcX11svQaF3SuWJV6Z8eWGY3PCeNcnSSjiOIfor'

auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

## Initialise the streamer

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

## Run the streamer on the keyword "Corona"

myStream.filter(track=['Corona'], is_async=True)
