from ..db import Base
from sqlalchemy import String, ForeignKey, Integer, Table, Column, Float
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    expenses: Mapped[List['Expenses']] = relationship(back_populates="category")
    incomes: Mapped[List['Incomes']] = relationship(back_populates="category")
    user: Mapped['Users'] = relationship(back_populates="category")


class Expenses(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100),nullable=True),
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
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
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallets.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    team: Mapped['Teams'] = relationship(back_populates="incomes")
    user: Mapped['Users'] = relationship(back_populates="incomes")
    wallet: Mapped['Wallets'] = relationship(back_populates="incomes")
    category: Mapped['Categories'] = relationship(back_populates="incomes")


class Teams(Base):

    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    admin: Mapped[str] = mapped_column(String(15), nullable=False)
    #####
    expenses: Mapped[List['Expenses']] = relationship(back_populates="team")
    incomes: Mapped[List['Incomes']] = relationship(back_populates="team")
    wallets: Mapped[List['Wallets']] = relationship(back_populates="team")
    users: Mapped[List['Users']] = relationship(secondary='users_teams' ,back_populates="teams")


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    expenses: Mapped[List['Expenses']] = relationship(back_populates="user")
    incomes: Mapped[List['Incomes']] = relationship(back_populates="user")
    wallets: Mapped[List['Wallets']] = relationship(back_populates="user")
    teams: Mapped[List['Teams']] = relationship(secondary='users_teams' ,back_populates="users")
    Categories: Mapped[List['Categories']] = relationship(back_populates="user")


class Wallets(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    ####
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    team: Mapped['Teams'] = relationship(back_populates="wallets")
    user: Mapped['Users'] = relationship(back_populates="wallets")
    expenses: Mapped[List['Expenses']] = relationship(back_populates="wallet")
    incomes: Mapped[List['Incomes']] = relationship(back_populates="wallet")


Users_Teams = Table(
    'users_teams',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('team_id', ForeignKey('teams.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('status', String(15), nullable=False, default='pending')
)