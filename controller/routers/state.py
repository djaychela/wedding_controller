from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from .. import schemas, api_calls
from .. dependencies import get_db
from .. crud import state, dancefloor


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
    background_tasks.add_task(api_calls.api_for_new_song, db, new_state.current_song_id)

    return current_state

@router.post("/dummy_song_change")
async def dummy_song_change(new_state: schemas.StateSetSong, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    current_state.current_song_id = new_state.current_song_id
    current_state.current_song_title = new_state.current_song_title
    current_state.current_song_artist = new_state.current_song_artist
    db.commit()
    dancefloor.increase_dancefloor_songs(db=db)
    background_tasks.add_task(api_calls.api_for_new_song, db, new_state.current_song_id)

    return {"0": True}

@router.get("/change_effect")
def change_effect(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_calls.new_random_effect(db, current_state.current_song_id)
    # current_state = state.get_state(db)
    return current_state

@router.get("/change_colour")
def change_colour(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_calls.new_random_colour(db, current_state.current_song_id)
    # current_state = state.get_state(db)
    return current_state

@router.get("/set_first_song")
def set_first_song(db: Session = Depends(get_db)):
    """Ensures the current state is set to the first dance song id"""
    first_song_id = "2NVpYQqdraEcQwqT7GhUkh"
    new_state = state.update_current_song_id(db, first_song_id)
    api_calls.api_for_new_song(db, first_song_id)
    return {"song_id": first_song_id}

@router.get("/set_darkness")
def set_darkness(db: Session = Depends(get_db)):
    """Ensures the current state is set to a song with black as the output"""
    darkness_id = "1234567890abcdef"
    new_state = state.update_current_song_id(db, darkness_id)
    api_calls.api_for_new_song(db, darkness_id)
    return {"song_id": "darkness"}