from pymongo import MongoClient
client = MongoClient("mongodb+srv://maanas:abcd@tweets-am9qn.mongodb.net/test?retryWrites=true&w=majority")

countries = []
topics = []
if client != None:
    database_names = client.list_database_names()

    print (len(database_names), "topics.")
    for db in database_names:
        topics.append(db)

print(topics)
topic = input()
collection_names = client[topic].list_collection_names()
for i in (collection_names):
            countries.append(i)

