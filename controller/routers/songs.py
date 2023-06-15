from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..crud import crud

from .. import models, schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db

router = APIRouter(prefix="/songs")



@router.get("/", response_model=list[schemas.Song])
def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs


# router /new:
    #get name of current song from post request
    #look up in database
    #look for users who voted for song, get colour palette from this
    #look for effect if present, or select random
    # put both together and GOOOO