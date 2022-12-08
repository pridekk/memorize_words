import re
import os
from types import SimpleNamespace
from typing import List
import uuid
import pymongo
from datetime import datetime
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

from fastapi.logger import logger

from ..models.users import User
from ..models.words import Meaning, Word, WordRequest

MONGO_HOST = os.getenv("MONGO_HOST", 'localhost:27017')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", 'words')
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")

PymongoInstrumentor().instrument()

client = pymongo.MongoClient(host=[MONGO_HOST], username=MONGO_USER, password=MONGO_PASSWORD)
words_db = client.get_database(MONGO_DB_NAME)
english_collection = words_db.get_collection("english")
user_collection = words_db.get_collection("users")


def get_meanings_by_id(word: str):
    word = english_collection.find_one({"_id": word})

    if word:
        word = Word(**word)

        meanings = word.meanings

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

    english_word = english_collection.find_one({"_id": word_meanings.word})

    if english_word:
        english_word = Word(**english_word)
        registered_meanings = set([meaning.meaning for meaning in english_word.meanings])
        new_meanings = set(word_meanings.meanings) - registered_meanings
        logger.info(f"Add new meanings {new_meanings} to {word_meanings.word}")
        add_new_meanings_to_word(word_meanings.word, list(new_meanings))
    else:
        logger.info(f"No word '{word_meanings.word}' in db create")
        add_new_word(word_meanings.word, user_id)
        add_new_meanings_to_word(word_meanings.word, word_meanings.meanings)

    add_new_meanings_to_user_word(user_id, word_meanings.word, word_meanings.meanings)


def add_new_word(word: str, user_id=1):
    now = datetime.now()
    english_collection.insert_one(
        {
            "_id": word,
            "word": word,
            "meanings": [],
            "s_count": 1,
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


def add_new_meanings_to_user_word(user_id: int, word: str, meanings: List[str]):

    now = datetime.now()
    user = User(**user_collection.find_one({"_id": user_id}))

    registered_meanings = user.get_meanings(word)
    if registered_meanings:
        registered_meanings_list = set([mean.meaning for mean in registered_meanings])
        new_meanings = set(meanings) - registered_meanings_list

        update_dict = {
                "$set": {"words.$.updated_at": now},
                "$inc": {
                    "words.$.search_count": 1
                }
            }
        if new_meanings:
            update_dict["$push"] = {
                    "words.$.meanings": {
                        "$each": [
                            {
                                "meaning": item
                            } for item in list(new_meanings)
                        ]
                    }
                }

        user_collection.update_one(
            {"_id": user_id, "words.word": word},
            update_dict
        )
    else:
        user_collection.update_one(
            {"_id": user_id},
            {
                "$push": {
                    "words": {
                        "word": word,
                        "meanings": [{"meaning": item} for item in list(meanings)],
                        "memorized": False,
                        "created_at": now,
                        "updated_at": now,
                        "correct_count": 0,
                        "incorrect_count": 0,
                        "search_count": 1,
                        "last_quizzed_at": None
                    }
                }
            }
        )

