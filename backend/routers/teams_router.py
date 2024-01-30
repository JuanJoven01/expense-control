from fastapi import APIRouter, Depends

from schemas.teams_schemas import Teams, Username_and_team_id, TeamName

from services.teams_services import create_new_team, get_my_teams, create_invitation, get_pending_invitations

from middlewares.auth import JWTBearer


teams_router = APIRouter()


@teams_router.post("/teams/new", tags=["teams"], dependencies=[Depends(JWTBearer())])
def new_team(team: TeamName, jwt_payload = Depends(JWTBearer())):
    '''
    This endpoint create a new team and defines the creator as admin
    
    "Body_example": {
                "name": "family",
            }
    * The username is obtained from JWT
    '''
    try:
        admin_name = jwt_payload['user']
        admin_id = jwt_payload['user_id']
        return create_new_team(admin_name, team.name, admin_id)
    except Exception as e :
        raise e
    
@teams_router.get('/teams/get', tags=['teams'], dependencies=[Depends(JWTBearer())])
def get_teams(jwt_payload = Depends(JWTBearer())):
    '''
    This endpoint get all the teams from an user
    The username is obtained from JWT
    '''
    try:
        username = jwt_payload['user']
        return get_my_teams(username)

    except Exception as e:
        raise e


@teams_router.post('/teams/invite', tags=['teams'], dependencies=[Depends(JWTBearer())])
def invite_user_to_team(user_team:Username_and_team_id):
    '''
    This endpoint receives a team id and an username in the body and create a new
    column in Users_Teams with status pending
    '''
    try:
        second_username = user_team.name
        team_id = user_team.team_id
        return create_invitation(second_username, team_id)

    except Exception as e:
        raise e


@teams_router.get('/teams/invite/get', tags=['teams'], dependencies={Depends(JWTBearer())})
def get_invitations(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        invitations = get_pending_invitations(user_id)
        return invitations
        
    except Exception as e:
        raise e
    

@teams_router.patch('/teams/change-admin', tags=['teams'],dependencies=[Depends(JWTBearer())])
def update_team_admin(team: Teams, jwt_payload  = Depends(JWTBearer())):
    try:
        pass
    except Exception as e:
        raise e