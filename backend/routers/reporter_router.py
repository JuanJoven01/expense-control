from fastapi import APIRouter, Depends

from middlewares.auth import JWTBearer

from services.reporter_services import get_incomes_per_category, get_just_values_per_cat, draw_donut_chart, get_expenses_per_category, get_team_incomes_per_category, get_team_expenses_per_category

reporter_router = APIRouter()

@reporter_router.get('/reporter/incomes',tags=['reporter'], dependencies=[Depends(JWTBearer())])
def get_own_incomes_per_category(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        incomes_per_category = get_incomes_per_category(user_id)
        incomes_per_category_just_values = get_just_values_per_cat(incomes_per_category)
        return draw_donut_chart(incomes_per_category_just_values)
    except Exception as e:
        return {'router error': str(e)}
    
@reporter_router.get('/reporter/expenses', tags=['reporter'], dependencies=[Depends(JWTBearer())])
def get_own_expenses_per_category(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        expenses_per_category = get_expenses_per_category(user_id)
        expenses_per_category_just_values = get_just_values_per_cat(expenses_per_category)
        return draw_donut_chart(expenses_per_category_just_values)
    except Exception as e:
        return {'router error': str(e)}

@reporter_router.get('/reporter/teams/incomes/{team_id}', tags=['reporter'], dependencies=[Depends(JWTBearer())])
def get_the_team_incomes_per_category(team_id:int, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        incomes_per_category = get_team_incomes_per_category(username, team_id)
        incomes_per_category_just_values = get_just_values_per_cat(incomes_per_category)
        print('==='*30)
        print(incomes_per_category)
        return draw_donut_chart(incomes_per_category_just_values)
    except Exception as e:
        return {'router error': str(e)}
    

@reporter_router.get('/reporter/teams/expenses/{team_id}', tags=['reporter'], dependencies=[Depends(JWTBearer())])
def get_the_team_expenses_per_category(team_id:int, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        expenses_per_category = get_team_expenses_per_category(username, team_id)
        expenses_per_category_just_values = get_just_values_per_cat(expenses_per_category)
        return draw_donut_chart(expenses_per_category_just_values)
    except Exception as e:
        return {'router error': str(e)}