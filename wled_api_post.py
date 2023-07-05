# importing the requests library
import requests
import json
import random
import time
  
# defining the api-endpoint 
WLED_BANDS_API_ENDPOINT = "http://192.168.1.33/json"

true = True
false = False
  
data = {"on":true,
        "bri":255,
        "transition":7,
        "ps":-1,
        "pl":-1,
        "nl":{"on":false,"dur":60,"mode":1,"tbri":0,"rem":-1},
        "udpn":{"send":false,"recv":true},
        "lor":0,"mainseg":0,
        "seg":[{"id":0,"start":0,"stop":4,"len":4,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":127,"cct":127,"col":[[0,0,255],[0,0,0],[0,0,0]],"fx":0,"sx":128,"ix":128,"pal":0,"c1":128,"c2":128,"c3":16,"sel":true,"rev":false,"mi":false,"o1":false,"o2":false,"o3":false,"si":0,"m12":0}]
        }

data = {"seg":[{"id":0,"start":0,"stop":4,"len":4,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":127,"cct":127,"col":[[0,0,255],[0,0,0],[0,0,0]],"fx":1,"sx":128,"ix":128,"pal":0,"c1":128,"c2":128,"c3":16,"sel":true,"rev":false,"mi":false,"o1":false,"o2":false,"o3":false,"si":0,"m12":0}]}
    
data = {"on":true,
        "bri":255,
}

data = {"seg":[{"sx":20,}]}

data = {"seg":[{"sx":20, "col":[[155,0,155],[155, 0, 155],[0,0,0]],}]}

data = {"seg":[{"sx":20, "col":[[255,0,0],[0, 0, 255],[0,0,0]],}]}

data = {"on":true,
        "bri":255,
        "transition":7,
        "ps":-1,
        "pl":-1,
        "nl":{"on":false,"dur":60,"mode":1,"tbri":0,"rem":-1},
        "udpn":{"send":false,"recv":true},
        "lor":0,
        "mainseg":0,
        "seg":[{"id":0,
                "start":0,
                "stop":4,
                "len":4,
                "grp":1,
                "spc":0,
                "of":0,
                "on":true,
                "frz":false,
                "bri":127,
                "cct":127,
                "col":[[0,0,255],[255,0,0],[0,0,0]],
                "fx":108,
                "sx":20,
                "ix":133,
                "pal":2,
                "c1":128,
                "c2":128,
                "c3":16,
                "sel":true,
                "rev":false,
                "mi":false,
                "o1":false,
                "o2":false,
                "o3":false,
                "si":0,
                "m12":1}]}

data_dump = json.dumps(data)

# sending post request and saving response as response object
r = requests.post(url = WLED_BANDS_API_ENDPOINT, data = data_dump)

# extracting response text 
response_text = r.text
print(f"The Response was: {response_text}")
# delay = input("Press Enter to change again...")

# exit()

sx = 20
col_1 = [0,0,255]
col_2 = [255,0,0]
increment = 10

for i in range(0,100, increment):
    sx += increment
    col_1[2] -= increment
    col_1[0] = int(i * 1.5)
    col_2[0] -= increment
    col_2[2] = int(i * 1.5)

    data = {"seg":[{"sx":sx, "col":[col_1,col_2,[0,0,0]],}]}
    print(f"Sending {data=}")
    data_dump = json.dumps(data)
    r = requests.post(url = WLED_BANDS_API_ENDPOINT, data = data_dump)

    time.sleep(10)


"""{"state":{"on":true,"bri":128,"transition":7,"ps":-1,"pl":-1,"nl":{"on":false,"dur":60,"mode":1,"tbri":0,"rem":-1},"udpn":{"send":false,"recv":true},"lor":0,"mainseg":0,"seg":[{"id":0,"start":0,"stop":4,"len":4,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":255,"cct":127,"col":[[255,0,0],[0,0,0],[0,0,0]],"fx":0,"sx":128,"ix":128,"pal":0,"c1":128,"c2":128,"c3":16,"sel":true,"rev":false,"mi":false,"o1":false,"o2":false,"o3":false,"si":0,"m12":0}]}"""

# Blue > Red fade:

data = {"on":true,
        "bri":255,
        "transition":7,
        "ps":-1,
        "pl":-1,
        "nl":{"on":false,"dur":60,"mode":1,"tbri":0,"rem":-1},
        "udpn":{"send":false,"recv":true},
        "lor":0,
        "mainseg":0,
        "seg":[{"id":0,
                "start":0,
                "stop":4,
                "len":4,
                "grp":1,
                "spc":0,
                "of":0,
                "on":true,
                "frz":false,
                "bri":127,
                "cct":127,
                "col":[[0,0,255],[255,0,0],[0,0,0]],
                "fx":108,
                "sx":20,
                "ix":133,
                "pal":2,
                "c1":128,
                "c2":128,
                "c3":16,
                "sel":true,
                "rev":false,
                "mi":false,
                "o1":false,
                "o2":false,
                "o3":false,
                "si":0,
                "m12":1}]}
