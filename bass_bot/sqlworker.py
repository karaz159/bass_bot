#!/usr/bin/python3
"""
Module contains all functions that
in some way relative to sql
"""
from datetime import datetime
from time import sleep
from contextlib import contextmanager

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from config import log
from models import Dude


class SqlWorker:
    def __init__(self, db_dsn, base):
        self.engine = create_engine(db_dsn)
        self.session_maker = sessionmaker(bind=self.engine)
        self.base = base
        self.connect()

    def connect(self):
        while True:
            try:
                self.base.metadata.create_all(self.engine)
                break
            except exc.OperationalError:
                log.info('can`t connect to db!')
                sleep(5)

    @contextmanager
    def session_scope(self) -> sessionmaker:
        """Provide a transactional scope around a series of operations."""
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def register_dude(self, message):
        """
        Register user from message
        """
        dude = Dude(tg_user_id=message.chat.id,
                    user_name=message.chat.username,
                    first_name=message.chat.first_name)

        with self.session_scope() as session:
            session.add(dude)
            log.info(f"registered dude {message.chat.username} "
                     f"with {dude.user_id} id!")

    def get_user(self, tg_user_id, session=None) -> Dude:
        """
        Returns Dude row object
        """
        if not session:
            with self.session_scope() as ses:
                dude = ses.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
                ses.expunge_all()
        else:
            dude = session.query(Dude).filter_by(tg_user_id=tg_user_id).one_or_none()
        return dude

    def check_state(self, tg_user_id, state) -> bool:  # TODO вообще нужен?
        """
        checks state of user
        """
        with selfsession_scope() as session:
            user = self.get_user(tg_user_id, session=session)
            if user:
                return user.curr_state == state
        return False

    def set_column(self, tg_user_id, state=None, last_src=None):
        """
        Saves current state of user.
        """
        with session_scope() as session:
            dude = get_user(tg_user_id, session=session)
            if state:
                dude.curr_state = state
            if last_src:
                dude.last_source = last_src

    def alt_bool(self, tg_user_id, transform=None, random=None):
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


