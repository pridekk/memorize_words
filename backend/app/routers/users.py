from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    pass
