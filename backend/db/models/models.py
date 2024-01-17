from ..db import Base
from sqlalchemy import String, ForeignKey, Integer, Table, Column, Float
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)

    expenses: Mapped[List['Expenses']] = relationship(back_populates="categories")
    income: Mapped[List['Incomes']] = relationship(back_populates="categories")

class Expenses(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallets.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    team: Mapped['Teams'] = relationship(back_populates="expenses")
    user: Mapped['Users'] = relationship(back_populates="expenses")
    wallet: Mapped['Wallets'] = relationship(back_populates="expenses")
    category: Mapped['Categories'] = relationship(back_populates="expenses")

class Incomes(Base):
    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallets.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    team: Mapped['Teams'] = relationship(back_populates="incomes")
    user: Mapped['Users'] = relationship(back_populates="incomes")
    wallet: Mapped['Wallets'] = relationship(back_populates="incomes")
    category: Mapped['Categories'] = relationship(back_populates="incomes")


class Teams(Base):

    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    admin: Mapped[str] = mapped_column(String(15), nullable=False)
    expenses: Mapped[List['Expenses']] = relationship(back_populates="teams")
    income: Mapped[List['Incomes']] = relationship(back_populates="teams")
    wallets: Mapped[List['Wallets']] = relationship(back_populates="teams")
    users: Mapped[List['Users']] = relationship(secondary='users_teams' ,back_populates="teams")


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    expenses: Mapped[List['Expenses']] = relationship(back_populates="users")
    income: Mapped[List['Incomes']] = relationship(back_populates="users")
    wallets: Mapped[List['Wallets']] = relationship(back_populates="users")
    teams: Mapped[List['Teams']] = relationship(secondary='users_teams' ,back_populates="users")

class Wallets(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    ####
    expenses: Mapped[List['Expenses']] = relationship(back_populates="wallets")
    income: Mapped[List['Incomes']] = relationship(back_populates="wallets")

    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    team: Mapped['Teams'] = relationship(back_populates="wallets")
    user: Mapped['Users'] = relationship(back_populates="wallets")


Users_Teams = Table(
    'users_teams',
    Base.metadata,
    Column('team_id', ForeignKey('teams.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('status', String(15), nullable=False, default='pending')
)