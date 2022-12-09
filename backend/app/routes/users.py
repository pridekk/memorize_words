from fastapi import APIRouter, Depends

from ..models.words import WordRequest
from ..utils.users import *
from ..utils.mongo import add_user_word, get_user_words
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "username": user.username,
            "user_id": user.user_id
        }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/me/add")
def add_words(word: WordRequest, user_id=Depends(get_user_id)):
    add_user_word(user_id, word)

    return {
        "message": "등록되었습니다."
    }


@router.get("/me/words")
def get_my_words(page=1, size=20, sort_by="updated_at", direction="desc", user_id=Depends(get_user_id)):

    return get_user_words(user_id)

