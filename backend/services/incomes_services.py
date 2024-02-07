from datetime import datetime

from sqlalchemy import select

from db.db import Session

from db.models.models import Incomes

from services.sql_services import to_dict

from services.teams_services import __verify_if_user_in_teams__

def get_own_incomes(user_id:int):
    try:
        with Session() as session:
            query = (
                select(Incomes)
                .where(Incomes.user_id == user_id)
                )

        incomes = session.execute(query).scalars().all()
        return incomes
    except Exception as e:
        return {'service error':str(e)}
    
def new_own_income(user_id:int, name:str, description:str, datetime: datetime, amount: float, wallet_id:int, category_id: int):
    try:
        with Session() as session:
            income = Incomes(name= name, description=description, amount= amount, datetime= datetime, user_id=user_id, wallet_id=wallet_id,category_id=category_id)
            session.add(income)
            session.commit()
        return  {'message':'income created'}
    except Exception as e:
        return {'service error':str(e)}

def update_own_income(user_id:int, name:str, description:str, datetime: datetime, amount: float, wallet_id:int, category_id: int, income_id:int):
    try:
        raw_incomes =  get_own_incomes(user_id)
        incomes = [to_dict(income) for income in raw_incomes]
        for income in incomes:
            if income['id'] == income_id:
                with Session() as session:
                    update_query = (
                        select(Incomes)
                        .where(Incomes.id == income_id)
                    )
                    income_to_update = session.execute(update_query).scalar()
                    income_to_update.name = name
                    income_to_update.description = description
                    income_to_update.datetime = datetime
                    income_to_update.amount = amount
                    income_to_update.wallet_id = wallet_id
                    income_to_update.category_id = category_id
                    session.commit()
                return {'message':'income updated'}
        return {'error': "looks like it's not your income"}
    except Exception as e:
        return {'service error': str(e)}
    
def delete_own_income(income_id:int, user_id:int):
    try:
        raw_incomes =  get_own_incomes(user_id)
        incomes = [to_dict(income) for income in raw_incomes]
        for income in incomes:
            if income['id'] == income_id:
                with Session() as session:
                    income = session.get(Incomes, income_id)
                    session.delete(income)
                    session.commit()
                    return {'message':'income removed'}
        return {'error': "looks like it's not your income"}
                    
    except Exception as e:
        return {'service error': str(e)}
    
def get_team_incomes(username:str, team_id: int):
    try:
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                query = (
                    select(Incomes)
                    .where(Incomes.team_id==team_id)
                )
                incomes = session.execute(query).scalars().all()
                incomes_list = [to_dict(income) for income in incomes]
                return incomes_list
        return {'error': 'looks like you are not bellow to the team'}
    except Exception as e:
        return {'service error': str(e)}
    

def new_team_incomes(username:str, team_id:int, income:dict):
    try:
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                new_income = Incomes(name=income.name, description=income.description, amount=income.amount, datetime=income.date, team_id=team_id, wallet_id=income.wallet_id, category_id=income.category_id)
                session.add(new_income)
                session.commit()
                return {'message':'income added'}
        return {'error': 'looks like you are not bellow to the team'}    

    except Exception as e:
        return {'service error': str(e)}
    
def update_team_incomes(username: str, team_id: int, income:dict):
    try:
        current_incomes = get_team_incomes(username, team_id)
        for current_income in current_incomes:
            if current_income['id'] == income.income_id:
                with Session() as session:
                    update_query = (
                        select(Incomes)
                        .where(Incomes.id == income.income_id)
                    )
                    income_to_update = session.execute(update_query).scalar()
                    income_to_update.name = income.name
                    income_to_update.description = income.description
                    income_to_update.amount = income.amount
                    income_to_update.datetime = income.date
                    income_to_update.wallet_id = income.wallet_id
                    income_to_update.category_id = income.category_id
                    session.commit()
                    return {'message': 'income updated'}
        return {'error': "looks like it's not your income"} 

    except Exception as e:
        return {'service error': str(e)}
    
def delete_team_incomes(username: str, team_id:int, income_id:int):
    try:
        incomes = get_team_incomes(username, team_id)
        for income in incomes:
            if income['id'] == income_id:
                with Session() as session:
                    income_to_delete = session.get(Incomes, income_id)
                    session.delete(income_to_delete)
                    session.commit()
                    return {'message':'income removed'}
        return {'error': "looks like it's not your income"} 
    except Exception as e:
        return {'service error': str(e)}