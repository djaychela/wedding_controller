# importing the requests library
import requests
import json
import random
  
# defining the api-endpoint 
API_ENDPOINT = "http://127.0.0.1:8888/api/virtuals/virtual-1/effects"
  

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
    "linear-gradient(90deg, rgb(0, 0, 0) 0%, rgb(255, 0, 0) 98%)"
    ]
 
effects_list = ["marching", "bands_matrix", "power", "rain", "glitch", "melt", "melt_and_sparkle", "water", "equalizer"]


while True:
    current_gradient = random.choice(gradient_list)
    current_effect = random.choice(effects_list)

    print(f"Effect Chosen: {current_effect}")
    print(f"Gradient Chosen: {current_gradient}")

    data = {
        "active": True,
	    "type": str(current_effect),
        "config": {
            "blur": 0.0,
            "gradient": str(current_gradient),
            "band_count" : 6
    }
    }

    data_dump = json.dumps(data)
    
    # sending post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, data = data_dump)
    
    # extracting response text 
    response_text = r.text
    print(f"The Response was: {response_text}")
    delay = input("Press Enter to change again...")