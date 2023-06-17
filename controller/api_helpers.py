from .crud import state

from .models import EffectPreset

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