import colorsys

from random import randint, choice, shuffle

def generate_random_hex_colour() -> str:
    # returns a 6-digit hex colour in the format #AABBCC
    r = hex(randint(127,255))[2:]
    g = hex(randint(127,255))[2:]
    b = hex(randint(127,255))[2:]
    return f"#{r}{g}{b}"

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
    print(f"{colour_list=}, {len(colour_list)=}")

    if colour_list is None:
        return []
    if len(colour_list) == 0:
        return []
    if len(colour_list) == 1:
        return colour_list
    """Takes a list of hex-format colours and sorts them in brightness order"""
    colour_list_nums = [convert_to_rgb_int(colour) for colour in colour_list]
    colour_list_nums.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
    colour_list_hex = [convert_int_to_hex(colour) for colour in colour_list_nums]

    return colour_list_hex

def create_gradient(colour_list, limit=3):
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


def refine_colourscheme(colour_list: list, mode: str) -> str:
    # Takes a list of colours and a mode from an effect
    # returns an appropriately-altered gradient
    # if single, choose song voter
    # if adjacent, use song voter as adjacent basis
    # if gradient, find number and create gradient from voter and df present
    if mode == "gradient":
        colourscheme = colour_list
    elif mode == "adjacent":
        # randomly choose one colour
        # make gradient from adjacents
        random_colour = choose_random_colour(colour_list)[0]
        colourscheme = adjacent_colours(random_colour)
        
    elif mode == "single":
        # randomly choose one colour
        random_colour = choose_random_colour(colour_list)[0]
        colourscheme = [random_colour]
        
    return create_gradient(colourscheme)
            