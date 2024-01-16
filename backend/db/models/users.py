from ..db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    def __repr__(self):
        return f"<Users(username='{self.username}', password='{self.password}')>"