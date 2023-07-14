from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models, schemas
from ..helpers import colour_helpers

import time

def get_user_by_nfc_id(db:Session, nfc_id: str):
    return db.query(models.User).filter(models.User.nfc_id == nfc_id).first()

def get_all_dancers(db: Session):
    return db.query(models.Dancefloor).all()

def get_dancefloor_colours(db: Session, list_mode=False):
    if not list_mode:
        return db.query(models.Dancefloor).with_entities(models.Dancefloor.dancer_colour).order_by(models.Dancefloor.id.desc()).limit(3).all()
    else:
        return [colour[0] for colour in db.query(models.Dancefloor).with_entities(models.Dancefloor.dancer_colour).order_by(models.Dancefloor.id.desc()).limit(3).all()]

def get_last_n_dancers(db: Session, list_mode=False, num_dancers = 1):
    result = db.query(models.Dancefloor).with_entities(models.Dancefloor.dancer_colour).order_by(models.Dancefloor.id.desc()).limit(num_dancers).all()
    if not result:
        # no-one on the dancefloor, so make some colours up!
        result = [(colour_helpers.generate_random_hex_colour(), )]
    if list_mode:
        return [colour[0] for colour in result]
    return result


def increase_dancefloor_songs(db: Session):
    dancers = db.query(models.Dancefloor).all()
    for dancer in dancers:
        dancer.dances_present += 1
        db.commit()
    return None

def add_dancer(dancer: schemas.DancefloorEntry, db: Session):
    # check if dancer already on dancefloor
    all_dancers = get_all_dancers(db)
    nfc_ids = [d.dancer_nfc_id for d in all_dancers]
    if dancer.dancer_nfc_id in nfc_ids:
        return (None, 1)
    # look up user from nfc to get colour
    nfc_user = get_user_by_nfc_id(db, dancer.dancer_nfc_id)
    if nfc_user:
        new_dancer = models.Dancefloor()
        new_dancer.dancer_nfc_id = dancer.dancer_nfc_id
        new_dancer.dancer_colour = nfc_user.colour
        db.add(new_dancer)
        db.commit()
        db.refresh(new_dancer)
        return (new_dancer, 1)
    return (None, 0)

def remove_dancer(dancer: schemas.DancefloorEntry, db: Session):
    # check if dancer is on dancefloor
    dancer_to_remove = db.query(models.Dancefloor).filter(models.Dancefloor.dancer_nfc_id == dancer.dancer_nfc_id).first()
    if dancer_to_remove:
        nfc_user = get_user_by_nfc_id(db, dancer.dancer_nfc_id)
        db.delete(dancer_to_remove)
        db.commit()
        return (nfc_user, 1)
    # not present in dancefloor, nothing to return
    return (None, 0)