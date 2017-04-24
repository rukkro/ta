To use: insert correct Twitter (tweet streaming) and/or Kairos (image analysis) API keys into the `config.py` file, then run `menu_main.py`, which is a menu interface.

Install mongoDB and run with `mongod --dbpath=/path/to/db`.

Requires Python 3.x, tested on 3.5/3.6.

1. Twitter tweet streaming [x]  - queue system found to be unnecessary, rarely tweets will be skipped to catch up.
2. Set up MongoDB system [x]
3. Check tweet duplicates [x] - Checks for exact duplicates and by similarity user can modify (default 55%) within same collection.
4. Sentiment analaysis [x] - Basic <a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a> implemented.
5. Associate characteristics using Kairos to tweets + users. [x]
6. Export to .csv spreadsheets. [x]
7. Historical tweet gathering 

## Notes:
  #### MongoDB
1.  Tweets are placed in MongoDB databases. These databases contain collections, and these collections contain documents.
2.  A document will contain the Twitter API data, the Kairos API data, the Vader Sentiment data, and anything else that is inserted.
      A document is basically a JSON file, but in binary format - a <a href="https://docs.mongodb.com/manual/core/document/">BSON</a>.
3.  When a collection is marked as temporary, a single document is created with the value `"temp" : True`. 
      This makes it easier to delete a group of collections later using the "Manage Collections" menu later.
  #### Tweet Streaming:
 1.  Tweepy is used as the Python module to interface with the Twitter API.
 2.  Retrieves new tweets created while the program is running.
 3.  Filters out retweets, quoted retweets, replies, and incomplete tweets(does not contain "created_at" in JSON data).
 4.  Finds duplicates in same collection by removing punctuation and spaces from tweet to be checked, 
      then getting all tweets from the same Twitter user. All of their tweets have punct. and spaces removed. Exact duplicates, and 
      similar tweets(defined by the similarity threshold) are ignored.
 5. Tweet data from the Twitter API is inserted into the specified MongoDB database and collection, in a JSON-like format.
 6. Incomplete Read error occurs when the API needs to "catch up" to the latest tweets. Some tweets are skipped when this occurs.
      Adding more filters (language, follower, etc) supposedly increases the frequency of this error.
 7. Queries using both the follower and search term options, will retrieve ANY new tweets from the specified user, and ANY tweets
    from any user who tweets the specified search term.
    
  #### Sentiment Analysis with Vader Sentiment:
1.  The NLTK Python module is used with <a href="https://github.com/cjhutto/vaderSentiment">Vader Sentiment</a>.
      Specifically, `subjectivity`, `vader_lexicon`, and `punkt` are used with the Naive Bayes Classifier to train it to understand
      tweet content.
2.  Four values are found from analysis: the positivity, negativity, and neutrality of the tweet. 
      In addition, the compound value is calculated: see the Vader Sentiment link above for an explanation.
3.  These values are inserted in each tweet document in the specified collection under `sentiment` : (`pos`,`neg`,`neu`, and `compound`).

  #### Facial Analysis with Kairos
1.  The Kairos facial detection and emotion/age/gender APIs are used.
2.  The profile image URL is taken from the current document in the collection, and is tested if it exists.
3.  The current doc is checked for `default_profile_image` being false, and the URL does not contain a 'default' picture URL.
4.  The current image is individually downloaded as `ta-image.jpg`, then is uploaded to the Kairos detect API.
5.  If the API does not find a face, then the next document repeats this process (overwriting `ta-image.jpg` with each new image).
6.  If a face is found, then the image is uploaded and run through the Kairos emotion API. 
7.  Data from the detection and emotion API are inserted into the current document under `face` : (`detect` and `emotion`)
8.  When the final image is processed, `ta-image.jpg` is deleted.
9.  Occasionally, the Kairos API will return facial detection data, but not emotion data. 
