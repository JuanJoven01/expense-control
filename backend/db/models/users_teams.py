from ..db import Base
from sqlalchemy import String, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


Users_Teams = Table(
    'users_teams',
    Base.metadata,
    Column('team_id', ForeignKey('teams.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('status', String(15), nullable=False, default='pending')
)