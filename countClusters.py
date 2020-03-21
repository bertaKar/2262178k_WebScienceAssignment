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

    ## Connect to the database

    client = MongoClient("mongodb://bertaKar:bertaKarpwd@127.0.0.1:27017")
    db = client["CoronaDB"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

collection = db["CoronaTweets"]

with open("clusterAndOverallData.txt", "w") as text_file:

    ## Counts how many tweets are in each cluster
    ## Number of clusters has to be specified in range()
    for i in range(5):
        string = "CLUSTER " + str(i)
        frequency = 0
        print(string, file=text_file)
        for item in collection.find():
            if item["cluster"] == i:
                frequency = frequency + 1
        print(frequency, file=text_file)


    ## Counts which user interracted with other users most overall in general inetrractions
    size = 0
    user = ""
    collection = db["General"]
    for item in collection.find():
        newsize = 0
        freq = item["frequencies"]
        for key, value in freq.items():
            newsize = newsize + value
        if newsize > size:
            user = item["_name"]
            size = newsize
    print(" ", file=text_file)
    print("FOR GENERAL INERRACTIONS", file=text_file)
    print("User " + user + " interracted with most other users which is " + str(size) + "times", file=text_file)
    print(" ", file=text_file)

    ## Counts which user interracted with other users most in each cluster in general inetrractions
    for i in range(5):
        size = 0
        user = ""
        string = "GeneralCluster" + str(i)
        collection = db[string]
        for item in collection.find():
            newsize = 0
            freq = item["frequencies"]
            for key, value in freq.items():
                newsize = newsize + value
            if newsize > size:
                user = item["_name"]
                size = newsize
        print("CLUSTER "+ str(i), file=text_file)
        print("User " + user + " interracted with most other users which is " + str(size) + "times", file=text_file)

    ## Counts which user interracted with other users most overall in retweet interactions
    size = 0
    user = ""
    collection = db["Retweet"]
    for item in collection.find():
        newsize = 0
        freq = item["frequencies"]
        for key, value in freq.items():
            newsize = newsize + value
        if newsize > size:
            user = item["_name"]
            size = newsize
    print(" ", file=text_file)
    print("FOR RETWEET INERRACTIONS", file=text_file)
    print("User " + user + " retweeted most other users which is " + str(size) + "times", file=text_file)
    print(" ", file=text_file)

    ## Counts which user interracted with other users most in each cluster in retweet interactions
    for i in range(5):
        size = 0
        user = ""
        string = "RetweetCluster" + str(i)
        collection = db[string]
        for item in collection.find():
            newsize = 0
            freq = item["frequencies"]
            for key, value in freq.items():
                newsize = newsize + value
            if newsize > size:
                user = item["_name"]
                size = newsize
        print("CLUSTER "+ str(i), file=text_file)
        print("User " + user + " retweeted most other users which is " + str(size) + "times", file=text_file)

    ## Counts which user interracted with other users most overall in quoted/reply interactions
    size = 0
    user = ""
    collection = db["Quoted"]
    for item in collection.find():
        newsize = 0
        freq = item["frequencies"]
        for key, value in freq.items():
            newsize = newsize + value
        if newsize > size:
            user = item["_name"]
            size = newsize
    print(" ", file=text_file)
    print("FOR QUOTED/REPLY INERRACTIONS", file=text_file)
    print("User " + user + " quoted or replied to most other users which is " + str(size) + "times", file=text_file)
    print(" ", file=text_file)

    ## Counts which user interracted with other users most in each cluster in quoted/reply interactions
    for i in range(5):
        size = 0
        user = ""
        string = "QuotedCluster" + str(i)
        collection = db[string]
        for item in collection.find():
            newsize = 0
            freq = item["frequencies"]
            for key, value in freq.items():
                newsize = newsize + value
            if newsize > size:
                user = item["_name"]
                size = newsize
        print("CLUSTER "+ str(i), file=text_file)
        print("User " + user + " quoted or replied to most other users which is " + str(size) + "times", file=text_file)

    print("  ", file=text_file)
    print("FOR HASHTAGS", file=text_file)


    ## Counts which hashtag appeared with most other hashtags in the cluster
    for i in range(5):
        size = 0
        tag = ""
        string = "HashtagsCluster" + str(i)
        collection = db[string]
        for item in collection.find():
            newsize = 0
            freq = item["frequencies"]
            newsize = len(freq)
            tag = item["_tag"]
            if newsize > size:
                hashtag = tag
                size = newsize
        print("CLUSTER "+ str(i), file=text_file)
        print("Hashtag " + hashtag + " appeared with most other hashtags which is " + str(size) + " other hashtags", file=text_file)



