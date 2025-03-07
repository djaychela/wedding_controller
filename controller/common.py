# Common functions

from .config import CONSOLE_OUTPUT

def output_to_console(mode, text_output, console):
    if CONSOLE_OUTPUT:
        if mode == "rule":
            console.rule(text_output)
        elif mode == "print":
            console.print(text_output)