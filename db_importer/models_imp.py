from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Float, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional

from typing import List

from database_imp import CtrlBase, DbBase

class User(CtrlBase):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    colour = Column(String)
    nfc_id = Column(String)

class Song(CtrlBase):
    __tablename__ = "song_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id = Column(String, unique=True, index=True)
    artist = Column(String)
    title = Column(String)
    duration = Column(Integer)

class Votes(CtrlBase):
    __tablename__ = "votes_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id = Column(String, index=True)
    voter_id = Column(Integer)

class State(CtrlBase):
    __tablename__ = "state_table"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    current_song_id = Column(String)
    current_song_title = Column(String, index=True)
    current_song_artist = Column(String, index=True)
    # current_song_ledfx_random = Column(Boolean)
    ledfx_name = Column(String, index=True)
    ledfx_type = Column(String, index=True)
    ledfx_config = Column(JSON)

class Gradient(CtrlBase):
    __tablename__ = "gradient_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gradient = Column(String, index=True)

class Effect(CtrlBase):
    __tablename__ = "effect_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)


class DbVotes(DbBase):
    __tablename__ = "tracks_votestable"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id = Column(String, index=True)
    voter_id = Column(Integer)

class DbUser(DbBase):
    __tablename__ = "users_customuser"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    colour = Column(String)

class DbTrack(DbBase):
    __tablename__ = "tracks_musictrack"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id = Column(String)
    artist = Column(String)
    name = Column(String)
    duration = Column(Integer)
