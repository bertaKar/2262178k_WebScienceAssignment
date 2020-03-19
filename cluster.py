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
    db = client["bertaDB"]
    collection = db["REAL"]

    print("Connected successfully!!!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

##Retrieve the collection and store it in Pandas dataframe
tweets = collection.find()
tweetList = list(tweets)
dumps(tweetList)
json_normalize(tweetList)

for tweet in tweetList:
    tweet["created_at"] = int(tweet["created_at"].strftime("%Y%m%d%H%M%S"))
    tweet["hashedText"] = hash(tweet["text"])


df = pd.DataFrame(tweetList)


# Set index to id for easy matching
df.set_index('_id', inplace=True)

# Start timing implementation
t0 = time.time()

# MiniBatch section
mb = MiniBatchKMeans(n_clusters=6, init='k-means++', n_init=10, batch_size=3000)
data = df[["hashedText", "created_at"]].values
mb.fit(data)
df['mb_cluster'] = mb.labels_   # Add labels back into DataFrame

# DBSCAN section
eps = 2000000000000000000

for i in df.mb_cluster.unique():
    subset = df.loc[df.mb_cluster == i]
    db = DBSCAN(eps=eps, min_samples=100)
    data = subset[["hashedText", "created_at"]].values
    db.fit(data)
    subset['db_cluster'] = db.labels_
    df.loc[df.mb_cluster == i, 'db_cluster'] = subset['db_cluster']

# Set final cluster variable
df['cluster'] = df.mb_cluster + (df.db_cluster.replace(-1.0, np.nan) / 100)

t1 = time.time() - t0
# Print implementation time
print('Implementation time: {}'.format(t1))

j = df.to_json(orient='records')

df1 = df[['text', 'cluster']]

# Sort the values by cluster

df.sort_values("cluster", inplace=True)

## Save the assigned clusters to the database

for index, frame in df.iterrows():
    for tweet in collection.find():
        if frame["username"] == tweet["username"]:
            collection.update_one({'_id': tweet["_id"]}, {"$set": {"cluster": frame["cluster"]}}, upsert=False, array_filters=None)


