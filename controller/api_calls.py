import time
import json
import copy

from concurrent.futures import ThreadPoolExecutor
from random import randint


from rich.console import Console

from .crud import state, effects, songs

from .helpers import colour_helpers, api_helpers

from .config import *

from .common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None

def dancefloor_entry_exit(db):
    current_state = state.get_state(db)
    if current_state.current_song_id in WRISTBANDS_DISABLED:
        # wristband colour changes disabled for the first song!
        output_to_console("rule", f"[bold green]:no_entry: Wristbands Disabled! :no_entry:[/]\n", console)
        return
    output_to_console("rule", f"[bold green]:light_bulb: Dancefloor Entry/Exit :light_bulb:[/]\n", console)
    colourscheme = colour_helpers.create_colourscheme(db)
    current_state = state.get_state(db)

    adj_colourscheme = colour_helpers.refine_colourscheme(db, colourscheme, current_state.ledfx_colour_mode, "floor")
    state.update_state_colours(db, adj_colourscheme)

    data = api_helpers.create_api_request_string(db, current_state.ledfx_type, adj_colourscheme)
    api_helpers.perform_api_call(db, data, "sticks")
    bands_current_song(db, timing="instant")

def bands_current_song(db, timing = "instant"):
    output_to_console("rule", f"[bold green]:light_bulb: Sending to Bands :light_bulb:[/]\n", console)
    if timing == "delayed":
        output_to_console("rule", f"[bold green]:clock10: Delay... :clock10:[/]\n", console)
        time.sleep(10)
    current_state = state.get_state(db)
    colourscheme = json.loads(current_state.colours)
    adj_colourscheme = colour_helpers.refine_colourscheme(db, colourscheme, current_state.ledfx_colour_mode, "song")
    
    data = api_helpers.create_api_request_string(db, "bands", adj_colourscheme)
    api_helpers.perform_api_call(db, data, mode="bands")

def flash_bands(db, song_id=None):
    """Looks up voters for current song"""
    output_to_console("rule", f"[bold green]:light_bulb: Flashing Bands :light_bulb:[/]\n", console)
    song_colours = songs.get_song_colours(db, song_id, mode="list", strict=True)
    if len(song_colours) == 0:
        # No-one voted, so set the bands for the song
        bands_current_song(db, "instant")
        return
    
    data = api_helpers.create_api_request_string(db, "bands_flash", song_colours, flash=True)
    api_helpers.perform_api_call(db, data, mode="bands")

def bands_slow_songs(db, song_id=None):
    """Slower bands for first three songs.  Colours from state (from preset)"""
    output_to_console("rule", f"[bold green]:light_bulb: Bands for Slow Songs :light_bulb:[/]\n", console)
    current_state = state.get_state(db)
    colourscheme = json.loads(current_state.colours)
    bands_slow = f"bands_slow_{SPECIAL_SONGS.index(song_id)}"
    data = api_helpers.create_api_request_string(db, bands_slow, colourscheme)
    api_helpers.perform_api_call(db, data, mode="bands")

def wrist_bands_new_song(db, song_id):
    if song_id in SPECIAL_SONGS:
        # first three songs, wrist bands have separate presets.
        bands_slow_songs(db, song_id)
    else:
        # perform both calls for wrist band.  Second call is delayed.
        executor = ThreadPoolExecutor(max_workers=3)
        executor.submit(flash_bands(db, song_id))
        # TODO:  RE-ENABLE THIS!!!
        executor.submit(bands_current_song(db, timing="delayed"))

def api_for_new_song(db, song_id=None):
    # look up to see if preset exists for song.
    preset_effect = effects.get_effect_preset_by_song_id(db, song_id)
    output_to_console("rule", f"[cyan]{songs.get_song_artist_title(db, song_id)}[/]", console)
    if preset_effect:
        # preset present, select output effect, colour type and max colours
        output_to_console("rule", f"[bold green]:light_bulb: Loading Preset! :light_bulb:[/]\n", console)
        api_request_1 = preset_effect.config['effect']
        # output_to_console("print", f"{api_request_1=}", console)
        colour_mode = preset_effect.colour_mode
        max_colours = preset_effect.max_colours
        # find matching effect to set id for updates
        matching_effect = effects.find_effect_match(db, preset_effect.type, colour_mode, max_colours)
        state.update_effect_id(db, matching_effect.id)
        # update state.colours from preset
        gradient = api_request_1["config"]["gradient"]
        preset_colours = colour_helpers.extract_gradient(gradient)
        state.update_state_colours(db, preset_colours)
        # create and update api_request_2 for virtual-2
        api_request_2 = copy.deepcopy(api_request_1)
        api_request_2['config']['band_count'] = 2
        api_request_2['config']['gradient_repeat'] = 2
    else:
        # Song does not have a preset, create random effect with voter colours
        output_to_console("rule",f"[bold green]:shuffle_tracks_button: Creating Effect :shuffle_tracks_button:[/]\n", console)
        num_votes = songs.get_song_votes(db, song_id)
        random_effect = effects.get_random_effect(db, num_votes)
        state.update_effect_id(db, random_effect.id)
        output_to_console("print", f"Effect Chosen: {random_effect.type}", console)
        colours = colour_helpers.create_colourscheme(db)
        colour_mode = random_effect.colour_mode
        max_colours = random_effect.max_colours        
        state.update_state_ledfx_colours(db, colour_mode, max_colours)
        colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
        state.update_state_colours(db, colourscheme)
        
        api_request_1 = api_helpers.create_api_request_string(db, random_effect.type, colourscheme, random_effect.id)
        api_request_2 = api_helpers.create_api_request_string(db, random_effect.type, colourscheme, random_effect.id, sticks_2=True)

    if STICKS:
        api_helpers.perform_api_call(db, api_request_1, "sticks")
    if STICKS_2:
        api_helpers.perform_api_call(db, api_request_2, "sticks_2")
    if BANDS:
        wrist_bands_new_song(db, song_id)
    return api_request_1

def new_random_effect(db, song_id=None):
    output_to_console("rule", f"[bold green]:light_bulb: New Random Effect :light_bulb:[/]\n", console)
    if not STANDALONE:
        num_votes = songs.get_song_votes(db, song_id)
    else:
        # There are no votes, so choose a decent number of colours (otherwise you end up 1)
        num_votes = 6
    random_effect = effects.get_random_effect(db, num_votes)
    state.update_effect_id(db, random_effect.id)
    output_to_console("print", f"Effect Chosen: {random_effect.type}", console)
    if not STANDALONE:
        colours = colour_helpers.create_colourscheme(db)
        colour_mode = random_effect.colour_mode
        max_colours = random_effect.max_colours
        state.update_state_ledfx_colours(db, colour_mode, max_colours)    
        colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "floor")
        state.update_state_colours(db, colourscheme)
    else:
        colourscheme = new_random_colour_standalone(db)
    
    api_request_1 = api_helpers.create_api_request_string(db, random_effect.type, colourscheme, random_effect.id)
    if STICKS:
        api_helpers.perform_api_call(db, api_request_1, "sticks")

    api_request_2 = api_helpers.create_api_request_string(db, random_effect.type, colourscheme, random_effect.id, sticks_2=True)
    if STICKS_2:
        api_helpers.perform_api_call(db, api_request_2, "sticks_2")

    if BANDS:
        bands_current_song(db, "instant")
    return api_request_1


def new_random_colour(db, song_id=None):
    output_to_console("rule", f"[bold green]:light_bulb: New Random Colour :light_bulb:[/]\n", console)
    current_state = state.get_state(db)
    colour_mode = current_state.ledfx_colour_mode
    max_colours = current_state.ledfx_max_colours
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]    
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
    state.update_state_colours(db, colourscheme)
    
    api_request_1 = api_helpers.create_api_request_string(db, current_state.ledfx_type, colourscheme)
    if STICKS:
        api_helpers.perform_api_call(db, api_request_1, "sticks")

    api_request_2 = api_helpers.create_api_request_string(db, current_state.ledfx_type, colourscheme, sticks_2=True)
    if STICKS_2:
        api_helpers.perform_api_call(db, api_request_2, "sticks_2")

    if BANDS:
        bands_current_song(db, "instant")
    
    return api_request_1

def new_random_colour_standalone(db, song_id=None):
    output_to_console("rule", f"[bold green]:light_bulb: New Random Colour :light_bulb:[/]\n", console)
    current_state = state.get_state(db)
    colour_mode = current_state.ledfx_colour_mode
    max_colours = current_state.ledfx_max_colours
    max_colours = randint(1, max_colours) # Provide variety!
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]    
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
    state.update_state_colours(db, colourscheme)

    return colourscheme
