from ..db import Base
from sqlalchemy import String, ForeignKey, Integer, Table, Column
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    children: Mapped[List['Expenses','Income']] = relationship(back_populates="categories")

class Expenses(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Integer, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallet.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))

    parents: Mapped[List['Teams','Users','Wallets','Categories']] = relationship(back_populates="expenses")

class Income(Base):
    __tablename__ = 'income'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Integer, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallet.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))

    parents: Mapped[List['Teams','Users','Wallets','Categories']] = relationship(back_populates="income")

class Teams(Base):

    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    admin: Mapped[str] = mapped_column(String(15), nullable=False)
    children: Mapped[List['Expenses','Income','Wallets']] = relationship(back_populates="users")
    child: Mapped['Users'] = relationship(secondary='users_teams' ,back_populates="users")

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    children: Mapped[List['Expenses','Income','Wallets']] = relationship(back_populates="users")
    child: Mapped['Teams'] = relationship(secondary='users_teams' ,back_populates="users")

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

Users_Teams = Table(
    'users_teams',
    Base.metadata,
    Column('team_id', ForeignKey('teams.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('status', String(15), nullable=False, default='pending')
)