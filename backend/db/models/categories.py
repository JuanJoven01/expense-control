from ..db import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)


    def __repr__(self):
        return f"<Categories(name='{self.name}')>"