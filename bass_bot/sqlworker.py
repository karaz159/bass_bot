#!/usr/bin/python3
from datetime import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from config import DB_DSN, log
from meta import BASE, Dude

ENGINE = create_engine(DB_DSN)

BASE.metadata.create_all(ENGINE)
SESSION_FACTORY = sessionmaker(bind=ENGINE)

def register_dude(m):
    session = SESSION_FACTORY()
    dude = Dude(tg_user_id=m.chat.id,
                user_name=m.chat.username,
                first_name=m.chat.first_name)
    session.add(dude)
    session.commit()
    log.info(f"registered dude {m.chat.username} with {dude.user_id} id!")
    session.close()

def get_user(tg_user_id, session=None):
    """
    Returns Dude row object
    """
    if not session:
        session = SESSION_FACTORY()
        dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
        session.close()
    dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
    return dude

def check_state(tg_user_id, state) -> bool:
    '''
    checks state of user
    '''
    user = get_user(tg_user_id)
    if user:
        return user.curr_state == state
    return False

def set_column(tg_user_id, state=None, last_src=None):
    """
    Saves current state of user.
    """
    session = SESSION_FACTORY()
    dude = get_user(tg_user_id, session=session)
    if state:
        dude.curr_state = state
    if last_src:
        dude.last_source = last_src
    session.commit()
    session.close()

def alt_bool(tg_user_id, transform=None, random=None):
    # TODO Объеденить мб с верхней функцией?
    """
    Sets random power of bass flag
    True by default.
    """
    session = SESSION_FACTORY()
    dude = get_user(tg_user_id, session=session)
    if transform:
        dude.transform_eyed3 = not dude.transform_eyed3
        result = dude.transform_eyed3
    if random:
        dude.random_bass = not dude.random_bass
        result = dude.random_bass
    session.commit()
    session.close()
    return result

def listener(messages):
    """
    listener function
    that logs message to file
    and updates last_message column in db # NOT_DRY
    """
    session = SESSION_FACTORY()
    for m in messages:
        if m.text:
            log.info(f'{m.chat.username} - {m.text}')
        elif m.voice:
            log.info(f'{m.chat.username} - sended voice')
        elif m.audio:
            log.info(f'{m.chat.username} - sended audio')
        elif m.document:
            log.info(f'{m.chat.username} - sended document,'
                     ' which we dont support yet')
        dude = get_user(m.chat.id, session=session)
        if dude:
            dude.last_message_date = datetime.utcnow()
            session.commit()
    session.close()
