from db.models.models import Teams
from db.db import Session

def create_new_team (username: str, team_name: str):
    try:
        with Session() as session:
            team = Teams(admin=username, name=team_name)
            session.add(team)
            session.commit()
        return {'message': 'Team created'}
    except Exception as e:
        return {'error': e}