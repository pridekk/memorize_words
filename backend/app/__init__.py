from fastapi import FastAPI
from .routers import users, words

app = FastAPI()

app.include_router(words.router, prefix="/api/v1/words", tags=["words"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "WELCOME TO MW"}


print("Memorize Words Api started!!!")
