from sqlalchemy.orm import Session

from . import models, schemas


def get_state(db: Session):
    return db.query(models.State).filter(models.State.id == 1).first()

def update_ledfx_state(db: Session, effect: schemas.EffectPreset):
    """ Takes a db session and an Effect and updates the current state to reflect the present Effect"""
    current_state = get_state(db)
    current_state.ledfx_name = effect.name
    current_state.ledfx_type = effect.type
    current_state.ledfx_config = effect.config
    db.commit()

def store_state(db: Session, state: schemas.StateBase):
    return db.query(models.State).filter(models.State.id == 1).first()    

def get_current_effect(db: Session):
    current_state = get_state(db)
    effect = models.Effect()
    effect.name = current_state.ledfx_name
    effect.type = current_state.ledfx_type
    effect.config = current_state.ledfx_config
    return effect

