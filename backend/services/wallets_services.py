from sqlalchemy import select

from fastapi.responses import JSONResponse


from db.models.models import Wallets, Users
from db.db import Session

def get_my_wallets_and_create_default(user_id:int):
    '''
    Get the wallets for an User, if this have not got wallets too
    created a default wallet cash
    '''
    try:
        with Session() as session:
            wallets_data = session.query(Wallets).filter_by(user_id=user_id).all()
            if wallets_data == []:
                with Session() as session:
                    new_wallet_cash = Wallets(name='Cash', description='Account for cash only', balance= 0.00, user_id=user_id)
                    session.add(new_wallet_cash)
                    session.commit()
                wallets_data = session.query(Wallets).filter_by(user_id=user_id).all()
            wallets_dict = [{'id':wallet.id,'name':wallet.name,'description':wallet.description,'balance':wallet.balance}for wallet in wallets_data]
            wallets_json = JSONResponse(content={'wallets': wallets_dict})
            return wallets_json 

    except Exception as e:
        raise e
    
def get_team_wallets_and_create_default(team_id: int):
    '''
    Get the wallets for an User, if this have not got wallets too
    created a default wallet cash
    '''
    try:
        with Session() as session:
            wallets_data = session.query(Wallets).filter_by(team_id=team_id).all()
            if wallets_data == []:
                with Session() as session:
                    new_wallet_cash = Wallets(name='Cash', description='Account for cash only', balance= 0.00, team_id=team_id)
                    session.add(new_wallet_cash)
                    session.commit()
                wallets_data = session.query(Wallets).filter_by(team_id=team_id).all()
            wallets_dict = [{'id':wallet.id,'name':wallet.name,'description':wallet.description,'balance':wallet.balance}for wallet in wallets_data]
            wallets_json = JSONResponse(content={'wallets': wallets_dict})
            return wallets_json 

    except Exception as e:
        raise e

def new_own_wallet(user_id: int, name:str, description:str = '', balance:float = 0.0):
    try:
        with Session() as session:
            wallet = Wallets(user_id=user_id, name=name, description=description, balance=balance)
            session.add(wallet)
            session.commit()
            return {'message': 'Wallet created'}
    except Exception as e:
        raise e