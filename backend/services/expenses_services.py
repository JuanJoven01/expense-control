from datetime import datetime

from sqlalchemy import select

from db.db import Session

from db.models.models import Expenses

from services.sql_services import to_dict

from services.teams_services import __verify_if_user_in_teams__

from services.wallets_services import __update_wallet_balance__

def get_own_expenses(user_id:int):
    try:
        with Session() as session:
            query = (
                select(Expenses)
                .where(Expenses.user_id == user_id)
                )

        expenses = session.execute(query).scalars().all()
        return expenses
    except Exception as e:
        return {'service error':str(e)}
    
def new_own_expense(user_id:int, name:str, description:str, datetime: datetime, amount: float, wallet_id:int, category_id: int):
    try:
        with Session() as session:
            expense = Expenses(name= name, description=description, amount= amount, datetime= datetime, user_id=user_id, wallet_id=wallet_id,category_id=category_id)
            session.add(expense)
            session.commit()
        __update_wallet_balance__(True, wallet_id, amount)
        return  {'message':'expense created'}
    except Exception as e:
        return {'service error':str(e)}

def update_own_expense(user_id:int, name:str, description:str, datetime: datetime, amount: float, wallet_id:int, category_id: int, expense_id:int):
    try:
        raw_expenses =  get_own_expenses(user_id)
        expenses = [to_dict(expense) for expense in raw_expenses]
        for expense in expenses:
            if expense['id'] == expense_id:
                with Session() as session:
                    update_query = (
                        select(Expenses)
                        .where(Expenses.id == expense_id)
                    )
                    expense_to_update = session.execute(update_query).scalar()
                    value_in_wallet = expense_to_update.amount - amount
                    __update_wallet_balance__(False, wallet_id, value_in_wallet)
                    expense_to_update.name = name
                    expense_to_update.description = description
                    expense_to_update.datetime = datetime
                    expense_to_update.amount = amount
                    expense_to_update.wallet_id = wallet_id
                    expense_to_update.category_id = category_id
                    session.commit()
                return {'message':'expense updated'}
        return {'error': "looks like it's not your expense"}
    except Exception as e:
        return {'service error': str(e)}
    
def delete_own_expense(expense_id:int, user_id:int):
    try:
        raw_expenses =  get_own_expenses(user_id)
        expenses = [to_dict(expense) for expense in raw_expenses]
        for expense in expenses:
            if expense['id'] == expense_id:
                with Session() as session:
                    expense = session.get(Expenses, expense_id)
                    session.delete(expense)
                    session.commit()
                    return {'message':'expense removed'}
        return {'error': "looks like it's not your expense"}
                    
    except Exception as e:
        return {'service error': str(e)}
    
def get_team_expenses(username:str, team_id: int):
    try:
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                query = (
                    select(Expenses)
                    .where(Expenses.team_id==team_id)
                )
                expenses = session.execute(query).scalars().all()
                expenses_list = [to_dict(expense) for expense in expenses]
                return expenses_list
        return {'error': 'looks like you are not bellow to the team'}
    except Exception as e:
        return {'service error': str(e)}
    

def new_team_expenses(username:str, team_id:int, expense:dict):
    try:
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                new_expense = Expenses(name=expense.name, description=expense.description, amount=expense.amount, datetime=expense.date, team_id=team_id, wallet_id=expense.wallet_id, category_id=expense.category_id)
                session.add(new_expense)
                session.commit()
            __update_wallet_balance__(True, expense.wallet_id, expense.amount)
            return {'message':'expense added'}
        return {'error': 'looks like you do not bellow to the team'}    
    except Exception as e:
        return {'service error': str(e)}
    
def update_team_expenses(username: str, team_id: int, expense:dict):
    try:
        current_expenses = get_team_expenses(username, team_id)
        for current_expense in current_expenses:
            if current_expense['id'] == expense.expense_id:
                with Session() as session:
                    update_query = (
                        select(Expenses)
                        .where(Expenses.id == expense.expense_id)
                    )
                    expense_to_update = session.execute(update_query).scalar()
                    value_to_update = expense_to_update.amount - expense.amount
                    __update_wallet_balance__(False, expense.wallet_id, value_to_update)
                    expense_to_update.name = expense.name
                    expense_to_update.description = expense.description
                    expense_to_update.amount = expense.amount
                    expense_to_update.datetime = expense.date
                    expense_to_update.wallet_id = expense.wallet_id
                    expense_to_update.category_id = expense.category_id
                    session.commit()
                return {'message': 'expense updated'}
        return {'error': "looks like it's not your expense"} 

    except Exception as e:
        return {'service error': str(e)}
    
def delete_team_expenses(username: str, team_id:int, expense_id:int):
    try:
        expenses = get_team_expenses(username, team_id)
        for expense in expenses:
            if expense['id'] == expense_id:
                with Session() as session:
                    expense_to_delete = session.get(Expenses, expense_id)
                    session.delete(expense_to_delete)
                    session.commit()
                    return {'message':'expense removed'}
        return {'error': "looks like it's not your expense"} 
    except Exception as e:
        return {'service error': str(e)}