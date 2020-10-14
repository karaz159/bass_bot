"""
Module that represents
metadata of DUDES in db
States and Answers
"""
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class States:
    start = 'start'
    asking_for_stuff = 'asking_for_stuff'
    asking_bass_pwr = 'asking_bass_pwr'
    downloading = 'downloading'
    boosting = 'boosting'


class Dude(BASE):
    """
    Main dude sqlalchemy class
    """
    __tablename__ = "dudes"

    user_id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, unique=True)
    user_name = Column(String)
    curr_state = Column(String, server_default=States.start)  # TODO enum
    last_source = Column(String, unique=True)
    random_bass = Column(Boolean, default=False)
    transform_eyed3 = Column(Boolean, default=True)
    last_message_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    first_message_date = Column(DateTime, server_default=func.now())

