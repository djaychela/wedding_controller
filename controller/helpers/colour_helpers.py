from random import randint, choice

def generate_random_hex_colour():
    # returns a 6-digit hex colour in the format #AABBCC
    r = hex(randint(127,255))[2:]
    g = hex(randint(127,255))[2:]
    b = hex(randint(127,255))[2:]
    return f"#{r}{g}{b}"

def choose_random_colour(colour_list):
    # returns a single colour from a list, as a list with a single member
    return [choice(colour_list)]