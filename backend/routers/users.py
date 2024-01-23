from fastapi import APIRouter

from schemas.users import User

from services.users import new_user
from services.users import login_get_token

users_router = APIRouter()


@users_router.post("/signup",tags=["login"])
def signup(user: User):
    try:
        username = user.name
        password = user.password
        new_user(username, password)
        return {"message": "User created"}
    except Exception as e:
        return {"error": str(e)}
    
@ users_router.post("/login",tags=["login"])
def login(user: User):
    try:
        username = user.name
        password = user.password
        logged = login_get_token(username, password)
        if logged:
            return logged
        else:
            return {"error": "Invalid credentials"}
    except Exception as e:
        return {"error": str(e)}

