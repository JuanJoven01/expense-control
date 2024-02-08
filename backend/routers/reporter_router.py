from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

reporter_router = APIRouter()

