from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..crud import crud
from ..crud import dancefloor

from .. import models, schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db, led_fx_post
from ..crud import state #import get_state, update_ledfx_state

router = APIRouter(prefix="/state",)

@router.get("/", response_model=schemas.StateBase)
def read_state(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    return current_state

@router.post("/set_current_song", response_model=schemas.StateBase)
def store_current_song(new_state: schemas.StateSetSong, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    current_state.current_song_id = new_state.current_song_id
    current_state.current_song_title = new_state.current_song_title
    current_state.current_song_artist = new_state.current_song_artist
    db.commit()
    dancefloor.increase_dancefloor_songs(db=db)
    # TODO: trigger new effect generation here.
    # Wrist bands should flash colour of song owner, if there is one
    # New Effect selected for song - random or programmed
    # Colour Palette Selected on Song owner and those on dancefloor
    # Colour Pallete for song is at crud.songs.get_song_colours (mode="list")
    # db_effect = crud.get_random_effect(db=db)
    # update_ledfx_state(db, db_effect)
    return current_state

