# calls to virtual-1
# calls to virtual-bands
# calls to virtual-dmx


"""
Bands calls are to last for ~20 seconds, then go to pattern to match dancefloor and current palette
virtual-1 calls to start straight away
virtual-dmx calls to start straight away

four different configs needed for fx
bands - flash
bands - current song
stick - current song
dmx   - current song

complementary patterns needed for bands and stick in particular

"""

import time

import pprint

import random

import requests

import json

from concurrent.futures import ThreadPoolExecutor

from .models import EffectPreset
from .crud import state, dancefloor
from .dependencies import create_gradient
from .api_helpers import update_state_from_response, create_api_request_string

API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-1/effects"

gradient_list = [
    "linear-gradient(90deg, rgb(255, 0, 0) 0%, rgb(255, 120, 0) 14%, rgb(255, 200, 0) 28%, rgb(0, 255, 0) 42%, rgb(0, 199, 140) 56%, rgb(0, 0, 255) 70%, rgb(128, 0, 128) 84%, rgb(255, 0, 178) 98%)",
    "linear-gradient(90deg, rgb(255, 0, 0) 0%,  rgb(255, 0, 178) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(127, 127, 127) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(0, 255, 0) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(255, 0, 0) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(0, 0, 255) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(0, 255, 255) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(255, 0, 255) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(255, 255, 0) 98%)",
    "linear-gradient(90deg, rgb(0, 0, 0) 0%, rgb(255, 0, 0) 98%)",
]

effects_list = [
    "marching",
    "bands_matrix",
    "power",
    "rain",
    "glitch",
    "melt",
    "melt_and_sparkle",
    "water",
    "equalizer",
]


def ledfx_random_api_call(db):
    # Should update state to reflect current status once random selected
    current_gradient = random.choice(gradient_list)
    current_effect = random.choice(effects_list)

    print(f"Effect Chosen: {current_effect}")
    print(f"Gradient Chosen: {current_gradient}")
    # get gradient from dancefloor
    dancefloor_colours = dancefloor.get_dancefloor_colours(db, list_mode=True)
    dancefloor_gradient = create_gradient(dancefloor_colours)
    print(dancefloor_gradient)

    data = create_api_request_string(current_effect, dancefloor_gradient)

    # data = {
    #     "active": True,
    #     "type": str(current_effect),
    #     "config": {
    #         "blur": 0.0,
    #         "gradient": dancefloor_gradient,
    #         "band_count" : 10
    #     }
    # }

    data_dump = json.dumps(data)

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data_dump)

    if r:
        update_state_from_response(db, r)


def dancefloor_entry_exit(db):
    current_state = state.get_state(db)
    current_type = current_state.ledfx_type

    dancefloor_colours = dancefloor.get_dancefloor_colours(db, list_mode=True)
    dancefloor_gradient = create_gradient(dancefloor_colours)

    data = create_api_request_string(current_type, dancefloor_gradient)

    data_dump = json.dumps(data)

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data_dump)
    if r:
        update_state_from_response(db, r)


def change_ledfx_type(db):
    current_state = state.get_state(db)
    current_config = current_state.ledfx_config
    current_name = current_config["name"]
    current_type = current_config["type"]
    current_gradient = current_config["config"]["gradient"]
    random_effect = random.choice(effects_list)
    print(f"{current_name=}")
    print(f"{current_type=}")
    print(f"{current_gradient=}")
    # dancefloor_colours = dancefloor.get_dancefloor_colours(db, list_mode=True)
    # dancefloor_gradient = create_gradient(dancefloor_colours)

    data = {
        "active": True,
        "type": str(random_effect),
        "config": {"blur": 0.0, "gradient": current_gradient, "band_count": 10},
    }

    data_dump = json.dumps(data)

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data_dump)
    if r:
        update_state_from_response(db, r)


def flash_bands():
    pass


def bands_current_song():
    pass


def sticks_current_song():
    pass


def dmx_current_song():
    pass


def call_2():
    print("Call 2")


# test async call
def api_blocking_call():
    print("Calling 1 and 2...")

    executor = ThreadPoolExecutor(max_workers=3)
    executor.submit(ledfx_random_api_call)
    executor.submit(call_2)
