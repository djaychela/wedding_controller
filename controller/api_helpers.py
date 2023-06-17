import json
import requests

from .crud import state

from .models import EffectPreset

STICKS_API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-1/effects"
BANDS_API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-bands/effects"
DMX_API_ENDPOINT = "http://192.168.1.51:8888/api/virtuals/virtual-dmx/effects"

def update_state_from_response(db, response):
    response_dict = response.json()    
    new_effect_preset = EffectPreset()
    new_effect_preset.name = response_dict['effect']['name']
    new_effect_preset.type = response_dict['effect']['type']
    new_effect_preset.config = response_dict["effect"]
    state.update_ledfx_state(db, new_effect_preset)


def create_api_request_string(type, gradient):
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
    
    data_dump = json.dumps(data)
    # sending post request and saving response as response object
    r = requests.post(url=endpoint, data=data_dump)
    if r:
        update_state_from_response(db, r)