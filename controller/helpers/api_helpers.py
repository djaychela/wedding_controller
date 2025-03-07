import json
import requests

import copy

from rich.console import Console

from .. crud import state, effects

from .. models import EffectPreset

from . import colour_helpers

from .. config import *

from .. common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None

def update_state_from_response(db, response, mode):
    response_dict = response.json()    
    new_effect_preset = EffectPreset()
    new_effect_preset.name = response_dict['effect']['name']
    new_effect_preset.type = response_dict['effect']['type']
    new_effect_preset.config = response_dict["effect"]
    if mode == "sticks":
        state.update_state_ledfx(db, new_effect_preset)
    elif mode == "bands":
        state.update_state_bands(db, new_effect_preset)


def create_api_request_string(db, fx_type, colourscheme, effect_id=None, sticks_2=False, flash=False):
    """Looks up a config from the database for the current effect id if provided, and
    substitutes sentinel values for the colourscheme / gradient where appropriate.
    If effect_id is not provided, then hard-coded dictionaries have values replaced in them, and are
    returned instead."""

    gradient = colour_helpers.create_gradient(colourscheme, flash=flash)

    if effect_id is not None:
        # output_to_console("print", f"Effect ID: {effect_id}", console)
        # output_to_console("print", f"Colourscheme: {colourscheme}", console)
        effect_config = copy.deepcopy(effects.get_effect_string_by_id(db, effect_id))
        # output_to_console("print", f"{id(effect_config)=}", console)
        # output_to_console("print", f"Effect Config: {effect_config}", console)
        index = list(effect_config['config'].values())
        gradient_indices = [i for i, x in enumerate(index) if x == "#GGGGGG"]
        other_indices = [i for i, x in enumerate(index) if x == "#HHHHHH"]
        # output_to_console("print", f"Gradient Indices: {gradient_indices}", console)
        # output_to_console("print", f"Other Indices:    {other_indices}", console)
        if gradient_indices:
            # output_to_console("print", f"Keys: {[list(effect_config['config'].keys())[g] for g in gradient_indices]}", console)
            for key in [list(effect_config['config'].keys())[g] for g in gradient_indices]:
                # output_to_console("print", f"Replacing {key}", console)
                effect_config['config'][key] = gradient
        if other_indices:
            # output_to_console("print", f"Keys: {[list(effect_config['config'].keys())[o] for o in other_indices]}", console)
            for idx, key in enumerate([list(effect_config['config'].keys())[o] for o in other_indices]):
                # output_to_console("print", f"Replacing {key}", console)
                try:
                    effect_config['config'][key] = colourscheme[idx]
                except IndexError:
                    effect_config['config'][key] = colourscheme[0]
        if sticks_2:
            effect_config['config']['band_count'] = 2
            effect_config['config']['gradient_repeat'] = 2
        # output_to_console("print", f"Final Effect Config: {effect_config}", console)

        return effect_config

    # generic construction strings
    if fx_type =="bands":
        data = {"config": {"background_brightness": 1.0, "background_color": "#000000", "beat_decay": 1.0, "blur": 0.0, "brightness": 1.0, "flip": False, "gradient": gradient, "gradient_roll": 0.0, "mirror": False, "strobe_decay": 1.5, "strobe_frequency": "1/4 (.o. )"}, "name": "BPM Strobe", "type": "strobe"}
    elif fx_type == "bands_flash":
        data = {"config": {"gradient": gradient, "gradient_roll": 0.2, "modulation_effect": "sine", "modulate": False, "blur": 0.0, "modulation_speed": 1.0, "speed": 2.7, "mirror": False, "flip": False, "brightness": 1.0, "background_brightness": 1.0, "background_color": "#000000"}, "name": "Gradient", "type": "gradient"}
    # bands special cases for first three songs
    elif fx_type == "bands_slow_0":
        data = {"config": {"background_brightness": 1.0, "background_color": "#000000", "blur": 4.5, "brightness": 1.0, "flip": True, "gradient_name": "Dancefloor", "solid_color": False, "gradient": "linear-gradient(90deg, rgb(255, 0, 0) 0%, rgb(0, 0, 255) 50%, rgb(255, 0, 0) 100%)", "gradient_repeat": 1, "gradient_roll": 1.0, "mirror": False, "speed": 4.9}, "name": "Fade", "type": "fade"}
    elif fx_type == "bands_slow_1":
        data = {"config": {"gradient": "linear-gradient(90deg, rgb(255, 0, 0) 0%, rgb(255, 0, 255) 25%, rgb(0, 0, 255) 50%, rgb(255, 0, 255) 75%, rgb(255, 0, 0) 100%)", "gradient_roll": 0.4, "modulation_effect": "sine", "modulate": False, "blur": 0.0, "modulation_speed": 1.0, "speed": 0.5, "mirror": False, "flip": False, "brightness": 1.0, "background_brightness": 1.0, "background_color": "#000000"}, "name": "Gradient", "type": "gradient"}
    elif fx_type == "bands_slow_2":
        data = {"config": {"background_brightness": 1.0, "background_color": "#000000", "beat_decay": 1.0, "blur": 0.0, "brightness": 1.0, "flip": False, "gradient": "#ff0000", "gradient_roll": 0.0, "mirror": False, "strobe_decay": 1.5, "strobe_frequency": "1/1 (.,. )"}, "name": "BPM Strobe", "type": "strobe"}
    else:
        # safe fallback in case something has been missed when adding specific lookups above.
        if sticks_2:
            data = {
                "active": True,
                "type": str(fx_type),
                "config": {
                    "blur": 0.0,
                    "gradient": gradient,
                    "band_count" : 2,
                    "gradient_repeat": 2,
                }
            }
        else:
            data = {
                "active": True,
                "type": str(fx_type),
                "config": {
                    "blur": 0.0,
                    "gradient": gradient,
                    "band_count" : 10,
                    "gradient_repeat": 10,
                }
            }
    return data

def perform_api_call(db, data, mode="sticks"):
    if mode == "sticks":
        endpoint = STICKS_API_ENDPOINT
    elif mode == "sticks_2":
        endpoint = STICKS_2_API_ENDPOINT
    elif mode == "bands":
        endpoint = BANDS_API_ENDPOINT
    elif mode == "bands_wled":
        endpoint = WLED_BANDS_API_ENDPOINT
    else:
        endpoint = DMX_API_ENDPOINT
    
    if MODE == "test":
        output_to_console("rule", f"[bold red]:test_tube: Test Mode Active :test_tube:[/]\n", console)
        output_to_console("print", f"API Data sent to :{endpoint}", console)
        output_to_console("print", f"{data=}", console)

        # TODO: update state from data
    else:
        output_to_console("rule", f"[bold green]:chequered_flag: API Call - {mode} :chequered_flag:[/]\n", console)
        data_dump = json.dumps(data)
        # sending post request and saving response as response object
        r = requests.post(url=endpoint, data=data_dump)
        if r.status_code == 200:
            output_to_console("rule", f"[bold green]:thumbs_up: 200 :thumbs_up:[/]\n", console)
            if mode != "sticks_2":
                update_state_from_response(db, r, mode)
        else:
            output_to_console("rule", f"[bold green]:no_entry_sign::thumbs_down: {r.status_code} :thumbs_down::no_entry_sign:[/]\n", console)
    
