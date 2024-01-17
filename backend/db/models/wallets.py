from ..db import Base
from sqlalchemy import String, Integer,List, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Wallets(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    ####
    children: Mapped[List['Expenses','Income']] = relationship(back_populates="wallets")

    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    parents: Mapped[List['Teams','Users']] = relationship(back_populates="wallets")



    def __repr__(self):
        return f"<Wallets(name='{self.name}', description='{self.description}', balance='{self.balance}', team_id='{self.team_id}', user_id='{self.user_id}')>"