import re
import os
from types import SimpleNamespace

import pymongo

from ..models.words import Meaning, Word

MONGO_HOST = os.getenv("MONGO_HOST", 'localhost:27017')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", 'words')
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")

client = pymongo.MongoClient(host=[MONGO_HOST], username=MONGO_USER, password=MONGO_PASSWORD)
words_db = client.get_database(MONGO_DB_NAME)
english_collection = words_db.get_collection("english")


def get_meanings_by_id(word: str):
    cursor = english_collection.find({"_id": word})
    word = cursor.next()
    word = SimpleNamespace(**word)

    meanings = []
    for item in word.meanings:
        meanings.append(Meaning(**item))

    meanings.sort(reverse=True)

    return meanings


def get_words_by_id(query: str):
    regex = re.compile(query, re.IGNORECASE)

    words = english_collection.find({"_id": regex}, {"_id": 1, "s_count": 1, "priority": 1})

    result = []
    for word in words:
        result.append(Word(**word))

    result.sort(reverse=True)

    return result


def increase_delete_count(word: str, m_id: str):
    english_collection.update_one(
        {"_id": word, "meanings.m_id": m_id},
        {"$inc": {"meanings.$.d_count": 1}}
    )

