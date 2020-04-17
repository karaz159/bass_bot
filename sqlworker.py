#!/usr/bin/python3
import logging

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from config import DB_DSN
from meta import BASE, Dude

ENGINE = create_engine(DB_DSN, echo=True)

BASE.metadata.create_all(ENGINE)
SESSION_FACTORY = sessionmaker(bind=ENGINE)

def register_dude(m):
    session = SESSION_FACTORY()
    dude = Dude(tg_user_id=m.chat.id,
                user_name=m.chat.username,
                first_name=m.chat.first_name)
    session.add(dude)
    session.commit()
    logging.info(f"registered dude with {dude.user_id} id!")
    session.close()

def get_user(tg_user_id):
    """
    Returns Dude row object
    """
    session = SESSION_FACTORY()
    dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
    session.close()
    return dude

def check_state(m, state):
    user = get_user(m.chat.id)
    if user:
        return user.curr_state == state # ОПАЧА, работает
    return False

def set_state(tg_user_id, value):
    """
    Saves current state of user.
    """
    session = SESSION_FACTORY()
    dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one()
    dude.curr_state = value
    session.commit()
    session.close()

def set_bool(tg_user_id, column, value=True):
    """
    Sets random power of bass flag
    True by default.
    """
    session = SESSION_FACTORY()
    dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one() # NOT_DRY
    if column == 'transform':
        dude.transform_eyed3 = not dude.transform_eyed3
    elif column == 'random':
        dude.random_bass = not dude.random_bass
    result = dude.random_bass
    session.commit()
    session.close()
    return result
