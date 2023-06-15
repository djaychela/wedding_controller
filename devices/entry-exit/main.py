import os
import ipaddress
import ssl
import time
import wifi
import socketpool
import adafruit_requests as requests
import microcontroller

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import PURPLE, GREEN, RED

import neopixel
import digitalio
import board
import busio
import json

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.uart import PN532_UART

# setup PN532 comms and connect

uart = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=115200, timeout=0.1)
pn532 = PN532_UART(uart, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# variables, etc...

pixel_pin = board.GP6
num_pixels = 20
ORDER = neopixel.GRB
MAX_BRIGHTNESS = 0.1
entry_mode = True
api_url_base = "http://192.168.1.183:8000"

# mode settings

if entry_mode:
    COUNTER_COLOUR = (0,127,0)
    api_url = api_url_base + "/dancefloor/entry"
else:
    COUNTER_COLOUR = (127,0,0)
    api_url = api_url_base + "/dancefloor/exit"

# create LED ring

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=MAX_BRIGHTNESS, auto_write=False, pixel_order=ORDER
)
comet = Comet(pixels, speed=0.001, color=COUNTER_COLOUR, tail_length=10, bounce=False, ring=True)



def hex_to_rgb(hex_colour):
    return tuple(int(hex_colour[i:i+2], 16) for i in (0, 2, 4))

def flash_ring(rgb_colour, cycles=5):
    for c in range(cycles):
        for i in range(0, 10):
            pixels.brightness = (i / 10) * MAX_BRIGHTNESS 
            pixels.fill(rgb_colour)
            pixels.show()
            time.sleep(0.01)
        for i in range(10, 0, -1):
            pixels.brightness = (i / 10) * MAX_BRIGHTNESS 
            pixels.fill(rgb_colour)
            pixels.show()
            time.sleep(0.01)
        pixels.fill((0,0,0))
        pixels.show()
        pixels.brightness = MAX_BRIGHTNESS

    
def pixel_animation(rgb_colour, mode=True):
    if mode:
        colours = ((0,0,0), rgb_colour)
    else:
        colours = (rgb_colour, (0,0,0))
    pixels.fill(colours[0])
    for i in range(num_pixels):
        pixels[i] = colours[1]
        time.sleep(0.03)
        pixels.show()
    for i in range(num_pixels):
        pixels[i] = (0,0,0)
        time.sleep(0.03)
        pixels.show()
        
def uid_to_nfc_id(uid):
    uid_list = ["{0:#0{1}x}".format(i,4) for i in uid]
    nfc_id = ":".join([u[2:] for u in uid_list])
    return nfc_id

def display_status(status):
    if status == 0:
        colour = response.json()[0]["colour"]
        rgb_colour = hex_to_rgb(colour[1:])
        pixel_animation(rgb_colour, True)
        flash_ring((0,255,0))
    elif status == 1:
        # Dancer already on dance floor.
        colour = response.json()[0]["colour"]
        rgb_colour = hex_to_rgb(colour[1:])
        flash_ring(rgb_colour, 3)
    elif status == 2:
        # Dancer leaving dance floor
        colour = response.json()[0]["colour"]
        rgb_colour = hex_to_rgb(colour[1:])
        flash_ring((rgb_colour), 3)
        pixel_animation(rgb_colour, False)

    else:
        flash_ring((255,0,0), 5)


print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")
pixel_animation((255,255,255), True)
pixel_animation((0,255,0), True)


pool = socketpool.SocketPool(wifi.radio)
requests = requests.Session(pool, ssl.create_default_context())

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

pn532.SAM_configuration()


while True:
    try:
        # Check for NFC to read...
        uid = pn532.read_passive_target(timeout=0.5)

        comet.animate()
        
        if uid is None:
            continue
        
        nfc_id = uid_to_nfc_id(uid)
        
        api_payload = {"dancer_nfc_id": nfc_id}
        api_json = json.dumps(api_payload)
        response = requests.post(api_url, data=api_json)
        
        status = response.json()[1]["status"]
        display_status(status)

    
    except RuntimeError:
        for i in range(3):
            flash_ring((255,255,0),2)
            time.sleep(1)

    
    except Exception as e:
        print("Error:\n", str(e))
        print(e)
        print("Resetting microcontroller in 10 seconds")
        for i in range(3):
            flash_ring((255,0,0),2)
            time.sleep(1)
        microcontroller.reset()
