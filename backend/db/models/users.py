from ..db import Base
from sqlalchemy import String, List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    children: Mapped[List['Expenses','Income','Wallets']] = relationship(back_populates="teams")
    child: Mapped['Users'] = relationship(secondary='users_teams' ,back_populates="teams")

    def __repr__(self):
        return f"<Users(username='{self.username}', password='{self.password}')>"