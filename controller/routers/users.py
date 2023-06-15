from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..crud import crud

from .. import models, schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db

router = APIRouter(prefix="/users",)


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    # crud.get_user_colours_for_song(db, 2)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return db_user
