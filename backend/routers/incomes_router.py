from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

from services.incomes_services import get_own_incomes, new_own_income

from schemas.incomes_schemas import Incomes

incomes_router = APIRouter()


@incomes_router.get('/incomes/get', tags=['incomes'], dependencies=[Depends(JWTBearer())])
def get_incomes(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        return get_own_incomes(user_id)
    except Exception as e:
        raise e
    
@incomes_router.post('/incomes/new', tags=['incomes'], dependencies=[Depends(JWTBearer())])
def new_income(income:Incomes, jwe_payload = Depends(JWTBearer())):
    try:
        user_id = jwe_payload['user']
        print(income)

        return new_own_income(user_id)
    except Exception as e:
        raise e