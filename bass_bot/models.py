"""
Module that represents
metadata of DUDES in db
States and Answers
"""
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from data import States

BASE = declarative_base()


class Dude(BASE):
    """
    Main dude sqlalchemy class
    """
    __tablename__ = "dudes"

    user_id = Column(Integer, primary_key=True, nullable=False)
    tg_user_id = Column(Integer, unique=True)
    user_name = Column(String)
    first_name = Column(String)
    curr_state = Column(String, server_default=States.start, nullable=False)  # TODO enum
    random_bass = Column(Boolean, default=False, nullable=False)
    transform_eyed3 = Column(Boolean, default=True, nullable=False)
    last_message_date = Column(DateTime, server_default=func.now(), nullable=False, onupdate=func.now())
    first_message_date = Column(DateTime, server_default=func.now(), nullable=False)
    last_source = Column(String, unique=True)
