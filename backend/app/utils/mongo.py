import re
import os
from types import SimpleNamespace
from typing import List
import uuid
import pymongo
from datetime import datetime
from fastapi.logger import logger

from ..models.users import User
from ..models.words import Meaning, Word, WordRequest

MONGO_HOST = os.getenv("MONGO_HOST", 'localhost:27017')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", 'words')
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")

client = pymongo.MongoClient(host=[MONGO_HOST], username=MONGO_USER, password=MONGO_PASSWORD)
words_db = client.get_database(MONGO_DB_NAME)
english_collection = words_db.get_collection("english")
user_collection = words_db.get_collection("users")


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


def add_user_word(user_id: int, word_meanings: WordRequest):
    user = user_collection.find_one({"_id": user_id})

    english_word = english_collection.find_one({"_id": word_meanings.word})

    if english_word:
        english_word = Word(**english_word)
        registered_meanings = set([meaning.meaning for meaning in english_word.meanings])
        new_meanings = set(word_meanings.meanings) - registered_meanings

        if new_meanings:
            logger.info(f"Add new meanings {new_meanings} to {word_meanings.word}")
            add_new_meanings(word_meanings.word, list(new_meanings))
        else:
            logger.debug(f"No new meaning {word_meanings.word}")
    else:
        logger.info(f"No word '{word_meanings.word}' in db create")
        add_new_word(word_meanings.word, word_meanings.meanings)


    user_collection.update_one(
        {"_id", user_id},
        {

        }
    )




def add_new_word(word: str, meanings: List[str], user_id=1):
    now = datetime.now()
    english_collection.insert_one(
        {
            "_id": word,
            "meanings": [],
            "s_count": 1,
            "priority": 255,
            "creator": user_id,
            "created_at": now
        }
    )

    add_new_meanings(word, meanings)


def add_new_meanings(word: str, meanings: List[str], user_id=1):
    now = datetime.now()
    meanings = [
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
    english_collection.update_one(
        {"_id": word},
        {"$push": {"meanings": {"$each": meanings}}}
    )

    user = user_collection.find_one({"_id": user_id})
    already_registered = False

    for registered_word in User(**user).words:
        if registered_word.word == word:
            already_registered = True
            registered_meanings = set([mean.meaning for mean in registered_word.meanings])
            new_meanings = set(meanings) - registered_meanings

            if new_meanings:
                user_collection.update_one(
                    {"_id": user_id, "words.word": word},
                    {
                        "$push": {
                            "words.$.meanings": {
                                "$each": [
                                    {
                                        "meaning": item
                                    } for item in list(new_meanings)
                                ]
                            }
                        }
                    }
                )
                break
    if already_registered is False:


    user_word = {
        "word": word,
        "meanings": {

        }
    }
    user_collection.update_one(
        {"_id": user_id},
        {
            pu
        }
    )
