from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

reporter_router = APIRouter()

@reporter_router.get('/reporter/expenses/category/{category_id}',tags=['reporter'], dependencies=[Depends(JWTBearer())])
def get_own_expenses_per_category(category_id:str, jwt_token = Depends(JWTBearer())):
    try:
        pass
    except Exception as e:
        return {'router error': str(e)}