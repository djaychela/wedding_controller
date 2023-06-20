from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Float, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional

from typing import List

from .database import Base

class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    colour = Column(String)
    nfc_id = Column(String)

class Song(Base):
    __tablename__ = "song_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id = Column(String, unique=True, index=True)
    artist = Column(String)
    title = Column(String)
    duration = Column(Integer)

class Votes(Base):
    __tablename__ = "votes_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id = Column(String, index=True)
    voter_id = Column(Integer)


class Gradient(Base):
    __tablename__ = "gradient_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gradient = Column(String, index=True)

class Effect(Base):
    __tablename__ = "effect_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    colour_type = Column(String, index=True)
    max_colours = Column(Integer)

class EffectPreset(Base):
    __tablename__ = "effect_preset_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    config = Column(JSON)
    

class State(Base):
    __tablename__ = "state_table"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    current_song_id = Column(String)
    current_song_title = Column(String, index=True)
    current_song_artist = Column(String, index=True)
    # current_song_ledfx_random = Column(Boolean)
    ledfx_name = Column(String, index=True)
    ledfx_type = Column(String, index=True)
    ledfx_config = Column(JSON)
    # dancers: Mapped[List] = mapped_column(String)

class Dancefloor(Base):
    __tablename__ = "dancefloor_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    dancer_nfc_id = Column(String)
    dancer_colour = Column(String)
    dances_present = Column(Integer, default=0)
