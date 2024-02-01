from sqlalchemy import select

from db.db import Session

from db.models.models import Incomes

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
        raise e
    
def new_own_income(user_id:int):
    pass