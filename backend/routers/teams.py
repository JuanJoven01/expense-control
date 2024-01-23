from fastapi import APIRouter, Depends
from schemas.teams import Teams

from services.teams import create_new_team

from middlewares.auth import JWTBearer


teams_router = APIRouter()


@teams_router.post("/teams/new", tags=["teams"], dependencies=[Depends(JWTBearer())])
def new_team(team: Teams, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        return create_new_team(username, team.name)
    except Exception as e :
        raise e

