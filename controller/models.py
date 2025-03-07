from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

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
    colour_mode = Column(String, index=True)
    max_colours = Column(Integer)
    config = Column(JSON)

class EffectPreset(Base):
    __tablename__ = "effect_preset_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    song_id = Column(String, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    config = Column(JSON)
    colour_mode = Column(String, index=True)
    max_colours = Column(Integer)
    

class State(Base):
    __tablename__ = "state_table"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    current_song_id = Column(String)
    current_song_title = Column(String, index=True)
    current_song_artist = Column(String, index=True)
    colours = Column(String)
    ledfx_name = Column(String, index=True)
    ledfx_type = Column(String, index=True)
    ledfx_config = Column(JSON)
    ledfx_colour_mode = Column(String, index=True)
    ledfx_max_colours = Column(Integer)
    bands_name = Column(String, index=True)
    bands_type = Column(String, index=True)
    bands_config = Column(JSON)
    bands_colour_mode = Column(String, index=True)
    bands_max_colours = Column(Integer)
    effect_id = Column(Integer)
    

class Dancefloor(Base):
    __tablename__ = "dancefloor_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    dancer_nfc_id = Column(String)
    dancer_colour = Column(String)
    dances_present = Column(Integer, default=0)
