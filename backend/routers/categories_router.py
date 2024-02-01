from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

from schemas.categories_schemas import Categories

categories_router = APIRouter()

@categories_router.post('/categories/new', tags=['categories'], dependencies=[Depends(JWTBearer())])
def new_category(category: Categories, jwt_payload = Depends(JWTBearer())):
    try:
        category_name = category['name']
        category_description = category['description']
        print('*'*30)
        print(category_name)
        print(category_description)
        print(jwt_payload)
    except Exception as e:
        raise e