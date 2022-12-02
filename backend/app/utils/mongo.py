from dataclasses import dataclass
import json
import os
from types import SimpleNamespace
from datetime import datetime
import pymongo

MONGO_HOST = os.getenv("MONGO_HOST", 'localhost:27017')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", 'words')
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")

client = pymongo.MongoClient(host=[MONGO_HOST], username=MONGO_USER, password=MONGO_PASSWORD)
words_db = client.get_database(MONGO_DB_NAME)
english_collection = words_db.get_collection("english")


@dataclass
class Meaning:
    m_id: str
    meaning: str
    verb: str
    s_count: int
    d_count: int
    created_at: datetime
    updated_at: datetime
    priority: int

    def __eq__(self, other):
        return self.priority == other.priority and self.s_count == other.s_count

    def __lt__(self, other):
        return self.priority > other.priority or self.s_count < other.s_count


def get_meanings_by_id(word: str):
    cursor = english_collection.find({"_id": word})
    word = cursor.next()
    word = SimpleNamespace(**word)

    meanings = []
    for item in word.meanings:
        meanings.append(Meaning(**item))

    meanings.sort(reverse=True)

    return meanings


def increase_delete_count(word: str, m_id: str):
    cursor = english_collection.find({"_id": word})
    word = cursor.next()
    word = SimpleNamespace(**word)

    meanings = []
    for item in word.meanings:
        meanings.append(Meaning(**item))

    meanings.sort(reverse=True)

    return meanings