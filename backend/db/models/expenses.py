from ..db import Base
from sqlalchemy import String, Integer, List, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Expenses(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallet.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))

    parents: Mapped[List['Teams','Users','Wallets','Categories']] = relationship(back_populates="income")


    def __repr__(self):
        return f"<Expenses(name='{self.name}', description='{self.description}', amount='{self.amount}', team_id='{self.team_id}', user_id='{self.user_id}', wallet_id='{self.wallet_id}', category_id='{self.category_id}')>"