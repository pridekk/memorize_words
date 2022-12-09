from typing import List

from fastapi import APIRouter, Depends

from ..models.words import Meaning, Word
from ..utils.mongo import get_meanings_by_query, increase_delete_count, get_words_by_query
from ..utils.users import get_user_id
router = APIRouter()


@router.get("/", response_model=List[Word])
def get_words(query: str,  page: int = 1, size: int = 20, user_id=Depends(get_user_id)):
    result: List[Word] = get_words_by_query(query, page, size)

    return result


@router.get("/{word}/meanings", response_model=List[Meaning])
def get_meanings(word: str, user_id=Depends(get_user_id)):
    result = get_meanings_by_query(word)

    return result


@router.patch("/{word}/meanings/{m_id}/decrease")
def increase_d_count(word: str, m_id: str, user_id=Depends(get_user_id)):

    increase_delete_count(word, m_id)

    return {
        "message": "decreased count"
    }


