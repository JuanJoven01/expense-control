from ..db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Teams(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    admin: Mapped[str] = mapped_column(String(15), nullable=False)

    def __repr__(self):
        return f"<Teams(name='{self.name}', admin='{self.admin}')>"