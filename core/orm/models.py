# coding: utf-8

# ---- Imports for ease of use while writing task
# from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, Date, ForeignKey, ForeignKeyConstraint, \
#    Integer, String, Table, Text, UniqueConstraint, Numeric, text, Enum


# ---- Import if you are going to be using postgresql JSONB type
# from sqlalchemy.dialects.postgresql import JSONB

# Needed for eager loading of joined tables
import datetime
import enum
import os
import time
from datetime import datetime as dt, timedelta as td

from sqlalchemy import BigInteger,  Integer, String, Text, Column, DateTime, ForeignKey, VARCHAR
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

Base = declarative_base()
metadata = Base.metadata


class Defender(Base):
    __tablename__ = 'defenders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(Text, nullable=False, unique=True)

    attack_points_generated = Column(BigInteger, nullable=False, default=0)
    defense_points_generated = Column(BigInteger, nullable=False, default=0)

    tower_id = Column(Integer, ForeignKey('towers.id'), nullable=False)
    tower = relationship("Tower", back_populates="defenders")

class Tower(Base):
    __tablename__ = 'towers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(12))
    healt = Column(BigInteger, nullable=False, default=0)
    defense = Column(BigInteger, nullable=False, default=0)
    defender_count = Column(BigInteger, nullable=False, default=0)
    
    round_id = Column(Integer, nullable=False)

    # round_id = Column(Integer, ForeignKey('rounds.id'), nullable=True)
    # round = relationship("Round", backref="towers")

    defenders = relationship("Defender", back_populates='tower')


class Round(Base):
    __tablename__ = 'rounds'

    id = Column(Integer, primary_key=True, autoincrement=True)
   
    time_created = Column(DateTime, default=datetime.datetime.now)

    global_defender_count = Column(BigInteger, nullable=False, default=0)

    hocus_tower_id = Column(Integer, ForeignKey('towers.id'), nullable=True)
    pocus_tower_id = Column(Integer, ForeignKey('towers.id'), nullable=True)

    hocus_tower = relationship("Tower", foreign_keys=[hocus_tower_id], backref="hocus")
    pocus_tower = relationship("Tower", foreign_keys=[pocus_tower_id], backref="pocus")



