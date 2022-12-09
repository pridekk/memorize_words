import csv
import os
from datetime import datetime
from typing import List
import uuid
import pymongo

MONGO_HOST = os.getenv("MONGO_HOST", 'localhost:27017')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", 'words')
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")

client = pymongo.MongoClient(host=[MONGO_HOST], username=MONGO_USER, password=MONGO_PASSWORD)
words_db = client.get_database(MONGO_DB_NAME)
english_collection = words_db.get_collection("english")
user_collection = words_db.get_collection("users")


def insert_words(filename: str):
    with open(filename, encoding="utf-8") as file:
        fields = ["word", "meaning"]
        reader = csv.DictReader(file, fields)
        for row in reader:
            word = row.get("word")
            meaning = row.get("meaning")
            found = english_collection.find_one({"_id": word})
            if found is None:
                add_new_word(word)
                add_new_meanings_to_word(word, [meaning], 1)


def add_new_word(word: str, user_id=1):
    now = datetime.now()
    english_collection.insert_one(
        {
            "_id": word,
            "word": word,
            "meanings": [],
            "s_count": 0,
            "priority": 255,
            "creator": user_id,
            "created_at": now
        }
    )


def add_new_meanings_to_word(word: str, meanings: List[str], user_id=1):
    now = datetime.now()

    update_dict = {
        "$inc": {"s_count": 1}
    }
    if meanings:
        update_dict["$push"] = {
            "meanings": {
                "$each": [
                    {
                        "m_id": str(uuid.uuid4()),
                        "meaning": meaning,
                        "s_count": 1,
                        "d_count": 0,
                        "created_at": now,
                        "updated_at": now,
                        "priority": 255,
                        "creator": user_id
                    }
                    for meaning in meanings
                ]
            }
        }

    english_collection.update_one(
        {"_id": word},
        update_dict
    )


if __name__ == "__main__":
    insert_words("3000words.csv")
