from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_nfc_id(db:Session, nfc_id: str):
    return db.query(models.User).filter(models.User.nfc_id == nfc_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_nfc_id(db:Session, id: int, nfc_id:str):
    current_user = db.query(models.User).filter(models.User.id == id).first()
    current_user.nfc_id = nfc_id
    db.commit()
    return current_user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, first_name=user.first_name, last_name=user.last_name, colour=user.colour)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_colours_for_song(db:Session, current_song_id: int = 1):
    users = db.query(models.User).join(models.association_table).join(models.Song).filter(models.Song.id == current_song_id).all()
    return users