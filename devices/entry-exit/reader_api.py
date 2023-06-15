import os
import ipaddress
import ssl
import time
import wifi
import socketpool
import adafruit_requests as requests
import microcontroller

import neopixel
import digitalio
import board
import busio
import json

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.uart import PN532_UART

uart = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=115200, timeout=0.1)
pn532 = PN532_UART(uart, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)
requests = requests.Session(pool, ssl.create_default_context())

api_url = "http://192.168.1.183:8000/dancefloor/entry"

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

pn532.SAM_configuration()

# "RuntimeError: Did not receive expected ACK from PN532!"

pixel_pin = board.GP6
num_pixels = 20
ORDER = neopixel.GRB
MAX_BRIGHTNESS = 0.1

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=MAX_BRIGHTNESS, auto_write=False, pixel_order=ORDER
)

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

    
def pixel_animation(rgb_colour):
    pixels.fill((0,0,0))
    for i in range(num_pixels):
        pixels[i] = rgb_colour
        time.sleep(0.03)
        pixels.show()
    for i in range(num_pixels):
        pixels[i] = (0,0,0)
        time.sleep(0.03)
        pixels.show()



while True:
    try:
        # Check for NFC to read...
        uid = pn532.read_passive_target(timeout=0.5)
        # print(".", end="")
        # Try again if nothing is read.
        if uid is None:
            continue
        uid_list = ["{0:#0{1}x}".format(i,4) for i in uid]
        nfc_id = ":".join([u[2:] for u in uid_list])
        
        # print("Found card with UID:", [hex(i) for i in uid])
        # print("UID List: ", nfc_id)
        api_payload = {"dancer_nfc_id": nfc_id}
        api_json = json.dumps(api_payload)
        response = requests.post(api_url, data=api_json)
        if response.json() is not None:
            colour = response.json()["colour"]
            print(colour)
            rgb_colour = hex_to_rgb(colour[1:])
            pixel_animation(rgb_colour)
            flash_ring((0,255,0))
        else:
            flash_ring((255,0,0), 2)

        # print(response.json())
    
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()


