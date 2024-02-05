from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

from schemas.categories_schemas import Categories, UpdateCategories

from services.categories_services import get_categories_or_create_default, new_own_category, update_own_category, get_team_categories_or_create_default, new_team_category, update_a_teams_categories

categories_router = APIRouter()


@categories_router.get('/categories/get', tags=['categories'], dependencies=[Depends(JWTBearer())])
def get_my_categories(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        return get_categories_or_create_default(user_id)

    except Exception as e:
        return {'router error': str(e)}


@categories_router.post('/categories/new', tags=['categories'], dependencies=[Depends(JWTBearer())])
def new_category(category: Categories, jwt_payload = Depends(JWTBearer())):
    try:
        category_name = category.name
        category_description = category.description
        user_id = jwt_payload['user_id']
        return new_own_category(category_name, category_description, user_id)


    except Exception as e:
        return {'router error': str(e)}
    
@categories_router.patch('/categories/update', tags=['categories'], dependencies=[Depends(JWTBearer())])
def update_category(category:UpdateCategories ,jwt_payload = Depends(JWTBearer())):
    try:
        name = category.name
        description = category.description
        category_id = category.id
        user_id = jwt_payload['user_id']
        return update_own_category(name, description, category_id, user_id)
    except Exception as e:
        return {'router error': str(e)}

@categories_router.get('/categories/teams/get/{team_id}', tags=['categories'], dependencies=[Depends(JWTBearer())])
def get_teams_categories(team_id, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        return get_team_categories_or_create_default(username, team_id)

    except Exception as e:
        return {'router error': str(e)}
    
@categories_router.post('/categories/teams/new/{team_id}', tags=['categories'], dependencies=[Depends(JWTBearer())])
def post_teams_categories(category: Categories,team_id, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        cat_name =  category.name
        cat_description = category.description
        return new_team_category(username, team_id, cat_name, cat_description)
    except Exception as e:
        return {'router error': str(e)}
    
@categories_router.patch('/categories/teams/update/{team_id}', tags=['categories'], dependencies=[Depends(JWTBearer())])
def update_teams_categories(category: UpdateCategories, team_id, jwt_payload= Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        cat_name = category.name
        cat_description = category.description
        cat_id =  category.id
        return update_a_teams_categories(username, team_id, cat_id, cat_name, cat_description)
    except Exception as e:
        return {'router error': str(e)}