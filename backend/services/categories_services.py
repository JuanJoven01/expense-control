from db.db import Session

from sqlalchemy import select

from db.models.models import Categories

from services.sql_services import to_dict

from services.teams_services import __verify_if_user_in_teams__


def get_categories_or_create_default(the_user_id:int):
    try:
        with Session() as session:
            query = (
                select(Categories)
                .where(Categories.user_id == the_user_id)
            )
            categories = session.execute(query).scalars().all()
        if categories == []:
            default_categories = ['Home','Family','Pet','Work']
            with Session() as session:
                for category in default_categories:
                    add_query = Categories(name=category, description=f'{category} category',user_id = the_user_id)
                    session.add(add_query)
                    session.commit()
            query = (
                select(Categories)
                .where(Categories.user_id == the_user_id)
            )
            categories = session.execute(query).scalars().all()
        return categories
            
    except Exception as e:
        return {'service error': str(e)}
    

def new_own_category(name:str, description:str, user_id:int):
    try:
        with Session() as session:
            category = Categories(name= name, description = description, user_id = user_id)
            session.add(category)
            session.commit()
            return {'message':'category created'}
    except Exception as e:
        return {'service error': str(e)}


def update_own_category(name,description,category_id,user_id):
    try:
        if __verify_if_category_belongs_to_user(category_id, user_id):
            with Session() as session:
                query = (
                    select(Categories)
                    .where(Categories.id == category_id)
                )
                category = session.execute(query).scalar()
                if name: category.name = name
                if description: category.description = description
                session.commit()
            return {'message': 'category updated'}
        else: 
            return {'error':'error in category, make sure is a valid category'}

    except Exception as e:
        return {'service error': str(e)}


def get_team_categories_or_create_default(username:str, team_id: int):
    try:
        if __verify_if_user_in_teams__(username,team_id):
            with Session() as session:
                query = (
                    select(Categories)
                    .where(Categories.team_id == team_id)
                )
                categories = session.execute(query).scalars().all()
            if categories == []:
                default_categories = ['Home','Family','Pet','Work']
                with Session() as session:
                    for category in default_categories:
                        add_query = Categories(name= category, description=f'{category} category', team_id= team_id)
                        session.add(add_query)
                        session.commit()
                    query = (
                    select(Categories)
                    .where(Categories.team_id == team_id)
                    )
                    categories = session.execute(query).scalars().all()
            return [to_dict(cat) for cat in categories]
        else:
            return {'error': 'verify if user belongs to the team'}

    except Exception as e:
        return {'service error': str(e)}


def new_team_category(username:str, team_id:int, cat_name:str, cat_description:str):
    try:
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                category = Categories(name= cat_name, description = cat_description, team_id = team_id )
                session.add(category)
                session.commit()
            return {'message': 'category created'}
        return {'error': 'verify if user belongs to the team'}
    except Exception as e:
        return {'service error': str(e)}


def update_a_teams_categories(username:str, team_id:int, cat_id: int, cat_name:str, cat_description:str):
    try:
        if __verify_if_category_belongs_to_team(username, cat_id, team_id):
            with Session() as session:
                query = (
                    select(Categories)
                    .where(Categories.id == cat_id)
                )
                category = session.execute(query).scalar()
                if cat_name: category.name = cat_name
                if cat_description: category.description = cat_description
                session.commit()
            return {'message': 'category updated'}
        return {'error': 'verify if the category id is correct'}

    except Exception as e:
        return {'service error': str(e)}

def __verify_if_category_belongs_to_user(category_id:int,user_id:int):
    my_categories = get_categories_or_create_default(user_id)
    my_categories_dict = [to_dict(category) for category in my_categories]
    for category in my_categories_dict:
        if category['id'] == category_id:
            return True
    return False

def __verify_if_category_belongs_to_team(username:str,category_id:int, team_id:int):
    team_categories = get_team_categories_or_create_default(username,team_id)
    print('*'*30)
    print('here')
    print(team_categories)
    for category in team_categories:
        if category['id'] == category_id:
            return True
    return False

