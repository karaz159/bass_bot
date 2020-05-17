#!/usr/bin/python3
'''
Module contains all functions that
in some way relative to sql
'''
from datetime import datetime
from time import sleep
from contextlib import contextmanager

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from config import DB_DSN, log
from meta import BASE, Dude

ENGINE = create_engine(DB_DSN)
print('connecting to db ...', end='')

while True:
    try:
        BASE.metadata.create_all(ENGINE)
        break
    except exc.OperationalError:
        sleep(5)

SESSION_FACTORY = sessionmaker(bind=ENGINE)
print('ok!')

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SESSION_FACTORY()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def register_dude(message) -> None:
    '''
    Register user from message
    '''
    dude = Dude(tg_user_id=message.chat.id,
                user_name=message.chat.username,
                first_name=message.chat.first_name)
    with session_scope() as session:
        session.add(dude)
        log.info(f"registered dude {message.chat.username} "
                 f"with {dude.user_id} id!")

def get_user(tg_user_id, session=None):
    """
    Returns Dude row object
    """
    if not session:
        with session_scope() as ses:
            dude = ses.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
            ses.expunge_all()
    else:
        dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
    return dude

def check_state(tg_user_id, state) -> bool:
    '''
    checks state of user
    '''
    with session_scope() as session:
        user = get_user(tg_user_id, session=session)
        if user:
            return user.curr_state == state
    return False

def set_column(tg_user_id, state=None, last_src=None):
    """
    Saves current state of user.
    """
    with session_scope() as session:
        dude = get_user(tg_user_id, session=session)
        if state:
            dude.curr_state = state
        if last_src:
            dude.last_source = last_src

def alt_bool(tg_user_id, transform=None, random=None):
    # TODO Объеденить мб с верхней функцией?
    """
    Alts bool of transform or random column
    """
    with session_scope() as session:
        dude = get_user(tg_user_id, session=session)
        if transform:
            dude.transform_eyed3 = not dude.transform_eyed3
            result = dude.transform_eyed3
        if random:
            dude.random_bass = not dude.random_bass
            result = dude.random_bass
    return result

def listener(messages):
    """
    listener function
    that logs message to file
    and updates last_message column in db # NOT_DRY
    """
    for message in messages:
        if message.text:
            log.info(f'{message.chat.username} - {message.text}')
        elif message.voice:
            log.info(f'{message.chat.username} - sended voice')
        elif message.audio:
            log.info(f'{message.chat.username} - sended audio')
        elif message.document:
            log.info(f'{message.chat.username} - sended document,'
                     ' which we dont support yet')
        with session_scope() as session:
            dude = get_user(message.chat.id, session=session)
            if dude:
                dude.last_message_date = datetime.utcnow()
            else:
                register_dude(message) # ЕСЛИ КТО ТО НЕ ЗАРЕГАН ПО БАЗЕ НО УЖЕ ПОЛЬЗОВАТЕЛЬ
