from pymongo import MongoClient
import requests
import tweepy
import sys
from tweepy import OAuthHandler
import pycountry
import nltk
from nltk.tokenize import word_tokenize
import flask
import os
from flask import Flask, render_template, request
import time
import json
from http.client import IncompleteRead

nltk.download('punkt')
consumer_key = "bCbz0MtQH0uSHlkJShAIVloUy"
consumer_secret = "zDV2luhxHOUOM8vLBRaVFe8syOrEyRugKzaB0MOeHuWLDf69nr"
access_key = "844778696896491522-70MO64w1NqmLr4BHYko7v0kuxzBHM2i"
access_secret = "0o3AbY7WkifCnbtacoVzGzdecBaEzez5TZEjsqYDF4h3k"
client = MongoClient("mongodb+srv://maanas:abcd@tweets-am9qn.mongodb.net/test?retryWrites=true&w=majority")
punc = '''!-[]{};:'"\,<>./?@#$%^&*_~'''

def puncremover(test_str):
    for ele in test_str:
        if ele in punc:
            test_str = test_str.replace(ele, "")
    return test_str
    
def streaming_tweets(text_query,time_limit,retweets):

    tokens_tt = word_tokenize(" ".join(text_query))
    words_tt = [word for word in tokens_tt if word.isalpha()]
    dbname = "_".join(words_tt)
    print(dbname, time_limit)
    db = client[dbname]

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    countries = pycountry.countries
    listofcountries = []
    for i in countries:
        listofcountries.append(i.name.lower())
        listofcountries.append(i.alpha_2.lower())
        listofcountries.append(i.alpha_3.lower())

    loc = []
    text = []

    class MyStreamListener(tweepy.StreamListener):
        def __init__(self, time_limit=time_limit):
            self.start_time = time.time()
            self.limit = time_limit
            super(MyStreamListener, self).__init__()
        def on_status(self, status):
            if (retweets):
                if ((time.time() - self.start_time) < self.limit):
                    k = (status.user.location)
                    if (k is not None):
                        location = str(k).lower()
                        tokens = word_tokenize(location)
                        loclist = [word for word in tokens if word.isalpha()]
                        for i in loclist:
                            if i in listofcountries:
                                if (len(i) == 2):
                                    country = pycountry.countries.get(alpha_2=i.upper())
                                    i = puncremover(country.name.lower())
                                elif(len(i) == 3):
                                    country = pycountry.countries.get(alpha_3=i.upper())
                                    i = puncremover(country.name.lower())
                                collection = db[i]
                                # print(i, status.text)
                                try:
                                    collection.insert_one(status._json)
                                except Exception as e:
                                    print(e)
                                    pass
                    return True
                else:
                    return False
            else:
                if ((time.time() - self.start_time) < self.limit):
                    k = (status.user.location)
                    if (k is not None and (not status.retweeted) and ('RT @' not in status.text)):
                        location = str(k).lower()
                        tokens = word_tokenize(location)
                        loclist = [word for word in tokens if word.isalpha()]
                        for i in loclist:
                            if i in listofcountries:
                                if (len(i) == 2):
                                    country = pycountry.countries.get(alpha_2=i.upper())
                                    i = puncremover(country.name.lower())
                                elif(len(i) == 3):
                                    country = pycountry.countries.get(alpha_3=i.upper())
                                    i = puncremover(country.name.lower())
                                collection = db[i]
                                # print(i, status.text)
                                try:
                                    collection.insert_one(status._json)
                                except Exception as e:
                                    print(e)
                                    pass
                    return True
                else:
                    return False

    def start_stream():
        k = True
        while k:
            try:
                myStream = tweepy.Stream(auth = auth, listener=MyStreamListener())
                k = myStream.filter(track=text_query)
                print(k)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
                continue
    start_stream()

def oldtweets(text_query,maxtweets,retweets,restype):

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    tokens_tt = word_tokenize(" ".join(text_query))
    words_tt = [word for word in tokens_tt if word.isalpha()]
    dbname = "_".join(words_tt)
    print(dbname, maxtweets)
    print(restype)

    countries = pycountry.countries
    listofcountries = []
    for i in countries:
        listofcountries.append(i.name.lower())
        listofcountries.append(i.alpha_2.lower())
        listofcountries.append(i.alpha_3.lower())

    loc = []
    text = []

    db = client[dbname]
    max_id = -999999999
    count = 100
    sinceId = None

    print("Downloading max {0} tweets".format(maxtweets))
    sofar = 0
    while sofar < maxtweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=text_query, count=count, result_type=restype)
                else:
                    new_tweets = api.search(q=text_query, count=count, since_id=sinceId, result_type=restype)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=text_query, count=count, max_id=str(max_id - 1), result_type=restype)
                else:
                    new_tweets = api.search(q=text_query, count=count, max_id=str(max_id - 1), since_id=sinceId, result_type=restype)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                k = (tweet.user.location)
                if (retweets):
                    if (k is not None):
                        location = str(k).lower()
                        tokens = word_tokenize(location)
                        loclist = [word for word in tokens if word.isalpha()]
                        for i in loclist:
                            if i in listofcountries:
                                if (len(i) == 2):
                                    country = pycountry.countries.get(alpha_2=i.upper())
                                    i = puncremover(country.name.lower())
                                elif(len(i) == 3):
                                    country = pycountry.countries.get(alpha_3=i.upper())
                                    i = puncremover(country.name.lower())
                                collection = db[i]
                                # print(i, tweet.text)
                                sofar = sofar+1
                                try:
                                    collection.insert_one(tweet._json)
                                except Exception as e:
                                    print(e)
                                    pass
                    else:
                        continue
                else:
                    if (k is not None and (not tweet.retweeted) and ('RT @' not in tweet.text)):
                        location = str(k).lower()
                        tokens = word_tokenize(location)
                        loclist = [word for word in tokens if word.isalpha()]
                        for i in loclist:
                            if i in listofcountries:
                                if (len(i) == 2):
                                    country = pycountry.countries.get(alpha_2=i.upper())
                                    i = puncremover(country.name.lower())
                                elif(len(i) == 3):
                                    country = pycountry.countries.get(alpha_3=i.upper())
                                    i = puncremover(country.name.lower())
                                collection = db[i]
                                # print(i, tweet.text)
                                sofar = sofar+1
                                try:
                                    collection.insert_one(tweet._json)
                                except Exception as e:
                                    print(e)
                                    pass
                    else:
                        continue
            
            print("Downloaded {0} tweets".format(sofar),end='\r')
            max_id = new_tweets[-1].id
        except IncompleteRead:
            pass
        except tweepy.TweepError as e:
            print("error, " + str(e))
            break



app=Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/result',methods=['GET','POST'])

def result():
    errors = []
    if request.method == 'POST':
        try:
            streaming = request.form.get('choice')
            if (streaming == "true"):
                queries = request.form['queries']
                time = request.form['time']
                list_of_queries = queries.split()
                tokens_tt = word_tokenize(" ".join(list_of_queries))
                words_tt = [word for word in tokens_tt if word.isalpha()]
                dbname = "_".join(words_tt)
                retweets = request.form.get('rtcheck')
                print(retweets)
                
                if retweets=="on":
                    streaming_tweets(list_of_queries,int(time),True)
                else:
                    streaming_tweets(list_of_queries,int(time),False)

            else:
                queries = request.form['queries-old']
                maxtweets = request.form['number']
                restype = request.form['restype']
                list_of_queries = queries.split()
                tokens_tt = word_tokenize(" ".join(list_of_queries))
                words_tt = [word for word in tokens_tt if word.isalpha()]
                dbname = "_".join(words_tt)
                retweets = request.form.get('rtcheck-old')
                print(restype)
                print(retweets)

                if retweets=="on":
                    oldtweets(list_of_queries,int(maxtweets),True, str(restype))
                else:
                    oldtweets(list_of_queries,int(maxtweets),False, str(restype))
                #dbname = "functionality for old tweets not yet added"


            
        except Exception as e:
            errors.append(e)

        print(errors)
    return flask.render_template('index.html',result = "Done, database name is {dbname}, please query it to fetch the caputed tweets.".format(dbname=dbname))

if __name__ == '__main__':
    app.run()

