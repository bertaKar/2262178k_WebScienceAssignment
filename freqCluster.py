import pymongo
from pymongo import MongoClient
import dns
from bson.json_util import dumps
import pandas as pd
from pandas import json_normalize
import time
import sklearn
from sklearn.cluster import MiniBatchKMeans, DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import hashlib
import numpy as np
import json
import os


try:
    ##Connect to the database
    client = MongoClient("mongodb://bertaKar:bertaKarpwd@127.0.0.1:27017")
    db = client["CoronaDB"]
    collection = db["CoronaTweets"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    # do whatever you needs
    print(err)



##Variable to store users that have already been checked
checked = []

## Loop through each cluster and count how many times every user has mentioned someone else and store it in the database

for i in range(5):
    checked = []
    collection_name = "GeneralCluster" + str(i)
    col = db[collection_name]
    for tweet in collection.find():
        if tweet["cluster"] == i:
            frequencies = {}
            user = tweet["username"]
            if user not in checked:
                checked.append(user)
                for tweet2 in collection.find():
                    if tweet2["username"] == user:
                        if tweet2["cluster"] == tweet["cluster"]:
                            mentions = tweet2["userMentions"]
                            for mention in mentions:
                                if mention in frequencies.keys():
                                    frequencies[mention] = frequencies.get(mention) + 1

                                else:
                                    frequencies[mention] = 1

                if frequencies:
                    item = {"_name": user, "frequencies": frequencies}
                    col.insert_one(item)


## Loop through each cluster and count how many times every user has retweeted someone else and store it in the database
for i in range(5):
    checked = []
    collection_name = "RetweetCluster" + str(i)
    col = db[collection_name]

    for tweet in collection.find():
        if tweet["cluster"] == i:
            frequencies = {}
            user = tweet["username"]
            if user not in checked:
                checked.append(user)
                for tweet2 in collection.find():
                    if tweet2["retweeted"] == True:
                        if tweet2["quoted"] == False:
                            if tweet2["username"] == user:
                                if tweet2["cluster"] == tweet["cluster"]:
                                    author = tweet2["original_author"]
                                    if author in frequencies.keys():
                                        frequencies[author] = frequencies.get(author) + 1

                                    else:
                                        frequencies[author] = 1

                if frequencies:
                    item = {"_name": user, "frequencies": frequencies}
                    col.insert_one(item)


## Loop through each cluster and count how many times every user has quoted or replied to someone else and store it in the database

for i in range(5):
    checked = []
    collection_name = "QuotedCluster" + str(i)
    col = db[collection_name]

    for tweet in collection.find():
        if tweet["cluster"] == i:
            frequencies = {}
            user = tweet["username"]
            if user not in checked:
                checked.append(user)
                for tweet2 in collection.find():
                    if tweet2["quoted"] == True:
                        if tweet2["retweeted"] == False:
                            if tweet2["username"] == user:
                                if tweet2["cluster"] == tweet["cluster"]:
                                    author = tweet2["original_author"]
                                    if author in frequencies.keys():
                                        frequencies[author] = frequencies.get(author) + 1

                                    else:
                                        frequencies[author] = 1

                    if tweet2["reply"] == True:
                        if tweet2["username"] == user:
                            if tweet2["cluster"] == tweet["cluster"]:
                                replyTo = tweet2["replyTo"]
                                if replyTo in frequencies.keys():
                                    frequencies[replyTo] = frequencies.get(replyTo) + 1

                                else:
                                    frequencies[replyTo] = 1

                if frequencies:
                    item = {"_name": user, "frequencies": frequencies}
                    col.insert_one(item)


## Loop through each cluster and check what hashtags appeared together and store it in the database

for i in range(5):
    checked = []
    collection_name = "HashtagsCluster" + str(i)
    col = db[collection_name]

    for tweet in collection.find():
        if tweet["cluster"] == i:
            hashtags = tweet["hashtags"]
            for tag in hashtags:
                frequencies = []
                if tag not in checked:
                    checked.append(tag)
                    for tweet2 in collection.find():
                        hashtags2 = tweet2["hashtags"]
                        if tag in hashtags2:
                            if tweet2["cluster"] == tweet["cluster"]:
                                for tag2 in hashtags2:
                                    if tag != tag2:
                                        if tag2 not in frequencies:
                                            frequencies.append(tag2)

                if frequencies:
                    item = {"_tag": tag, "frequencies": frequencies}
                    col.insert_one(item)
