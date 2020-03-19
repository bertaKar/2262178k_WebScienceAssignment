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
    db = client["bertaDB"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

## Specify the collection
collection = db["generalCluster1"]


triads = 0
totalTies = 0
uniqueTies = 0

## Count the number of total ties (how many times someone was mentioned)

for item in collection.find():
    frequencies = item["frequencies"]
    for key, value in frequencies.items():
        totalTies = totalTies + value

print(totalTies)


## Count the number of unique ties (how many users have been mentioned)

for item in collection.find():
    frequencies = item["frequencies"]
    uniqueTies = uniqueTies + len(frequencies)

print(uniqueTies)


## Count circle triads i.e. A->B; B-> C; C->A



for itemA in collection.find():
    userA = itemA["_name"]
    mentionsA = itemA["frequencies"]
    for itemB in collection.find():
        userB = itemB["_name"]
        mentionsB = itemB["frequencies"]
        if userB in mentionsA:
            if userA != userB:
                for itemC in collection.find():
                    userC = itemC["_name"]
                    mentionsC = itemC["frequencies"]
                    if userC in mentionsB:
                        if userB != userC:
                            if userA in mentionsC:
                                if userA != userC:
                                    circles = circles + 1


## Count simple triads i.e. A->B; B-> C;


for itemA in collection.find():
    userA = itemA["_name"]
    mentionsA = itemA["frequencies"]
    for itemB in collection.find():
        userB = itemB["_name"]
        mentionsB = itemB["frequencies"]
        if userB in mentionsA:
            if userA != userB:
                for itemC in collection.find():
                    userC = itemC["_name"]
                    mentionsC = itemC["frequencies"]
                    if userC in mentionsB:
                        if userB != userC:
                            if userA not in mentionsC:
                                simple_triad = simple_triad + 1



##Print to file
with open("generalCluster1TiesAndTriads.txt", "w") as text_file:
    string1 = "Number of total ties: " + str(totalTies)
    print(string1, file=text_file)
    string2 = "Number of unique ties: " + str(uniqueTies)
    print(string2, file=text_file)
    string3 = "Number of triads: " + str(circles / 3 + simple_triad)
    print(string3, file=text_file)
