import json
import requests

from ..crud import state

from ..models import EffectPreset, State

STICKS_API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-1/effects"
BANDS_API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-bands/effects"
DMX_API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-dmx/effects"
MODE = "test"

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

def update_state_colours(db, colour_type, max_colours):
    new_state = State()
    new_state.ledfx_colour_mode = colour_type
    new_state.ledfx_max_colours = max_colours
    state.update_state_ledfx_colours(db, new_state)


def create_api_request_string(type, gradient):
    # TODO: do lookup of prototype strings from database
    # create dictionary
    # insert parameters
    # return dictionary
    data = {
        "active": True,
	    "type": str(type),
        "config": {
            "blur": 0.0,
            "gradient": gradient,
            "band_count" : 10
        }
    }
    return data

def perform_api_call(db, data, mode="sticks"):
    if mode == "sticks":
        endpoint = STICKS_API_ENDPOINT
    elif mode == "bands":
        endpoint = BANDS_API_ENDPOINT
    else:
        endpoint = DMX_API_ENDPOINT
    
    if MODE == "test":
        print(f"API Data sent to :{endpoint}")
        print(f"{data=}")
        # TODO: update state from data
    else:
        data_dump = json.dumps(data)
        # sending post request and saving response as response object
        r = requests.post(url=endpoint, data=data_dump)
        if r:    
            update_state_from_response(db, r, mode)
    