import tweepy
import pymongo
from pymongo import MongoClient
import dns
from pymongo.errors import ConnectionFailure


try:

    ##connecting to the database

    client = MongoClient("mongodb://bertaKar:bertaKarpwd@127.0.0.1:27017")
    db = client["bertaDB"]
    collection = db["REAL"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

## tweepy authorisation

auth = tweepy.OAuthHandler('kqjc5TSwIvwM3pk0eLQx5qHP4', 'iKL4xesvaqjQqlbxRxuulhf7KWoCXIeQMKrbu9X9XFzpJwloTw')

access_key = '1560674708-yV09daJp2h3JgpYQJ6t2gMkAAor01UFfIg8y8KJ'
access_secret = 'lj2NHgtcX11svQaF3SuWJV6Z8eWGY3PCeNcnSSjiOIfor'

auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

##Retrieve tweets from three top most mentioned users

for status in tweepy.Cursor(api.user_timeline, id="Jabinbotsford").items(50):
    try:

        hashtagsToStore = []
        userMentions = []

        tweet = {'_id': status.id, 'text': status.text, 'created_at': status.created_at, 'username': status.author.screen_name, 'author_id': status.author.id}
        hashtags = status.entities["hashtags"]
        user_mentions = status.entities["user_mentions"]

        if status.in_reply_to_screen_name:
            tweet["reply"] = True
            tweet["replyTo"] = status.in_reply_to_screen_name
        else:
            tweet["reply"] = False

        if hasattr(status, 'retweeted_status'):
            tweet["retweeted"] = True
            retweetStatus = status.retweeted_status
            originalTweeter = retweetStatus.user
            tweet["original_author"] = originalTweeter.screen_name
        else:
            tweet["retweeted"] = False

        if hasattr(status, 'quoted_status'):
            tweet["quoted"] = True
            quotedStatus = status.quoted_status
            originalTweeter = quotedStatus.user
            tweet["original_author"] = originalTweeter.screen_name

        else:
            tweet["quoted"] = False

        for tag in hashtags:
            hashtagsToStore.append(tag["text"])

        for mention in user_mentions:
            userMentions.append(mention["screen_name"])

        tweet["hashtags"] = hashtagsToStore
        tweet["userMentions"] = userMentions

        collection.insert_one(tweet)
    except pymongo.errors.DuplicateKeyError:
        pass

for status in tweepy.Cursor(api.user_timeline, id="realdonaldtrump").items(50):

    try:
        hashtagsToStore = []
        userMentions = []

        tweet = {'_id': status.id, 'text': status.text, 'created_at': status.created_at, 'username': status.author.screen_name, 'author_id': status.author.id}
        hashtags = status.entities["hashtags"]
        user_mentions = status.entities["user_mentions"]


        if status.in_reply_to_screen_name:
            tweet["reply"] = True
            tweet["replyTo"] = status.in_reply_to_screen_name
        else:
            tweet["reply"] = False

        if hasattr(status, 'retweeted_status'):
            tweet["retweeted"] = True
            retweetStatus = status.retweeted_status
            originalTweeter = retweetStatus.user
            tweet["original_author"] = originalTweeter.screen_name
        else:
            tweet["retweeted"] = False

        if hasattr(status, 'quoted_status'):
            tweet["quoted"] = True
            quotedStatus = status.quoted_status
            originalTweeter = quotedStatus.user
            tweet["original_author"] = originalTweeter.screen_name

        else:
            tweet["quoted"] = False

        for tag in hashtags:
            hashtagsToStore.append(tag["text"])

        for mention in user_mentions:
            userMentions.append(mention["screen_name"])

        tweet["hashtags"] = hashtagsToStore
        tweet["userMentions"] = userMentions

        collection.insert_one(tweet)
    except pymongo.errors.DuplicateKeyError:
        pass

for status in tweepy.Cursor(api.user_timeline, id="Jbarro").items(50):
    try:
        hashtagsToStore = []
        userMentions = []

        tweet = {'_id': status.id, 'text': status.text, 'created_at': status.created_at, 'username': status.author.screen_name, 'author_id': status.author.id}
        hashtags = status.entities["hashtags"]
        user_mentions = status.entities["user_mentions"]

        if status.in_reply_to_screen_name:
            tweet["reply"] = True
            tweet["replyTo"] = status.in_reply_to_screen_name
        else:
            tweet["reply"] = False

        if hasattr(status, 'retweeted_status'):
            tweet["retweeted"] = True
            retweetStatus = status.retweeted_status
            originalTweeter = retweetStatus.user
            tweet["original_author"] = originalTweeter.screen_name
        else:
            tweet["retweeted"] = False

        if hasattr(status, 'quoted_status'):
            tweet["quoted"] = True
            quotedStatus = status.quoted_status
            originalTweeter = quotedStatus.user
            tweet["original_author"] = originalTweeter.screen_name

        else:
            tweet["quoted"] = False

        for tag in hashtags:
            hashtagsToStore.append(tag["text"])

        for mention in user_mentions:
            userMentions.append(mention["screen_name"])

        tweet["hashtags"] = hashtagsToStore
        tweet["userMentions"] = userMentions

        collection.insert_one(tweet)
    except pymongo.errors.DuplicateKeyError:
        pass
