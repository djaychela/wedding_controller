import time
import json

from concurrent.futures import ThreadPoolExecutor

from .crud import state, effects, songs

from .helpers import colour_helpers, api_helpers, bands_helpers

API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-1/effects"

def dancefloor_entry_exit(db):
    colourscheme = colour_helpers.create_colourscheme(db)
    current_state = state.get_state(db)

    adj_colourscheme = colour_helpers.refine_colourscheme(db, colourscheme, current_state.ledfx_colour_mode, "floor")
    gradient = colour_helpers.create_gradient(adj_colourscheme)
    data = api_helpers.create_api_request_string(current_state.ledfx_type, gradient)
    api_helpers.perform_api_call(db, data, "sticks")
    bands_current_song(db, timing="instant")

def bands_current_song(db, timing = "instant"):
    if timing == "delayed":
        time.sleep(10)
    current_state = state.get_state(db)
    colourscheme = json.loads(current_state.colours)
    adj_colourscheme = colour_helpers.refine_colourscheme(db, colourscheme, current_state.ledfx_colour_mode, "song")
    gradient = colour_helpers.create_gradient(adj_colourscheme)
    
    data = api_helpers.create_api_request_string("bands", gradient)
    api_helpers.perform_api_call(db, data, mode="bands")

def flash_bands(db, song_id=None):
    """Looks up voters for current song"""
    song_colours = songs.get_song_colours(db, song_id, mode="list", strict=True)
    if len(song_colours) == 0:
        # No-one voted, so set the bands for the song
        bands_current_song(db, "instant")
        return
    gradient = colour_helpers.create_gradient(song_colours)
    data = api_helpers.create_api_request_string("bands_flash", gradient)
    api_helpers.perform_api_call(db, data, mode="bands")

def wrist_bands_new_song(db, song_id):
    # perform both calls for wrist band.  Second call is delayed.
    executor = ThreadPoolExecutor(max_workers=3)
    executor.submit(flash_bands(db, song_id))
    executor.submit(bands_current_song(db, timing="delayed"))

def wrist_bands_animate(db):
    executor = ThreadPoolExecutor(max_workers=3)
    executor.submit(bands_helpers.animate_bands(db))

def api_for_new_song(db, song_id=None):
    # look up to see if preset exists for song.
    preset_effect = effects.get_effect_preset_by_song_id(db, song_id)
    if preset_effect:
        # preset present, select output effect, colour type and max colours
        output_effect = preset_effect.config['effect']
        colour_mode = preset_effect.colour_mode
        max_colours = preset_effect.max_colours
        # update state.colours from preset
        gradient = output_effect["config"]["gradient"]
        preset_colours = colour_helpers.extract_gradient(gradient)
        state.update_state_colours(db, preset_colours)
    else:
        # Song does not have a preset, create random effect with voter colours
        num_votes = songs.get_song_votes(db, song_id)
        random_effect = effects.get_random_effect(db, num_votes)
        colours = colour_helpers.create_colourscheme(db)
        colour_mode = random_effect.colour_mode
        max_colours = random_effect.max_colours        
        state.update_state_ledfx_colours(db, colour_mode, max_colours)
        colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
        state.update_state_colours(db, colourscheme)
        gradient = colour_helpers.create_gradient(colourscheme)
        output_effect = api_helpers.create_api_request_string(random_effect.type, gradient)

    api_helpers.perform_api_call(db, output_effect, "sticks")
    wrist_bands_new_song(db, song_id)
    return output_effect

def new_random_effect(db, song_id=None):
    num_votes = songs.get_song_votes(db, song_id)
    random_effect = effects.get_random_effect(db, num_votes)
    colours = colour_helpers.create_colourscheme(db)
    colour_mode = random_effect.colour_mode
    max_colours = random_effect.max_colours
    state.update_state_ledfx_colours(db, colour_mode, max_colours)    
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "floor")
    state.update_state_colours(db, colourscheme)
    gradient = colour_helpers.create_gradient(colourscheme)
    output_effect = api_helpers.create_api_request_string(random_effect.type, gradient)

    api_helpers.perform_api_call(db, output_effect, "sticks")
    bands_current_song(db, "instant")
    return output_effect


def new_random_colour(db, song_id=None):
    current_state = state.get_state(db)
    colour_mode = current_state.ledfx_colour_mode
    max_colours = current_state.ledfx_max_colours
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]    
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
    state.update_state_colours(db, colourscheme)
    gradient = colour_helpers.create_gradient(colourscheme)
    output_effect = api_helpers.create_api_request_string(current_state.ledfx_type, gradient)

    api_helpers.perform_api_call(db, output_effect, "sticks")
    bands_current_song(db, "instant")
    return output_effect


