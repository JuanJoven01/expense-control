from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

from services.incomes_services import get_own_incomes, new_own_income, update_own_income

from schemas.incomes_schemas import Incomes, IncomesUpdate

incomes_router = APIRouter()


@incomes_router.get('/incomes/get', tags=['incomes'], dependencies=[Depends(JWTBearer())])
def get_incomes(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        return get_own_incomes(user_id)
    except Exception as e:
        return {'router error':str(e)}
    
@incomes_router.post('/incomes/new', tags=['incomes'], dependencies=[Depends(JWTBearer())])
def new_income(income:Incomes, jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        income_name = income.name
        income_description = income.description
        income_date = income.date
        amount = income.amount
        wallet_id = income.wallet_id
        category_id = income.category_id
        return new_own_income(user_id, income_name,income_description,income_date, amount,wallet_id, category_id)
    except Exception as e:
        return {'router error':str(e)}
    
@incomes_router.patch('/incomes/update', tags=['incomes'], dependencies=[Depends(JWTBearer())])
def update_income(income: IncomesUpdate, jwt_payload =  Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        income_name = income.name
        income_description = income.description
        income_date = income.date
        amount = income.amount
        wallet_id = income.wallet_id
        category_id = income.category_id
        income_id = income.income_id
        return update_own_income(user_id, income_name,income_description,income_date, amount,wallet_id, category_id, income_id)
    except Exception as e:
        return {'service error': str(e)}