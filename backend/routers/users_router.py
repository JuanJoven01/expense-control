from fastapi import APIRouter

from schemas.users_schemas import User

from services.users_services import new_user, login_get_token, find_user_by_name

users_router = APIRouter()


@users_router.post("/signup",tags=["login"])
def signup(user: User):
    try:
        username = user.name
        password = user.password
        if find_user_by_name(username):
            return {'error': 'invalid username, try another'}
        new_user(username, password)
        return {"message": "User created"}
    except Exception as e:
        return {"error": str(e)}
    
@ users_router.post("/login",tags=["login"])
def login(user: User):
    try:
        username = user.name
        password = user.password
        token = login_get_token(username, password)
        if token:
            return token
        else:
            return {"error": "Invalid credentials"}
    except Exception as e:
        return {"error": str(e)}

