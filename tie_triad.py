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

    # Connect to the database

    client = MongoClient("mongodb://bertaKar:bertaKarpwd@127.0.0.1:27017")
    db = client["CoronaDB"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

with open("TiesAndTriads.txt", "w") as text_file:

    # For general interaction
    collection = db["General"]
    print("FOR GENERAL INTERRACTION ON OVERALL DATA", file=text_file)

    triads = 0
    totalTies = 0
    uniqueTies = 0

    # Count the number of total ties (how many times someone was mentioned)

    for item in collection.find():
        frequencies = item["frequencies"]
        for key, value in frequencies.items():
            totalTies = totalTies + value

    # Count the number of unique ties (how many users have been mentioned)

    for item in collection.find():
        frequencies = item["frequencies"]
        uniqueTies = uniqueTies + len(frequencies)

    # Print to file the number of total ties and unique ties

    string1 = "Number of total ties: " + str(totalTies)
    print(string1, file=text_file)
    string2 = "Number of unique ties: " + str(uniqueTies)
    print(string2, file=text_file)

    # Count circle triads i.e. A->B; B-> C; C->A

    print("CIRCLE TRIADS")

    circles = 0

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
                                        string = userA + "-->" + userB + "-->" + userC + "-->" + userA
                                        print(string)

    # Count simple triads i.e. A->B; B-> C;

    print("SIMPLE TRIADS")

    simple_triad = 0

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
                                    string = userA + "-->" + userB + "-->" + userC
                                    print(string)

    # Print the total number of triads

    string3 = "Number of triads: " + str(circles / 3 + simple_triad)
    print(string3, file=text_file)

    # For general interaction clusters

    print("FOR GENERAL INTERRACTION ON EACH CLUSTER", file=text_file)

    for i in range(5):

        print(" ")
        print("CLUSTER" + str(i), file=text_file)

        coll = "GeneralCluster" + str(i)
        collection = db[coll]

        triads = 0
        totalTies = 0
        uniqueTies = 0

        # Count the number of total ties (how many times someone was mentioned)

        for item in collection.find():
            frequencies = item["frequencies"]
            for key, value in frequencies.items():
                totalTies = totalTies + value

        # Count the number of unique ties (how many users have been mentioned)

        for item in collection.find():
            frequencies = item["frequencies"]
            uniqueTies = uniqueTies + len(frequencies)

        # Print to file the number of total ties and unique ties

        string1 = "Number of total ties: " + str(totalTies)
        print(string1, file=text_file)
        string2 = "Number of unique ties: " + str(uniqueTies)
        print(string2, file=text_file)

        # Count circle triads i.e. A->B; B-> C; C->A

        print("CIRCLE TRIADS")

        circles = 0

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
                                            string = userA + "-->" + userB + "-->" + userC + "-->" + userA
                                            print(string)

        # Count simple triads i.e. A->B; B-> C;

        print("SIMPLE TRIADS")

        simple_triad = 0

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
                                        string = userA + "-->" + userB + "-->" + userC
                                        print(string)

        # Print the total number of triads

        string3 = "Number of triads: " + str(circles / 3 + simple_triad)
        print(string3, file=text_file)

    # For RETWEET interaction
    collection = db["Retweet"]
    print("FOR RETWEET INTERRACTION ON OVERALL DATA", file=text_file)

    triads = 0
    totalTies = 0
    uniqueTies = 0

    # Count the number of total ties (how many times someone was mentioned)

    for item in collection.find():
        frequencies = item["frequencies"]
        for key, value in frequencies.items():
            totalTies = totalTies + value

    # Count the number of unique ties (how many users have been mentioned)

    for item in collection.find():
        frequencies = item["frequencies"]
        uniqueTies = uniqueTies + len(frequencies)

    # Print to file the number of total ties and unique ties

    string1 = "Number of total ties: " + str(totalTies)
    print(string1, file=text_file)
    string2 = "Number of unique ties: " + str(uniqueTies)
    print(string2, file=text_file)

    # Count circle triads i.e. A->B; B-> C; C->A

    print("CIRCLE TRIADS")

    circles = 0

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
                                        string = userA + "-->" + userB + "-->" + userC + "-->" + userA
                                        print(string)

    # Count simple triads i.e. A->B; B-> C;

    print("SIMPLE TRIADS")

    simple_triad = 0

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
                                    string = userA + "-->" + userB + "-->" + userC
                                    print(string)

    # Print the total number of triads

    string3 = "Number of triads: " + str(circles / 3 + simple_triad)
    print(string3, file=text_file)

    # For RETWEET interaction clusters
    print(" ", file=text_file)

    print("FOR RETWEET INTERRACTION ON EACH CLUSTER", file=text_file)

    for i in range(5):

        print(" ")
        print("CLUSTER" + str(i), file=text_file)

        coll = "RetweetCluster" + str(i)
        collection = db[coll]

        triads = 0
        totalTies = 0
        uniqueTies = 0

        # Count the number of total ties (how many times someone was mentioned)

        for item in collection.find():
            frequencies = item["frequencies"]
            for key, value in frequencies.items():
                totalTies = totalTies + value

        # Count the number of unique ties (how many users have been mentioned)

        for item in collection.find():
            frequencies = item["frequencies"]
            uniqueTies = uniqueTies + len(frequencies)

        # Print to file the number of total ties and unique ties

        string1 = "Number of total ties: " + str(totalTies)
        print(string1, file=text_file)
        string2 = "Number of unique ties: " + str(uniqueTies)
        print(string2, file=text_file)

        # Count circle triads i.e. A->B; B-> C; C->A

        print("CIRCLE TRIADS")

        circles = 0

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
                                            string = userA + "-->" + userB + "-->" + userC + "-->" + userA
                                            print(string)

        # Count simple triads i.e. A->B; B-> C;

        print("SIMPLE TRIADS")

        simple_triad = 0

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
                                        string = userA + "-->" + userB + "-->" + userC
                                        print(string)

        # Print the total number of triads

        string3 = "Number of triads: " + str(circles / 3 + simple_triad)
        print(string3, file=text_file)

    # For QUOTED/REPLY interaction
    print(" ", file=text_file)
    collection = db["Quoted"]
    print("FOR QUOTED/REPLY INTERRACTION ON OVERALL DATA", file=text_file)

    triads = 0
    totalTies = 0
    uniqueTies = 0

    # Count the number of total ties (how many times someone was mentioned)

    for item in collection.find():
        frequencies = item["frequencies"]
        for key, value in frequencies.items():
            totalTies = totalTies + value

    # Count the number of unique ties (how many users have been mentioned)

    for item in collection.find():
        frequencies = item["frequencies"]
        uniqueTies = uniqueTies + len(frequencies)

    # Print to file the number of total ties and unique ties

    string1 = "Number of total ties: " + str(totalTies)
    print(string1, file=text_file)
    string2 = "Number of unique ties: " + str(uniqueTies)
    print(string2, file=text_file)

    # Count circle triads i.e. A->B; B-> C; C->A

    print("CIRCLE TRIADS")

    circles = 0

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
                                        string = userA + "-->" + userB + "-->" + userC + "-->" + userA
                                        print(string)

    # Count simple triads i.e. A->B; B-> C;

    print("SIMPLE TRIADS")

    simple_triad = 0

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
                                    string = userA + "-->" + userB + "-->" + userC
                                    print(string)

    # Print the total number of triads

    string3 = "Number of triads: " + str(circles / 3 + simple_triad)
    print(string3, file=text_file)

    # For QUOTED/REPLY interaction clusters
    print(" ", file=text_file)

    print("FOR QUOTED/REPLY INTERRACTION ON EACH CLUSTER", file=text_file)

    for i in range(5):

        print(" ")
        print("CLUSTER" + str(i), file=text_file)

        coll = "QuotedCluster" + str(i)
        collection = db[coll]

        triads = 0
        totalTies = 0
        uniqueTies = 0

        # Count the number of total ties (how many times someone was mentioned)

        for item in collection.find():
            frequencies = item["frequencies"]
            for key, value in frequencies.items():
                totalTies = totalTies + value

        # Count the number of unique ties (how many users have been mentioned)

        for item in collection.find():
            frequencies = item["frequencies"]
            uniqueTies = uniqueTies + len(frequencies)

        # Print to file the number of total ties and unique ties

        string1 = "Number of total ties: " + str(totalTies)
        print(string1, file=text_file)
        string2 = "Number of unique ties: " + str(uniqueTies)
        print(string2, file=text_file)

        # Count circle triads i.e. A->B; B-> C; C->A

        print("CIRCLE TRIADS")

        circles = 0

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
                                            string = userA + "-->" + userB + "-->" + userC + "-->" + userA
                                            print(string)

        # Count simple triads i.e. A->B; B-> C;

        print("SIMPLE TRIADS")

        simple_triad = 0

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
                                        string = userA + "-->" + userB + "-->" + userC
                                        print(string)

        # Print the total number of triads

        string3 = "Number of triads: " + str(circles / 3 + simple_triad)
        print(string3, file=text_file)
