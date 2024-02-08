from fastapi import FastAPI
from db.db import engine, Base


from db.models.models import Users, Expenses, Incomes, Wallets, Teams, Categories, Users_Teams


from middlewares.error_handler import ErrorHandler

from routers.users_router import users_router
from routers.teams_router import teams_router
from routers.wallet_router import wallet_router
from routers.categories_router import categories_router
from routers.incomes_router import incomes_router
from routers.expenses_router import expenses_router
from routers.reporter_router import reporter_router


app = FastAPI()


app.add_middleware(ErrorHandler)


app.include_router(users_router)
app.include_router(teams_router)
app.include_router(wallet_router)
app.include_router(categories_router)
app.include_router(incomes_router)
app.include_router(expenses_router)
app.include_router(reporter_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

