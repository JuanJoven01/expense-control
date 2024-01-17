from fastapi import FastAPI
from db.db import engine, Base

from db.models import Users, Expenses, Income, Wallets, Teams, Categories, Users_Teams


from routers.users import users_router

app = FastAPI()

app.include_router(users_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

