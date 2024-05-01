from datetime import datetime as dt

from sqlalchemy import MetaData, Table, Integer, Column, ForeignKey, Boolean, JSON, DateTime

metadata = MetaData()

boards = Table('boards', metadata,
               Column('id', Integer(), primary_key=True, autoincrement=True, unique=True),
               Column("size", Integer(), primary_key=True, nullable=False),
               Column("map", JSON(), nullable=False)
               )

games = Table('games', metadata,
              Column('id', Integer(), primary_key=True, autoincrement=True, unique=True),
              Column("points", Integer(), nullable=False),
              Column("is_win", Boolean(), default=False),
              Column("datetime", DateTime(), default=dt.now),
              Column("board_id", ForeignKey("boards.id"), default=None),
              )