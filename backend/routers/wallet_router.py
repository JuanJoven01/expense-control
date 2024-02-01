from fastapi import APIRouter, Depends
import json
from schemas.wallets_schemas import Wallets

from services.wallets_services import get_my_wallets_and_create_default, get_team_wallets_and_create_default, new_own_wallet
from services.teams_services import get_my_teams

wallet_router = APIRouter ()

from middlewares.auth import JWTBearer

@wallet_router.get('/wallets/get', tags=['wallets'], dependencies=[Depends(JWTBearer())])
def get_my_wallets(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        return get_my_wallets_and_create_default(user_id)
    except Exception as e:
        raise e

@wallet_router.get('/wallet/get-team/{team_id}', tags=['wallets'], dependencies=[Depends(JWTBearer())])
def get_team_wallet(team_id:int, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        my_teams = get_my_teams(username)
        json_str= my_teams.body.decode('utf-8')
        json_dict = json.loads(json_str)
        for team in json_dict['teams']:
            if team['team_id'] == team_id:
                return get_team_wallets_and_create_default(team_id)
        return {'message: Invalid team id'}
        
    except Exception as e:
        raise e
    
@wallet_router.post('/wallets/new', tags=['wallets'],dependencies=[Depends(JWTBearer())])
def new_wallet(wallet:Wallets, jwt_payload=Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        name = wallet.name
        description = wallet.description or ''
        balance = wallet.balance or 0.0
        return new_own_wallet(user_id, name, description, balance)
    except Exception as e:
        raise e
