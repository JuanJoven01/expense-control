from fastapi import APIRouter, Depends
from schemas.teams import Teams

from middlewares.auth import JWTBearer


teams_router = APIRouter()


@teams_router.post("/teams/new", tags=["teams"], dependencies=[Depends(JWTBearer())])
def new_team(team: Teams, jwt_payload = Depends(JWTBearer())):
    print(jwt_payload)

