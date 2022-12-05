from typing import List

from fastapi import APIRouter, Depends

from ..models.words import Meaning, Word
from ..utils.mongo import get_meanings_by_id, increase_delete_count, get_words_by_id
router = APIRouter()


@router.get("/", response_model=List[Word])
def get_words_by_query(query: str):
    result: List[Word] = get_words_by_id(query)

    return result


@router.get("/{word}/meanings", response_model=List[Meaning])
def get_meanings_by_word(word: str):
    result = get_meanings_by_id(word)

    return result


@router.patch("/{word}/meanings/{m_id}/decrease")
def increase_d_count(word: str, m_id: str):

    increase_delete_count(word, m_id)

    return {
        "message": "decreased count"
    }


