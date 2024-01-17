from ..db import Base
from sqlalchemy import String, List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Teams(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    admin: Mapped[str] = mapped_column(String(15), nullable=False)
    children: Mapped[List['Expenses','Income','Wallets']] = relationship(back_populates="users")
    child: Mapped['Teams'] = relationship(secondary='users_teams' ,back_populates="users")


    def __repr__(self):
        return f"<Teams(name='{self.name}', admin='{self.admin}')>"