from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from .routes import users, words
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )



app = FastAPI()

app.include_router(words.router, prefix="/api/v1/words", tags=["words"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/")
async def root():
    return {"message": "WELCOME TO MW"}


@app.get("/test")
async def get_test(token: str = Depends(oauth2_scheme)):

    return {"token": token}

print("Memorize Words Api started!!!")
