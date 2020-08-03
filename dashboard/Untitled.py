from pymongo import MongoClient
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string


# In[137]:


client = MongoClient("mongodb+srv://maanas:abcd@tweets-am9qn.mongodb.net/test?retryWrites=true&w=majority")


# In[138]:


countries = []
topics = []
if client != None:
    database_names = client.list_database_names()

    print (len(database_names), "topics.")
    for db in database_names:
        topics.append(db)


# In[139]:


topics.remove("local")
topics.remove("admin")
databases=dict()

# In[140]:


for topic in topics:


# In[141]:
    

    collection_names = client[topic].list_collection_names()
    countries=[]
    for i in (collection_names):
                countries.append(i)


    # In[142]:


    countries


    # In[143]:


    counts = []
    sentiments = []
    numtwts = []


    # In[144]:


    db = client[topic]

    for i in countries:
        collection = db[i]
        documents = []
        for doc in collection.find():
            documents.append(doc)

        df = pd.DataFrame(documents)

        df['tweet_source'] = df['source'].apply(lambda x: BeautifulSoup(x,features="html.parser").get_text())
        devices = list(set(df[df['tweet_source'].str.startswith('Twitter')]['tweet_source']))
        adstring = 'Twitter for Advertisers'

        if adstring in devices:
            devices.remove('Twitter for Advertisers')

        df = df[df['tweet_source'].isin(devices)]

        nltk.download('stopwords', quiet=True)
        nltk.download('vader_lexicon', quiet=True)

        df['tokens'] = df['text'].apply(TweetTokenizer().tokenize)

        stopwords_vocabulary = stopwords.words('english')
        df['stopwords'] = df['tokens'].apply(lambda x: [i for i in x if i.lower() not in stopwords_vocabulary])

        punctuations = list(string.punctuation)

        df['punctuation'] = df['stopwords'].apply(lambda x: [i for i in x if i not in punctuations])
        df['digits'] = df['punctuation'].apply(lambda x: [i for i in x if i[0] not in list(string.digits)])
        df['final'] = df['digits'].apply(lambda x: [i for i in x if len(i) > 1])


        sentiment = SentimentIntensityAnalyzer()

        df['sentiment'] = df.text.apply(lambda x: sentiment.polarity_scores(x)['compound'])

        pos = len(df[df.sentiment > 0])
        neg = len(df[df.sentiment < 0])
        neu = len(df[df.sentiment == 0])

        y = [pos, neu, neg]
        counts.append(i)
        sentiments.append(y)
        numtwts.append(len(documents))


    # In[145]:


    counts


    # In[146]:


    pos = [i[0] for i in sentiments]
    neu = [i[1] for i in sentiments]
    neg = [i[2] for i in sentiments]


    # In[147]:


    numtwts


    # In[148]:


    res = pd.DataFrame({'country': counts, 'positive': pos, 'neutral': neu, 'negative':neg})

    # In[149]:


    pd.set_option("display.max_rows", None, "display.max_columns", None)


    # In[150]:


    res


    # In[111]:


    res.set_index('country')
    databases[topic] = res