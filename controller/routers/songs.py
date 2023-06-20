from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..crud import songs

from .. import models, schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db

router = APIRouter(prefix="/songs")



@router.get("/", response_model=list[schemas.Song])
def get_all_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    song_list = songs.get_songs(db, skip=skip, limit=limit)
    return song_list

@router.get("/{song_id}")
def get_song_details(song_id: str, db: Session = Depends(get_db)):
    song = songs.get_song(song_id, db)
    return song

@router.get("/{song_id}/colours/")
def get_song_colours(song_id: str, db: Session = Depends(get_db)):
    colours = songs.get_song_colours(song_id, db)
    return colours

