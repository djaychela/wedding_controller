from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import json

from .. import models, schemas


def get_state(db: Session):
    return db.query(models.State).filter(models.State.id == 1).first()

def update_state_ledfx(db: Session, effect: schemas.EffectPreset):
    """ Takes a db session and an Effect and updates the current ledfx state to reflect the present Effect"""
    current_state = get_state(db)
    current_state.ledfx_name = effect.name
    current_state.ledfx_type = effect.type
    current_state.ledfx_config = effect.config
    db.commit()

def update_state_bands(db: Session, effect: schemas.EffectPreset):
    """ Takes a db session and an Effect and updates the current bands state to reflect the present Effect"""
    current_state = get_state(db)
    current_state.bands_name = effect.name
    current_state.bands_type = effect.type
    current_state.bands_config = effect.config
    db.commit()

def update_state_ledfx_colours(db: Session, colour_mode, max_colours):
    """ Takes a db session and an Effect and updates the current state to reflect the present Effect"""
    current_state = get_state(db)
    current_state.ledfx_colour_mode = colour_mode
    current_state.ledfx_max_colours = max_colours
    db.commit()

def update_state_colours(db: Session, colours):
    """ Takes a list of colours, and stores it in the database as json"""
    current_state = get_state(db)
    current_state.colours = json.dumps(colours)
    db.commit()   

def update_current_song_id(db: Session, current_song_id):
    """ Takes a song id and updates the current state.  Returns the state"""
    current_state = get_state(db)
    current_state.current_song_id = current_song_id
    db.commit()  
    return current_state

def get_current_effect(db: Session):
    current_state = get_state(db)
    effect = models.Effect()
    effect.name = current_state.ledfx_name
    effect.type = current_state.ledfx_type
    effect.config = current_state.ledfx_config
    return effect

def update_effect_id(db: Session, effect_id: int):
    """ Takes an effect id and updates the current state.  Returns the state"""
    current_state = get_state(db)
    current_state.effect_id = effect_id
    db.commit()
    return current_state

