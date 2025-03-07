import sys
import time
import requests

from rich.console import Console

from controller.config import *

from controller.common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None

while True:
    try:
        output_to_console("rule", f"[bold green] :computer: Requesting new effect and colour. :computer: [/]\n", console)
        effect = requests.get(EFFECT_URL)
        colour = requests.get(COLOUR_URL)
        virtual = requests.get(VIRTUAL_URL)
        output_to_console("print", f"New Colour: [bold green]{virtual.json()['effect']['config']['gradient']}[/]", console)
        output_to_console("print", f"New Effect: [bold green]{virtual.json()['effect']['name']}[/]", console)
        output_to_console("print", f"Sleeping for {TIMED_CALL_TIMEOUT} Seconds...", console)
        time.sleep(TIMED_CALL_TIMEOUT)
    except KeyboardInterrupt:
        sys.exit()

