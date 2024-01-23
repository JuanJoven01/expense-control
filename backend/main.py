from fastapi import FastAPI
from db.db import engine, Base


from db.models.models import Users, Expenses, Incomes, Wallets, Teams, Categories, Users_Teams


from middlewares.error_handler import ErrorHandler

from routers.users import users_router
from routers.teams import teams_router


app = FastAPI()


app.add_middleware(ErrorHandler)


app.include_router(users_router)
app.include_router(teams_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

