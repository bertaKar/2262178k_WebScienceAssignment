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

# for i in range(5):
#     frequency = 0
#     print("---------------CLUSTER---------------")
#     print(i)
#     for item in collection.find():
#         if item["cluster"] == i:
#             frequency = frequency + 1
#     print(frequency)
# with open("users.txt", "w") as text_file:

#     users = {}
#     checked = []

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
print("User " + user + " interracted with most other users which is " + str(size) + "times")

# freqTags = {}
# checked = []
# frequency = 0
# for item in collection.find():
#     hashtags = item["hashtags"]
#     for tag in hashtags:
#             freqTags[tag] = freqTags[tag] + 1

# print("OVERALL TOP HASHTAGS")

# topHashtags = sorted(freqTags.items(), key=lambda x: x[1])[-5:]
# print(topHashtags)

