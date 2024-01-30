from sqlalchemy import select, insert

from fastapi.responses import JSONResponse

from db.models.models import Teams, Users_Teams, Users
from db.db import Session

from services.users_services import find_user_by_name

def get_team_id(team_name:str):
    '''
    Uses the unique attribute name on Teams to
    find and return team
    '''
    try:

        with Session() as session:
            query = (
                select(Teams)
                .where(Teams.name == team_name)
            )
            team = session.execute(query).scalar()
            return team if team else None
    except Exception as e:
        raise e

def create_new_team (admin: str, team_name: str, user_id: int):
    '''
    Create a new team in the table Teams with the username as admin
    and create the relation in Users_Tables
    '''
    try:
        if get_team_id(team_name):
            return {'error': 'Select another team name'}
        with Session() as session:
            team = Teams(admin=admin, name=team_name)
            session.add(team)
            session.commit()
        team_id = get_team_id(team_name).id
        with Session() as session:
            user_team_data = {'user_id': user_id, 'team_id': team_id, 'status':'accepted'}
            insert_smtp = Users_Teams.insert().values(**user_team_data)
            session.execute(insert_smtp)
            session.commit()
            # user_team = Users_Teams(user_id= user_id, team_id=team_id, status='accepted')
            # session.add(user_team)
            # session.commit()
        
        return {'message': 'Team created'}
    except Exception as e:
        raise e


def get_my_teams(username : str):
    '''
    This function receives as input a username, 
    find it with find username and get the teams related with username
    '''
    try:
        user = find_user_by_name(username)
        user_id = user.id
        with Session() as session:
            query = (
                select(Teams)
                .join(Users_Teams)
                .join(Teams.users)
                .where(Users.id==user_id, Users_Teams.c.status == 'accepted')
                    )
            teams = session.execute(query).scalars().all()
            team_data = [{"name": team.name, "admin": team.admin, 'team_id': team.id} for team in teams]
            return JSONResponse(content={'teams': team_data})
    except Exception as e:
        raise e


def create_invitation(second_username: str, team_id:str):
    '''
    Receives an username, and team id and create the request on Users_Teams
    with status pending 
    '''
    try:
        second_user = find_user_by_name(second_username)
        with Session() as session:
            user_team_data = {'user_id': second_user.id, 'team_id': team_id, 'status':'pending'}
            insert_smtp = Users_Teams.insert().values(**user_team_data)
            session.execute(insert_smtp)
            session.commit()
            return {'message': 'Invitation sended'}
    except Exception as e:
        raise e

def get_pending_invitations (user_id: int):
    print('into '*10)
    try:
        print('into '*10)
        with Session() as session:
            query = (
                select(Teams)
                .join(Users_Teams)
                .join(Teams.users)
                .where(Users.id==user_id, Users_Teams.c.status == 'pending')
                    )
            teams = session.execute(query).scalars().all()
            team_data = [{"name": team.name, "admin": team.admin, 'team_id': team.id} for team in teams]
            return JSONResponse(content={'teams': team_data})

    except Exception as e:
        raise e


def change_team_admin(new_admin: str, team_id):
    pass