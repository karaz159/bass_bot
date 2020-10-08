"""
Module describes audio class
allowing to set eyed3 tags, add dcb to bass, etc
"""
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from time import sleep

import eyed3
import ffmpeg
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot

from config import BASS_PATH, DOWNLOAD_PATH, LOG_PATH, sys_log, file_log
from helpers import download, download_video, leet_translate
from models import Dude
from handlers import setup_handlers


@dataclass()
class Paths:
    download: Path
    bass: Path
    log: Path

    @property
    def list(self):
        return [self.log, self.bass, self.download]


class TgAudio:
    """
    Main TgAudio class
    """
    def __init__(self, sender_id, src_path, content_type,
                 performer=None, title=None, update_tags=False):
        self.sender_id = sender_id
        self.content_type = content_type  # TODO two classes?

        if self.content_type == 'audio':
            self.performer = performer
            self.title = title
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}B.mp3'
        else:
            self.bass_done_path = f'{BASS_PATH}{self.sender_id}B.ogg'
        self.src_path = src_path
        self.transform_eyed3 = False
        if update_tags:
            ll = eyed3.load(self.src_path)
            ll.tag.artist = self.performer
            ll.tag.title = self.title
            ll.tag.save()

    @classmethod
    def from_message(cls, m):
        """
        Make this class from message,
        just pass message from tg
        """
        src_path = f'{DOWNLOAD_PATH}{m.chat.id}.mp3' if m.audio else f'{DOWNLOAD_PATH}{m.chat.id}.ogg'

        download(m, src_path)

        if m.audio:
            return cls(sender_id=m.chat.id,
                       src_path=src_path,
                       content_type=m.content_type,
                       performer=m.audio.performer,
                       title=m.audio.title)

        return cls(sender_id=m.chat.id,
                   src_path=src_path,
                   content_type=m.content_type)

    @classmethod
    def from_local(cls, m):
        """
        Make this class from local audio
        """
        user = get_user(m.chat.id)
        src = user.last_source

        if not os.path.exists(src):
            raise FileNotFoundError

        if src.endswith('mp3'):
            tags = eyed3.load(src).tag
            return cls(sender_id=m.chat.id,
                       src_path=user.last_source,
                       content_type='audio',
                       performer=tags.artist if tags else '',
                       title=tags.title if tags else '')

        return cls(m.chat.id, src, 'voice')

    @classmethod
    def from_yt(cls, m, link):
        """
        Makes class out of youtube video
        """
        src_path = f'{DOWNLOAD_PATH}{m.chat.id}'

        try:
            os.remove(f'{src_path}.mp3')
            os.remove(f'{src_path}.mp4')

        except FileNotFoundError:
            pass

        meta = download_video(link, src_path)
        src_path += '.mp3'
        title = meta['alt_title'] if meta['alt_title'] else meta['title']
        time.sleep(3)

        return cls(sender_id=m.chat.id, src_path=src_path,
                   content_type='audio', performer=meta['uploader'],
                   title=title, update_tags=True)

    def save_tags(self):
        """
        Updates mp3 tags using
        eyed3 lib
        """
        loaded_audio = eyed3.load(self.bass_done_path)
        loaded_audio.tag.artist = self.performer
        loaded_audio.tag.title = self.title
        loaded_audio.tag.save()

    def transform_tag(self):
        """
        gets title and performer from self
        and transforms them using leet_translate func
        """
        self.title = leet_translate(self.title)
        self.performer = leet_translate(self.performer)
        self.save_tags()

    def bass_boost(self, how_many):
        """
        Adds some dcb to loaded audio
        """
        stream = ffmpeg.input(self.src_path)
        stream = stream.audio.filter("bass", g=how_many)
        ffmpeg.output(stream, self.bass_done_path).overwrite_output().run()

        if self.transform_eyed3:
            self.transform_tag()

    def open_bass(self):
        """
        Returns opened in bytes audio
        """
        return open(self.bass_done_path, 'rb')


class BassBot(TeleBot):
    def __init__(self, token: str, db_dsn, base,
                 download_path: Path = DOWNLOAD_PATH,
                 bass_path: Path = BASS_PATH,
                 log_path: Path = LOG_PATH):
        super().__init__(token=token)
        self.db = SqlWorker(base=base, db_dsn=db_dsn)
        self.audio = TgAudio
        self.paths = Paths(download=download_path,
                           bass=bass_path,
                           log=log_path)
        self.audio = TgAudio
        self.setup()


    def setup(self):
        self.update_listener.append(self.listener)
        self.prepare_folders()
        setup_handlers(self)

    def prepare_folders(self):
        for folder in self.paths.list:
            if not folder.exists:
                pass

    @staticmethod
    def listener(messages):
        for message in messages:
            if message.text:
                file_log.info(f'{message.chat.username} - {message.text}')

            elif message.voice:
                file_log.info(f'{message.chat.username} - sent voice')

            elif message.audio:
                file_log.info(f'{message.chat.username} - sent audio')

            elif message.document:
                file_log.info(f'{message.chat.username} - sent document,'
                              ' which we dont support yet')


class SqlWorker:
    def __init__(self, base, db_dsn: str):
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
                print('ll')
                sys_log.warning('can`t connect to db!')
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
            file_log.info(f"registered dude {message.chat.username} "
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
        with self.session_scope() as session:
            user = self.get_user(tg_user_id, session=session)
            if user:
                return user.curr_state == state
        return False

    def set_column(self, tg_user_id, state=None, last_src=None):
        """
        Saves current state of user.
        """
        with self.session_scope() as session:
            dude = self.get_user(tg_user_id, session=session)
            if state:
                dude.curr_state = state
            if last_src:
                dude.last_source = last_src

    def alt_bool(self, tg_user_id, transform=None, random=None):
        # TODO Объеденить мб с верхней функцией?
        # TODO сделать функцию get update
        """
        Alts bool of transform or random column
        """
        with self.session_scope() as session:
            dude = self.get_user(tg_user_id, session=session)
            if transform:
                dude.transform_eyed3 = not dude.transform_eyed3
                result = dude.transform_eyed3
            if random:
                dude.random_bass = not dude.random_bass
                result = dude.random_bass
        return result
