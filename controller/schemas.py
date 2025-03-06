from pydantic import BaseModel, Json
from typing import Optional, List

class SongBase(BaseModel):

    track_id: str | None = None
    title: str
    artist: str
    duration: int

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int
    track_id: str
    title: str | None
    artist: str
    duration: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    colour: str
    nfc_id: str

class UserCreate(UserBase):
    username: str
    first_name: str
    last_name: str
    colour: str
    nfc_id: str

class User(UserBase):
    id: int
    username: str
    first_name: str
    last_name: str
    colour: str | None
    nfc_id: str | None

    class Config:
        from_attributes = True


class GradientBase(BaseModel):
    gradient: str

    class Config:
        from_attributes = True

class Gradient(GradientBase):
    gradient: str

class GradientCreate(GradientBase):
    gradient: str


class EffectBase(BaseModel):
    name: str
    type: str
    colour_mode: str
    max_colours: int

    class Config:
        from_attributes = True

class EffectPresetBase(BaseModel):
    song_id: str
    name: str
    type: str
    config: Optional[dict]

    class Config:
        from_attributes = True

class EffectPresetCreate(EffectPresetBase):
    song_id: str
    name: str
    type: str
    config: Json
    
                     
    class Config:
        from_attributes = True

class EffectPreset(EffectPresetBase):
    class Config:
        from_attributes = True

class EffectPresetSelect(BaseModel):
    name: str
    type: str

    class Config:
        from_attributes = True


class StateBase(BaseModel):
    current_song_id: str
    current_song_title: str
    current_song_artist: str
    ledfx_name: str
    ledfx_type: str
    ledfx_config: Optional[dict]
    ledfx_colour_mode: str
    ledfx_max_colours: int
    bands_name: str
    bands_type: str
    bands_config: Optional[dict]
    bands_colour_mode: str
    bands_max_colours: int
    effect_id: int
    colours: Optional[str]

    class Config:
        from_attributes = True

class StateLedFxUpdate(BaseModel):

    ledfx_name: str
    ledfx_type: str
    ledfx_config: Optional[dict]

    class Config:
        from_attributes = True

class StateLedFxUpdateColours(BaseModel):

    ledfx_colour_mode: str
    ledfx_max_colours: str

    class Config:
        from_attributes = True

class StateSetSong(BaseModel):
    current_song_id: str
    current_song_title: str
    current_song_artist: str

class DancefloorBase(BaseModel):
    # id: int
    dancer_id: Optional[int]

    class Config:
        from_attributes = True

class DancefloorList(BaseModel):
    data: List[DancefloorBase]

    class Config:
        from_attributes = True

class DancefloorColourBase(BaseModel):
    dancer_colour: Optional[str]

class DancefloorColourList(BaseModel):
    dancer_colour: List[DancefloorColourBase] | None

    class Config:
        from_attributes = True

class DancefloorEntry(BaseModel):
    # id: int
    dancer_nfc_id: Optional[str]



