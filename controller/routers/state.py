from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db
from ..crud import state, dancefloor, effects, songs #import get_state, update_ledfx_state
from ..api_calls import api_for_new_song

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

@router.post("/dummy_song_change")
def dummy_song_change(new_state: schemas.StateSetSong, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    current_state.current_song_id = new_state.current_song_id
    current_state.current_song_title = new_state.current_song_title
    current_state.current_song_artist = new_state.current_song_artist
    db.commit()
    effect_chosen = api_for_new_song(db, new_state.current_song_id)
    # song_id = "043bfUkTydw0xJ5JjOT91w"
    # dancefloor.increase_dancefloor_songs(db=db)
    # # look up to see if preset exists for song.
    # # if it does, send that to api
    # # otherwise create random effect with song owner as colour/s
    # random_effect = effects.get_random_effect(db)
    # colours = songs.get_song_colours(song_id, db, mode="list")
    # print(colours)
    # print(create_gradient(colours))
    # # build effect from random root
    # # get gradient from song owner
    # # send to create_api_request_string
    return effect_chosen
