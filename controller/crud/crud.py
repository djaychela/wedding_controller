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

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, first_name=user.first_name, last_name=user.last_name, colour=user.colour)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()

def create_effect(db: Session, effect: schemas.EffectPresetCreate):
    db_effect = models.EffectPreset(**effect.dict())
    db.add(db_effect)
    db.commit()
    db.refresh(db_effect)
    return db_effect

def get_effects(db: Session, skip: int=0, limit: int=100):
    return db.query(models.EffectPreset).offset(skip).limit(limit).all()

def get_effect_types(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Effect).offset(skip).limit(limit).all()

def get_effect_by_id(db: Session, effect_id: int):
    return db.query(models.EffectPreset).filter(models.EffectPreset.id == effect_id).first()

def get_random_effect(db: Session):
    return db.query(models.EffectPreset).order_by(func.random()).first()

def get_user_colours_for_song(db:Session, current_song_id: int = 1):
    users = db.query(models.User).join(models.association_table).join(models.Song).filter(models.Song.id == current_song_id).all()
    for user in users:
        print(user.name, user.colour)
    return users