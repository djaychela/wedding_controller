import time

from . import api_helpers


def animate_bands(db):
    true = True
    false = False

    init_data = {"on":true,
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

    api_helpers.perform_api_call(db, init_data, mode="bands_wled")

    sx = 20
    col_1 = [0,0,255]
    col_2 = [255,0,0]
    increment = 3   

    for i in range(0,100, increment):
        sx += increment
        col_1[2] -= increment
        col_1[0] = int(i * 1.5)
        col_2[0] -= increment
        col_2[2] = int(i * 1.5)

        data = {"seg":[{"sx":sx, "col":[col_1,col_2,[0,0,0]],}]}

        api_helpers.perform_api_call(db, data, mode="bands_wled")

        time.sleep(10)