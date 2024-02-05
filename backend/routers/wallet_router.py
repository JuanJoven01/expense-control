from fastapi import APIRouter, Depends
import json
from schemas.wallets_schemas import Wallets

from services.wallets_services import get_my_wallets_and_create_default, get_team_wallets_and_create_default, new_own_wallet, new_team_wallet_service
from services.teams_services import __verify_if_user_in_teams__

wallet_router = APIRouter ()

from middlewares.auth import JWTBearer

@wallet_router.get('/wallets/get', tags=['wallets'], dependencies=[Depends(JWTBearer())])
def get_my_wallets(jwt_payload = Depends(JWTBearer())):
    try:
        user_id = jwt_payload['user_id']
        return get_my_wallets_and_create_default(user_id)
    except Exception as e:
        raise e

@wallet_router.get('/wallet/teams/get/{team_id}', tags=['wallets'], dependencies=[Depends(JWTBearer())])
def get_team_wallet(team_id:int, jwt_payload = Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        if __verify_if_user_in_teams__(username, team_id): 
            return get_team_wallets_and_create_default(team_id)
        else : 
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

@wallet_router.post('/wallets/teams/new/{team_id}', tags=['wallets'], dependencies=[Depends(JWTBearer())])
def new_team_wallet(wallet:Wallets, team_id , jwt_payload =Depends(JWTBearer())):
    try:
        username = jwt_payload['user']
        name = wallet.name
        description = wallet.description or ''
        balance = wallet.balance or 0.0
        if __verify_if_user_in_teams__(username, team_id):
            print('*'*30)
            print('is near the service')
            return new_team_wallet_service(team_id, name, description, balance)
        else:
            return {'error': 'Invalid team_id, maybe you dont belong to the team'}
        
    except Exception as e:
        raise e
