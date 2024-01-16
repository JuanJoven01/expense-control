from ..db import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Income(Base):
    __tablename__ = 'income'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    wallet_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)



    def __repr__(self):
        return f"<Expenses(name='{self.name}', description='{self.description}', amount='{self.amount}', team_id='{self.team_id}', user_id='{self.user_id}', wallet_id='{self.wallet_id}', category_id='{self.category_id}')>"