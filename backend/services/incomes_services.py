from datetime import datetime

from sqlalchemy import select

from db.db import Session

from db.models.models import Incomes

from services.sql_services import to_dict

def get_own_incomes(user_id:int):
    try:
        with Session() as session:
            query = (
                select(Incomes)
                .where(Incomes.user_id == user_id)
                )

        incomes = session.execute(query).scalars().all()
        return incomes
    except Exception as e:
        return {'service error':str(e)}
    
def new_own_income(user_id:int, name:str, description:str, datetime: datetime, amount: float, wallet_id:int, category_id: int):
    try:
        with Session() as session:
            income = Incomes(name= name, description=description, amount= amount, datetime= datetime, user_id=user_id, wallet_id=wallet_id,category_id=category_id)
            session.add(income)
            session.commit()
        return  {'message':'income created'}
    except Exception as e:
        return {'service error':str(e)}

def update_own_income(user_id:int, name:str, description:str, datetime: datetime, amount: float, wallet_id:int, category_id: int, income_id:int):
    try:
        raw_incomes =  get_own_incomes(user_id)
        incomes = [to_dict(income) for income in raw_incomes]
        for income in incomes:
            if income['id'] == income_id:
                with Session() as session:
                    update_query = (
                        select(Incomes)
                        .where(Incomes.id == income_id)
                    )
                    income_to_update = session.execute(update_query).scalar()
                    print('='*30)
                    print(income_to_update)
                    income_to_update.name = name
                    income_to_update.description = description
                    income_to_update.datetime = datetime
                    income_to_update.amount = amount
                    income_to_update.wallet_id = wallet_id
                    income_to_update.category_id = category_id
                    session.commit()
                return {'message':'income updated'}
        return {'error': "looks like it's not your income"}
    except Exception as e:
        return {'service error': str(e)}