from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import asyncio

import time

from ..crud import crud

from ..crud import dancefloor

from .. import models, schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db, led_fx_post, convert_to_rgb_int
from ..api_calls import api_blocking_call, ledfx_random_api_call, dancefloor_entry_exit, change_ledfx_type


router = APIRouter(prefix="/dancefloor",)

@router.get("/", response_model=schemas.DancefloorBase)
def get_dancers(db: Session = Depends(get_db)):
    dancers = dancefloor.get_all_dancers(db)
    return dancers

@router.get("/list")
def list_dancers(db: Session = Depends(get_db)):
    dancers = dancefloor.get_all_dancers(db)
    return dancers

@router.get("/list_rgb")
def list_dancers_rgb(db: Session = Depends(get_db)):
    dancers = dancefloor.get_all_dancers(db)
    for dancer in dancers:
        dancer.dancer_colour = convert_to_rgb_int(dancer.dancer_colour)
    return dancers

@router.get("/list_names")
def list_dancers(db: Session = Depends(get_db)):
    dancers = dancefloor.get_all_dancers(db)
    if len(dancers) == 0:
        return {0: "No-one"}
    dancers_names = {}
    for dancer in dancers:
        dancer_user = crud.get_user_by_nfc_id(db, dancer.dancer_nfc_id)
        dancers_names[dancer.id] = f"{dancer_user.first_name}"
        # dance_names_dict = {dancer[0]: f"{dancer[1].first_name} {dancer[1].last_name}" for dancer in enumerate(dancers)}
        dancer.dancer_colour = convert_to_rgb_int(dancer.dancer_colour)
    return dancers_names

@router.get("/colours")
def list_colours(db: Session = Depends(get_db)):
    colours = dancefloor.get_dancefloor_colours(db)
    colours_dict = {colour[0]: colour[1][0] for colour in enumerate(colours)}
    return colours_dict

@router.get("/colours_rgb")
def list_colours_rgb(db: Session = Depends(get_db)):
    colours = dancefloor.get_dancefloor_colours(db)
    colours_dict = {colour[0]: convert_to_rgb_int(colour[1][0]) for colour in enumerate(colours)}
    return colours_dict


@router.post("/entry")
def dancefloor_entry(dancer: schemas.DancefloorEntry, db: Session = Depends(get_db)):
    """Adds dancer to dancefloor list.
    Returns info for the dancer who matches the NFC ID.
    Calls API to update colour palette with new dancer"""
    valid, present = dancefloor.add_dancer(dancer, db)
    if valid:
        # dancer["present"] = 1
        # change_ledfx_type(db=db)
        dancefloor_entry_exit(db=db)
        dancer = dancefloor.get_user_by_nfc_id(db, dancer.dancer_nfc_id)
        return dancer, {"status": 0}
    elif present:
        dancer = dancefloor.get_user_by_nfc_id(db, dancer.dancer_nfc_id)
        return dancer, {"status": 1}
    else:
        return {"None": "None"}, {"status": 3}
    
@router.post("/exit")
def dancefloor_exit(dancer: schemas.DancefloorEntry, db: Session = Depends(get_db)):
    """ Removes dancer from dancefloor list.
        Sends API call to refresh current palette."""

    valid, present = dancefloor.remove_dancer(dancer, db)
    if present:
        dancefloor_entry_exit(db=db)
        return {"colour": valid.colour}, {"status": 2}
    else:
        return {"None": "None"}, {"status": 3}
    


    
