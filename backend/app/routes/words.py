from fastapi import APIRouter, Depends
from ..utils.mongo import get_meanings_by_id, increase_delete_count
router = APIRouter()


@router.get("/search")
def get_meanings_by_word(word: str):
    result = get_meanings_by_id(word)

    return result


@router.patch("/{word}/d-count/{m_id}")
def increase_d_count(word: str, m_id: str):

    pass
