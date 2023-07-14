from fastapi import APIRouter, Depends, FastAPI, HTTPException, BackgroundTasks
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
def store_current_song(new_state: schemas.StateSetSong, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    current_state.current_song_id = new_state.current_song_id
    current_state.current_song_title = new_state.current_song_title
    current_state.current_song_artist = new_state.current_song_artist
    db.commit()
    dancefloor.increase_dancefloor_songs(db=db)
    background_tasks.add_task(api_for_new_song, db, new_state.current_song_id)

    return current_state

@router.post("/dummy_song_change")
async def dummy_song_change(new_state: schemas.StateSetSong, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    current_state.current_song_id = new_state.current_song_id
    current_state.current_song_title = new_state.current_song_title
    current_state.current_song_artist = new_state.current_song_artist
    db.commit()
    dancefloor.increase_dancefloor_songs(db=db)
    background_tasks.add_task(api_for_new_song, db, new_state.current_song_id)

    return {"0": True}
