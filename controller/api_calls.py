# calls to virtual-1
# calls to virtual-bands
# calls to virtual-dmx


"""
Bands calls are to last for ~10 seconds, then go to pattern to match dancefloor and current palette
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
import random
import requests
import json

from concurrent.futures import ThreadPoolExecutor

from .models import EffectPreset
from .crud import state, dancefloor, effects
from .dependencies import create_gradient, adjacent_colours, convert_to_rgb_int, convert_int_to_hex
from .api_helpers import (
    update_state_from_response,
    create_api_request_string,
    perform_api_call,
)

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
    random_gradient = random.choice(gradient_list)
    random_effect = random.choice(effects_list)

    data = create_api_request_string(random_effect, random_gradient)
    perform_api_call(db, data, "sticks")


def dancefloor_entry_exit(db):
    current_state = state.get_state(db)
    current_type = current_state.ledfx_type
    dancefloor_gradient = create_gradient(
        dancefloor.get_dancefloor_colours(db, list_mode=True)
    )

    # TODO: this is where the experimental gradients happen
    # adj_gradient is adjacents, based on the last dancer
    # mono_gradient is just the last dancer and (0,0,0) 0%

    last_dancer = dancefloor.get_last_dancer(db)
    adj = adjacent_colours(convert_to_rgb_int(last_dancer[0]))
    adj_gradient = create_gradient(adj)
    mono_gradient = create_gradient([last_dancer[0]])

    data = create_api_request_string(current_type, adj_gradient)
    perform_api_call(db, data, "sticks")


def change_ledfx_type(db):
    current_state = state.get_state(db)
    current_config = current_state.ledfx_config
    current_gradient = current_config["config"]["gradient"]
    # TODO: this should check if the song has a user vote?
    # select a random effect from effects in db
    new_effect = effects.get_random_effect()
    print(new_effect.colour_type)
    # create suitable gradient for chosen effect (single, adjacent, gradient)
    # if single, choose song voter
    # if adjancent, use song voter as adjacent basis
    # if gradient, find number and create gradient from voter and df present

    random_effect = random.choice(effects_list)

    data = create_api_request_string(random_effect, current_gradient)
    perform_api_call(db, data, "sticks")

def api_for_new_song(db):
    current_state = state.get_state(db)
    current_config = current_state.ledfx_config
    current_gradient = current_config["config"]["gradient"]
    # TODO: this should check if the song has a user vote?
    # select a random effect from effects in db
    new_effect = effects.get_random_effect()
    print(new_effect.colour_type)
    # create suitable gradient for chosen effect (single, adjacent, gradient)
    # if single, choose song voter
    # if adjancent, use song voter as adjacent basis
    # if gradient, find number and create gradient from voter and df present

    random_effect = random.choice(effects_list)

    data = create_api_request_string(random_effect, current_gradient)
    perform_api_call(db, data, "sticks")

def flash_bands():
    # look up user who voted for song
    # set api to flash on this colour
    pass


def bands_current_song():
    # get current colour palette
    # set bands to whatever fx in that colour
    pass


def sticks_current_song():
    # check if song has an effect set for it
    #
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
