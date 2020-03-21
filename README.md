### Tools used:
Python 3.8.2., Tweepy 3.8.0., Pymongo 3.10.1
 
### Description
The repository contains "Twitter" scraper/data crawler and network analysis software.

### Connecting to your own database
Each script in this repository contain contain to connect to the author's database. To be able to use software on your own database you <b> WILL NEED TO </b> change the connection code to include your database information <b> FOR ALL 8 SCRIPTS </b>.
Each script contains the line <pre class="prettyprint lang-cpp linenums"> client = MongoClient("mongodb://bertaKar:bertaKarpwd@127.0.0.1:27017") </pre> 

This line should be changed with your own data like this <pre class="prettyprint lang-cpp linenums"> client = MongoClient("mongodb://&lt;username&gt;:&lt;password&gt;@&lt;host&gt;:&lt;port&gt;") </pre> 


### How To Import Sample Data
To import sample data make sure you are connected to your MongoDB database. Then you have to navigate to the "Data" folder in this repository and execute on command line: <pre class="prettyprint lang-cpp linenums"> ./importScript.sh </pre> 

If you get permission denied run: <pre class="prettyprint lang-cpp linenums"> chmod 666 importScript.sh </pre> 

and then run <pre class="prettyprint lang-cpp linenums"> ./importScript.sh </pre>

#### NOTE
It is not neccesary to import sample data. While running the scripts your database will be populated with real-time data instead. However, sample data is supplied so that the marker could see the dataset I was working with to produce the results presented in the report. 

### How To Use This Software
Once all eight scripts have been changed to connect to your own database (See section "Connecting to your own database") you can run the software. 

Firstly, run the script <b> "scraper.py" </b>. This script populates the initial collection "CoronaTweets" with real time data with the streamer object. This script can be left to run for as long as needed. The longer it runs the more tweets it will retrieve. <b> If you already imported sample data, this script will add more tweets to the sample data collection </b>.

##### The repository is comprised of 8 scripts and a Data folder:
* scraper.py
* mostMentioned.py
* rest.py
* cluster.py
* freq.py
* freqCluster.py
* tie_triad.py
* #### Data
  * importScript.sh <sub><sup> (Script to import sample data into local database) </sub></sup>
  * MostMentioned.txt <sub><sup>(List of most mentioned users in the dataset)</sub></sup>
  * clusterAndOverallData.txt <sub><sup>(Contains information about most interracted users and hashtags for overall and cluster data)</sub></sup>
  * TiesAndTriads.txt <sub><sup>(Contains information about ties and triads in overall and cluster data)</sub></sup>
  * CoronaTweets.csv <sub><sup>(Dataset containing all scraped tweets)</sub></sup>
  * General.csv <sub><sup>(Dataset containing frequencies of general interaction in overall data)</sub></sup>
  * GeneralCluster[0-4].csv <sub><sup>(General data for each cluster)</sub></sup>
  * Retweet.csv <sub><sup>(Dataset containing frequencies of retweet interaction in overall data)</sub></sup>
  * RetweetCluster[0-4].csv <sub><sup>(Retweet data for each cluster)</sub></sup>
  * Quoted.csv <sub><sup>(Dataset containing frequencies of quoted/reply interaction in overall data)</sub></sup>
  * QuotedCluster[0-4].csv <sub><sup>(Quoted/reply data for each cluster)</sub></sup>
  * Hashtags.csv <sub><sup>(Dataset containing all used hashtags and the list of which other hashtags this hashtag has appeared together with)</sub></sup>
  * HashtagsCluster[0-4]. <sub><sup>(Hashtag data for each cluster)</sub></sup>



