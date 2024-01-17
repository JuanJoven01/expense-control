from fastapi import APIRouter

users_router = APIRouter()

@users_router.get("/users",tags=["users"])
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]