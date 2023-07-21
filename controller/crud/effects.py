from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models, schemas

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

def get_random_effect(db: Session, max_colours):
    return db.query(models.Effect).filter(models.Effect.max_colours >= max_colours).order_by(func.random()).first()

def get_random_effect_preset(db: Session):
    return db.query(models.EffectPreset).order_by(func.random()).first()

def get_effect_preset_by_song_id(db: Session, song_id: str):
    return db.query(models.EffectPreset).filter(models.EffectPreset.song_id == song_id).first()

def get_effect_string_by_id(db: Session, effect_id: str):
    effect = db.query(models.Effect).filter(models.Effect.id == effect_id).first()
    return effect.config