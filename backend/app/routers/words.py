from fastapi import APIRouter, Depends
from ..utils.mongo import get_word_by_id
router = APIRouter()


@router.get("/search")
def get_user_by_id(word: str):
    result = get_word_by_id(word)

    return result
