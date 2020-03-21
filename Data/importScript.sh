colls=( CoronaTweets General GeneralCluster0 GeneralCluster1 GeneralCluster2 GeneralCluster3 GeneralCluster4 Retweet RetweetCluster0 RetweetCluster1 RetweetCluster2 RetweetCluster3 RetweetCluster4 Quoted QuotedCluster0 QuotedCluster1 QuotedCluster2 QuotedCluster3 QuotedCluster4 Hashtags HashtagsCluster0 HashtagsCluster1 HashtagsCluster2 HashtagsCluster3 HashtagsCluster4 )

for c in ${colls[@]}
do
  mongoimport --db=CoronaDB --collection=$c --file=$c.csv
done