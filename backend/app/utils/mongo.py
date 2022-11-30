import os

import pymongo

MONGO_HOST = os.getenv("MONGO_HOST", 'localhost:27017')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", 'words')
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")

client = pymongo.MongoClient(host=[MONGO_HOST], username=MONGO_USER, password=MONGO_PASSWORD)
words_db = client.get_database(MONGO_DB_NAME)
english_collection = words_db.get_collection("english")


def get_word_by_id(word: str):
    return english_collection.find({"_id": word})
