from typing import List

from pydantic import BaseModel
from datetime import datetime

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

fake_users_db = {
    "pridekk": {
        "_id": 1,
        "user_id": 1,
        "username": "pridekk",
        "email": "pridekk@gmail.com",
        "joined_at": "2022-11-19 12:00:00",
        "words": [
            {
                "word": "read",
                "meanings": [
                    {
                        "meaning": "읽다"
                    }
                ],
                "memorized": False,
                "created_at": "2022-11-30 11:00:00",
                "updated_at": "2022-11-30 11:00:00",
                "correct_count": 1,
                "incorrect_count": 2,
                "search_count": 1,
                "last_quizzed_at": "2022-11-30 10:00:00"
            }
        ],
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",

    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserMeaning(BaseModel):
    meaning: str


class UserWord(BaseModel):
    word: str
    meanings: List[UserMeaning]
    memorized: bool = False
    created_at: datetime
    updated_at: datetime
    correct_count: int = 0
    incorrect_count: int = 0
    search_count: int = 1
    last_quizzed_at: datetime | None = None


class User(BaseModel):
    user_id: int
    username: str
    email: str | None = None
    joined_at: datetime
    words: List[UserWord]
    disabled: bool


class UserInDB(User):
    hashed_password: str
