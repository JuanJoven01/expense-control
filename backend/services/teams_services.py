from sqlalchemy import select

from fastapi.responses import JSONResponse

import json

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
    '''
    Filter in Users_Teams the pending invitations with the user_id
    if have repeated invitations, remove the duplicated,
    return the teams
    '''
    try:
        __delete_duplicated_invitations__()
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

def __delete_duplicated_invitations__():
    '''
    This function get the UsersTeams info, verify if get duplicated 
    invitations an remove that from the db
    '''
    try:
        with Session() as session:
            query = (
                select(Users_Teams)
                .where(Users_Teams.c.status == 'pending')
                    )
            invitations = session.execute(query).all()
        ######    
        to_remove = __get_duplicated__(invitations)
        with Session() as session:
            for item in to_remove:
                delete_query = Users_Teams.delete().where(Users_Teams.c.id == item)
                session.execute(delete_query)
                session.commit()   
    except Exception as e:
        raise e

def __get_duplicated__(list_with_repeated: list):
    dicts_of_invitations = [{str([item[1], item[2]]):item[0] } for item in list_with_repeated]
    dict_with_repeated = {}
    for dictionary in dicts_of_invitations:
        for key, value in dictionary.items():
            if key in dict_with_repeated:
                dict_with_repeated[key].append(value)
            else:
                dict_with_repeated[key] = [value]
    to_remove= []
    for value in dict_with_repeated.values():
        if len(value) > 1:
            for i in range(len(value)-1):
                to_remove.append(value[i])
    return to_remove

def accept_invitation(user_id: int, team_id: int):
    '''
    With the user_id and team_id, get the Users_Teams id
    changes the status to accept
    '''
    try:
        invitation_id = __get_invitation_id__(user_id, team_id)
        with Session() as session:
            update_query = (
                Users_Teams.update()
                .where(Users_Teams.c.id == invitation_id)
                .values(status='accepted')
            )
            session.execute(update_query)
            session.commit()
            return {'message':'Invitation Accepted'}
    except Exception as e:
        raise e

def __get_invitation_id__(user_id: int, team_id: int):
    try:
        with Session() as session:
            query = (
                select(Users_Teams)
                .where(Users_Teams.c.team_id == team_id)
                .where(Users_Teams.c.user_id == user_id)
                )
            
            return session.execute(query).scalar()
    except Exception as e:
        raise e 

def __verify_if_user_in_teams__(username:str, team_id:int):
    my_teams = get_my_teams(username)
    my_teams_str = my_teams.body.decode('utf-8')
    my_teams_dict = json.loads(my_teams_str)
    for team in my_teams_dict['teams']:
        if int(team['team_id']) == int(team_id):
            return True
    print('False')
    return False

