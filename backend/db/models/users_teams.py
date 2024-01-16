from ..db import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Users_Teams(Base):
    __tablename__ = 'users_teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(15), nullable=False, default='pending')
    ####
    team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Users_Teams(status='{self.status}', team_id='{self.team_id}', user_id='{self.user_id}')>"