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
from typing import List, Optional

import eyed3
import ffmpeg
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot
from telebot.types import Message

from config import BASS_PATH, DOWNLOAD_PATH, LOG_PATH, sys_log
from handlers import setup_handlers
from helpers import download_video, leet_translate
from models import Dude


@dataclass()
class Paths:
    download: Path
    bass: Path
    log: Path

    @property
    def list(self) -> List[Path]:
        return [self.log, self.bass, self.download]


class TgAudio:
    """
    Main TgAudio class
    """
    def __init__(self, sender_id: int, src_path: Path, content_type, bot: BassBot,
                 performer: str = None, title: str = None, update_tags: bool = False):
        self.sender_id = sender_id
        self.content_type = content_type
        self.performer = performer
        self.title = title
        self.bot = bot

        if self.content_type == 'audio':
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
        src_path = DOWNLOAD_PATH / f'{m.chat.id}.mp3' if m.audio else DOWNLOAD_PATH / f'{m.chat.id}.ogg'

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

    def __str__(self):
        return str(self.src_path)


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
        self.setup()

    def setup(self):
        self.update_listener.append(self.listener)
        self.prepare_folders()
        setup_handlers(self)

    def prepare_folders(self):
        for folder in self.paths.list:
            folder.mkdir(exist_ok=True)

    @staticmethod
    def listener(messages):
        for message in messages:
            if message.text:
                sys_log.info(f'{message.chat.username} - {message.text}')

            elif message.voice:
                sys_log.info(f'{message.chat.username} - sent voice')

            elif message.audio:
                sys_log.info(f'{message.chat.username} - sent audio')

            elif message.document:
                sys_log.info(f'{message.chat.username} - sent document,'
                             ' which we dont support yet')

    def download(self, message: Message, name: Path):
        """
        downloads mp3 or voice via bot
        """
        if message.audio:
            file_info = self.get_file(message.audio.file_id)
        else:
            file_info = self.get_file(message.voice.file_id)

        downloaded_file = self.download_file(file_info.file_path)

        with name.open('wb') as new_file:
            new_file.write(downloaded_file)

        return name


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
                sys_log.warning('can`t connect to db!')
                sleep(5)

    @contextmanager
    def session_scope(self) -> sessionmaker:  # TODO is there others scopes in sqlalchemy?
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

    @staticmethod
    def get_user(message: Message, session) -> Dude:
        """
        Returns Dude row object
        """
        dude = session.query(Dude).filter_by(tg_user_id=message.chat.id).one_or_none()
        if not dude:
            dude = Dude(tg_user_id=message.chat.id,
                        user_name=message.chat.username)
            session.add(dude)

            sys_log.info(f"registered dude {message.chat.username} "
                         f"with {dude.tg_user_id} id!")

        return dude

    def check_state(self, message: Message = None, state: str = None):
        with self.session_scope() as ses:
            user = self.get_user(message=message, session=ses)
            if user.curr_state == state:
                return True
            return False

    def provide_session(self, function):
        def session_wrapper(*args, **kwargs):
            with self.session_scope() as ses:
                return function(*args, ses, **kwargs)

        return session_wrapper

