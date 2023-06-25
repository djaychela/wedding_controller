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
from .crud import state, dancefloor, effects, songs

from .helpers import colour_helpers, api_helpers

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

    data = api_helpers.create_api_request_string(random_effect, random_gradient)
    api_helpers.perform_api_call(db, data, "sticks")


def dancefloor_entry_exit(db):
    colourscheme = colour_helpers.create_colourscheme(db)
    current_state = state.get_state(db)

    adj_colourscheme = colour_helpers.refine_colourscheme(db, colourscheme, current_state.ledfx_colour_mode, "floor")
    gradient = colour_helpers.create_gradient(adj_colourscheme)
    data = api_helpers.create_api_request_string(current_state.ledfx_type, gradient)
    api_helpers.perform_api_call(db, data, "sticks")

    # TODO: call bands_current_song(db, timing = "instant") to update bands colours


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
    # if adjacent, use song voter as adjacent basis
    # if gradient, find number and create gradient from voter and df present

    random_effect = random.choice(effects_list)

    data = api_helpers.create_api_request_string(random_effect, current_gradient)
    api_helpers.perform_api_call(db, data, "sticks")

def wrist_bands_new_song(db):
    # perform both calls for wrist band.  Second call has inherent delay.
    executor = ThreadPoolExecutor(max_workers=3)
    executor.submit(flash_bands(db))
    executor.submit(bands_current_song(db, timing="delayed"))

def api_for_new_song(db, song_id=None):
    dancefloor.increase_dancefloor_songs(db=db)
    # look up to see if preset exists for song.
    preset_effect = effects.get_effect_preset_by_song_id(db, song_id)
    if preset_effect:
        # preset present, select output effect, colour type and max colours
        output_effect = preset_effect.config['effect']
        colour_type = preset_effect.colour_type
        max_colours = preset_effect.max_colours
    else:
        # Song does not have a preset, create random effect with voter colours
        random_effect = effects.get_random_effect(db)
        colours = songs.get_song_colours(db, song_id, mode="list")
        colour_type = random_effect.colour_type
        max_colours = random_effect.max_colours        
        colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_type, "floor")
        gradient = colour_helpers.create_gradient(colourscheme)
        output_effect = api_helpers.create_api_request_string(random_effect.type, colourscheme)

    api_helpers.update_state_colours(db, colour_type, max_colours)    
    api_helpers.perform_api_call(db, output_effect, "sticks")
    
    # TODO: perform calls for wristbands
    return output_effect

def flash_bands(db, song_id=None):
    # look up colours of user/s who voted for song
    song_colours = songs.get_song_colours(db, song_id, mode="list")
    # TODO: set api to flash on this colour/s
    data = api_helpers.create_api_request_string("flash", song_colours)
    api_helpers.perform_api_call(db, data, mode="bands")

def bands_current_song(db, timing = "instant"):
    if timing == "delayed":
        # 10 second delay before api call (when called alongside flash mode)
        time.sleep(10)
    # get and refine colourscheme
    colourscheme = colour_helpers.create_colourscheme(db)
    adj_colourscheme = colour_helpers.refine_colourscheme(db, colourscheme)
    # create data call for bands
    # TODO: create appropriate request string for bands effect
    data = api_helpers.create_api_request_string("bands", adj_colourscheme)
    api_helpers.perform_api_call(db, data, mode="bands")


