from ..db import Base
from sqlalchemy import String, List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    children: Mapped[List['Expenses','Income']] = relationship(back_populates="categories")


    def __repr__(self):
        return f"<Categories(name='{self.name}')>"