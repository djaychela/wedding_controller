import sys
import time
import requests

from rich.console import Console

EFFECT_URL = "http://127.0.0.1:8000/state/change_effect"
COLOUR_URL = "http://127.0.0.1:8000/state/change_colour"
VIRTUAL_URL = "http://127.0.0.1:8888/api/virtuals/virtual-1/effects"
TIMEOUT = 180

console = Console()

while True:
    try:
        console.rule(f"[bold green] :computer: Requesting new effect and colour. :computer: [/]\n")
        effect = requests.get(EFFECT_URL)
        colour = requests.get(COLOUR_URL)
        virtual = requests.get(VIRTUAL_URL)
        console.print(f"New Colour: [bold green]{virtual.json()['effect']['config']['gradient']}[/]")
        console.print(f"New Effect: [bold green]{virtual.json()['effect']['name']}[/]")
        console.print(f"Sleeping for {TIMEOUT} Seconds...")
        time.sleep(TIMEOUT)
    except KeyboardInterrupt:
        sys.exit()

