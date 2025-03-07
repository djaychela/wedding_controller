import json, colorsys

from random import randrange, shuffle

from sqlalchemy.orm import Session
from requests import post

from . database import SessionLocal
from . state import update_ledfx_state

from . helpers import colour_helpers


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def led_fx_post(db: Session, db_effect):
    API_ENDPOINT = "http://192.168.1.88:8888/api/virtuals/virtual-1/effects"

    data = {
        "active": True,
        "type": str(db_effect.type),
        "name": str(db_effect.name),
        "config": {**db_effect.config},
    }

    data_dump = json.dumps(data)
    r = post(url=API_ENDPOINT, data=data_dump)

    update_ledfx_state(db=db, effect=db_effect)

def sort_colour_list(colour_list):
    if colour_list is None:
        return []
    if len(colour_list) == 0:
        return []
    """Takes a list of hex-format colours and sorts them in brightness order"""
    colour_list_nums = [convert_to_rgb_int(colour) for colour in colour_list]
    colour_list_nums.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
    colour_list_hex = [colour_helpers.convert_int_to_hex(colour) for colour in colour_list_nums]

    return colour_list_hex


def create_gradient(colour_list, limit=3):
    """takes a list of hex-format colours, and outputs
    a linear gradient for ledfx based on the colour list.
    if there are more than limit entries, only a random selection
    of length limit will be added to the gradient."""
    colour_list = sort_colour_list(colour_list)
    if len(colour_list) > limit:
        shuffle(colour_list)
        colour_list = colour_list[:limit]
    if len(colour_list) == 0:
        # empty list, return a random 2-length gradient
        r = randrange(127, 255)
        g = randrange(127, 255)
        b = randrange(127, 255)
        colour = f"#{hex(r)[2:]}{hex(g)[2:]}{hex(b)[2:]}"
        colour_list = [colour]
    increment = int(98 / len(colour_list))
    location = 0
    stem = "linear-gradient(90deg, rgb(0, 0, 0) 0%"
    for colour in colour_list:
        colour_rgb = convert_to_rgb(colour)
        location += increment
        current_colour = f", {colour_rgb} {location}%"
        stem += current_colour
    stem += ")"
    return stem


def convert_to_rgb(colour_string):
    colours = colour_string.lstrip("#")
    return f"rgb{tuple(int(colours[i:i+2], 16) for i in (0, 2, 4))}"


def convert_to_rgb_int(colour_string):
    colours = colour_string.lstrip("#")
    return tuple(int(colours[i : i + 2], 16) for i in (0, 2, 4))


