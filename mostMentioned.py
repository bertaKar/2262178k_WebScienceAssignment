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


mostMentioned = {}



##Loop through the collection and check which users were mentioned most frequently

for item in collection.find():
    itemMentions = item["userMentions"]
    for mention in itemMentions:
        if mention not in mostMentioned:
            frequency = 0
            for item2 in collection.find():
                item2Mentions = item2["userMentions"]
                for mention2 in item2Mentions:
                    if mention == mention2:
                        frequency = frequency + 1
            mostMentioned[mention] = frequency


##Print to file
with open("mostMentioned.txt", "w") as text_file:
    for key, value in mostMentioned.items():
        string = key + " " + str(value)
        print(string, file=text_file)
