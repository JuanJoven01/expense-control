from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

from services.expenses_services import get_own_expenses, new_own_expense, update_own_expense, delete_own_expense, get_team_expenses,new_team_expenses, update_team_expenses, delete_team_expenses

from schemas.expenses_schemas import Expenses, ExpensesUpdate

expenses_router = APIRouter()


@expenses_router.get('/expenses/get', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def get_expenses(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        return get_own_expenses(user_id)
    except Exception as e:
        return {'router error':str(e)}
    
@expenses_router.post('/expenses/new', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def new_expense(expense:Expenses, jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        expense_name = expense.name
        expense_description = expense.description
        expense_date = expense.date
        amount = expense.amount
        wallet_id = expense.wallet_id
        category_id = expense.category_id
        return new_own_expense(user_id, expense_name,expense_description,expense_date, amount,wallet_id, category_id)
    except Exception as e:
        return {'router error':str(e)}
    
@expenses_router.patch('/expenses/update', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def update_expense(expense: ExpensesUpdate, jwt_payload =  Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        expense_name = expense.name
        expense_description = expense.description
        expense_date = expense.date
        amount = expense.amount
        wallet_id = expense.wallet_id
        category_id = expense.category_id
        expense_id = expense.expense_id
        return update_own_expense(user_id, expense_name,expense_description,expense_date, amount,wallet_id, category_id, expense_id)
    except Exception as e:
        return {'service error': str(e)}
    
@expenses_router.delete('/expenses/delete/{eid}', tags=['expenses'],dependencies=[Depends(JWTBearer())])
def delete_expense(eid: int, jwt_payload = Depends(JWTBearer())):
    try:
        return delete_own_expense(eid, jwt_payload['user_id'])
    except Exception as e:
        return {'router error': str(e)}
    
@expenses_router.get('/expenses/teams/get/{team_id}', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def get_teams_expenses(team_id:int, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        return get_team_expenses(username, team_id)
    except Exception as e:
        return {'router error': str(e)}
    
@expenses_router.post('/expenses/teams/new/{team_id}', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def new_teams_expenses(team_id, expense:Expenses, jwt_payload=Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        return new_team_expenses(username, team_id, expense)
    except Exception as e:
        return {'router error': str(e)}
    
@expenses_router.patch('/expenses/teams/patch/{team_id}', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def update_teams_expenses(team_id, expense: ExpensesUpdate, jwt_payload= Depends(JWTBearer())):
    try:
       username = jwt_payload['user']
       return  update_team_expenses( username, team_id, expense)

    except Exception as e:
        return {'router error': str(e)}
    
@expenses_router.delete('/expenses/teams/remove/teams/{team_id}/{expense_id}', tags=['expenses'], dependencies=[Depends(JWTBearer())])
def delete_teams_expenses(team_id:int, expense_id:int, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        return delete_team_expenses(username, team_id, expense_id)
    except Exception as e:
        return {'router error': str(e)}