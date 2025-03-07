import colorsys
import math
import re

from rich.console import Console

from random import choice, shuffle, uniform

from ..crud import dancefloor, state, songs

from ..config import *

from ..common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None


def generate_random_hex_colour() -> str:
    # returns a 6-digit hex colour in the format #AABBCC
    candidates = ["#ff0000", "#00ff00", "#0000ff", "#fa9d00", "#ffff00", "#9370db", "#808080", "#00ffff", "#ff00ff"]	
    colour = choice(candidates)
    output_to_console("print", f"Random Colour: {colour}", console)
    return colour

def choose_random_colour(colour_list):
    # returns a single colour from a list, as a list with a single member
    return [choice(colour_list)]


def convert_int_to_hex(colour_tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        colour_tuple[0], colour_tuple[1], colour_tuple[2]
    )


def convert_to_rgb(colour_string):
    colours = colour_string.lstrip("#")
    return f"rgb{tuple(int(colours[i:i+2], 16) for i in (0, 2, 4))}"


def convert_to_rgb_int(colour_string):
    colours = colour_string.lstrip("#")
    return tuple(int(colours[i : i + 2], 16) for i in (0, 2, 4))


def adjacent_colours(rgb_colour, d=30 / 360):  # Assumption: r, g, b in [0, 255]
    r, g, b = [c / 255 for c in convert_to_rgb_int(rgb_colour)]  # Convert to [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # RGB -> HLS
    h = [(h + d) % 1 for d in (-d, d)]  # Rotation by d
    adjacent = [
        list(map(lambda x: int(round(x * 255)), colorsys.hls_to_rgb(hi, l, s)))
        for hi in h
    ]  # H'LS -> new RGB
    hex_list = [convert_int_to_hex(colour) for colour in adjacent]
    hex_list.insert(1, rgb_colour)
    return hex_list

def sort_colour_list(colour_list):
    def lum (r,g,b):
        return math.sqrt( .241 * r + .691 * g + .068 * b )


    if colour_list is None:
        return []
    if len(colour_list) == 0:
        return []
    if len(colour_list) == 1:
        return colour_list
    """Takes a list of hex-format colours and sorts them in brightness order"""
    
    colour_list_nums = [convert_to_rgb_int(colour) for colour in colour_list]
    colour_list_nums.sort(key=lambda rgb: lum(*rgb), reverse=False)
    colour_list_hex = [convert_int_to_hex(colour) for colour in colour_list_nums]

    return colour_list_hex

def create_gradient(colour_list, limit=6, flash=False):
    """takes a list of hex-format colours, and outputs
    a linear gradient for ledfx based on the colour list.
    if there are more than limit entries, only a random selection
    of length limit will be added to the gradient."""
    colour_list = sort_colour_list(colour_list)
    if len(colour_list) > limit:
        shuffle(colour_list)
        colour_list = colour_list[:limit]
    if len(colour_list) == 0:
        colour_list = [generate_random_hex_colour()]
    if len(colour_list) == 1:
        # if a single colour, 50% chance of solid colour
        if uniform(0,1) > 0.5:
            return colour_list[0]
    # modify list for flashing
    if flash:
        # insert #000000 at every other index
        colours = [[colour, "#000000"] for colour in colour_list]
        colour_list = [item for sublist in colours for item in sublist]
    increment = int(98 / len(colour_list))
    location = 0
    stem = "linear-gradient(90deg, rgb(0, 0, 0) 0%"
    for colour in colour_list:
        colour_rgb = convert_to_rgb(colour)
        location += increment
        current_colour = f", {colour_rgb} {location}%"
        stem += current_colour
    stem += ")"
    return stem

def create_colourscheme(db) -> list:
    """ Gets the current relevant colours - 
    song voters (first, but randomised in order)
    dancefloor members (in reverse order, newest first)
    returns a list of #AABBCC format colours """
    output_to_console("print", "[bright_cyan]colour_helpers[/].[bold]create_colourscheme[/]", console)
    current_state = state.get_state(db)
    voter_colours = songs.get_song_colours(db, current_state.current_song_id, mode="list")
    if voter_colours == None:
        voter_colours = []
    shuffle(voter_colours)
    output_to_console("print", f"{voter_colours=}", console)
    dancefloor_colours = dancefloor.get_dancefloor_colours(db, list_mode=True)
    # remove any duplication
    dancefloor_colours = [colour for colour in dancefloor_colours if colour not in voter_colours]
    current_colours = voter_colours + dancefloor_colours
    if len(current_colours) == 0:
        # No votes, no-one on the dancefloor, so return a single random colour
        current_colours = [generate_random_hex_colour()]
    state.update_state_colours(db, current_colours)
    output_to_console("print", f"{current_colours=}", console)
    return current_colours


def refine_colourscheme(db, colour_list: list, colour_mode: str, mode: str) -> list:
    # Takes a list of colours and a mode from an effect
    # returns an appropriately-altered gradient
    output_to_console("print", "[bright_cyan]colour_helpers[/].[bold]refine_colourscheme[/]", console)
    output_to_console("print", f"{colour_list=}, {colour_mode=}, {mode=}", console)
    colour_list = list(set(colour_list))
    if colour_mode == "gradient":
        # limit to current length in settings - same for both modes
        current_state = state.get_state(db)
        ledfx_max_colours = current_state.ledfx_max_colours
        unsorted_colourscheme = colour_list[:ledfx_max_colours]
        colourscheme = sort_colour_list(unsorted_colourscheme)
    elif colour_mode == "adjacent":
        # song change - pick a voter (random), adjacent the colours
        # dancefloor  - adjacent based on latest to dancefloor
        if mode == "song":
            colour = colour_list[0]
        else:
            colour = dancefloor.get_last_n_dancers(db, True, 1)[0]
        # make colourscheme of adjacents
        colourscheme = adjacent_colours(colour)
        
    elif colour_mode == "single":
        # song change - pick a voter (random) and they are the colour
        # dancefloor  - new single colour is latest to dancefloor
        if mode == "song":
            colourscheme = [colour_list[0]]
        else:
            colourscheme = dancefloor.get_last_n_dancers(db, True, 1)
        
    output_to_console("print", f"Returning {colourscheme=}", console)
    return colourscheme
            
def extract_gradient(gradient_string):
    """Takes a gradient string in rgb or hex value.
    Returns a list of hex values of colours."""
    rgb_matches = re.findall(r"(\d+),\s*(\d+),\s*(\d+)", gradient_string)
    hex_matches = [ convert_int_to_hex([int(x) for x in rgb]) for rgb in rgb_matches]
    hex_finds = re.findall(r"#[A-Fa-f0-9]+", gradient_string)
    if hex_finds:
        hex_matches += hex_finds
    return hex_matches
