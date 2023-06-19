"""Utility functions for project."""

import sys
import os
import time
from typing import AnyStr


# use "|" to seperate paragraphs
TEXT = """
Once upon a time, in a far away land, there once existed a cozy little cat cafe that goes by the name of “The Wildcat Cafe”. The cafe housed multifarious species of cats, each with their own unique personalities and quirks. They lived a peaceful life, being pampered by the cafe’s patrons. |
One day, a mysterious virus broke out at the cat cafe, taking down every cat one by one. The virus was relentless and deadly, causing nausea, fever, seizures and eventually death. The cafe owners were left with no choice and hence, had to close down the cafe and release the remaining cats back into the forest. |
Left stranded in the wild, the cats were anxious and traumatized by the catastrophe. They had to navigate through the forest fighting off potential predators, while also trying to unravel the mystery of the sudden virus outbreak. Upon a discussion amongst the cats, they have decided to choose [number_of_playable_character] cat(s) to protect them from predators while the rest help in navigation and finding clues to the mystery...
"""
SPEED = 500

def print_with_animation(string: AnyStr=None, line_length: int=80) -> None:
    """
    prints text with typing animation

    text (str)
      the text to print with typing animation
    """
    buffer = ""

    # loops through every character in the string provided and prints
    # it one by one
    for char in string:
        buffer += char
        sys.stdout.write(char)

        # checks if line exceeded line_length limit
        if char == " " and len(buffer) > line_length:
            sys.stdout.write("\n") # insert new line
            buffer = "" # resets buffer

        if not char.isspace():
            time.sleep(SPEED / (5*3600))

        if char == ".":
            time.sleep(0.3)

        sys.stdout.flush()

# prints string like a storyline
def execute_lore(lore: str=None):
    """
    prints the lore given. 
    Use "|" to split sentences into paragraphs.

    lore (str)
      the lore to be displayed
    """
    # clear terminal
    os.system("clear")

    # splits lore into paragraphs
    paragraphs = lore.split("|")

    # loops through paragraphs to print to console
    for paragraph in paragraphs:
        print_with_animation(paragraph)
        input("\n\n\nPress enter to continue...")
        os.system("clear")

#execute_lore(TEXT)

def create_percentage_bar(title, current_stat: int, max_stat: int, bar_length: int=20):
    """Creates a percentage bar.

    Parameters
    ----------
    title : str
        The title of the stat.
    current_stat : int
        The current amount of that stat.
    max_stat : int
        The max amount of that stat.
    bar_length : int
        The length of the bar in number of characters. Defaults to 20.
    """


    # calculate the length of the bar to be filled
    filled_length = int(bar_length * current_stat / max_stat)

    # return the percentage bar string
    return f"{title}: {'█' * filled_length:▒<{bar_length}s} {current_stat}/{max_stat}"

strings = [
    ('shorterstring', 0),
    ('                  longerstring', 10),
    ('anotherstring', 40),
    ('            laststring', 60)
]

output = ''
last_column = 0

for string, start in strings:
    if start < last_column:
        string = ' ' * (last_column - start) + string
    else:
        string = string.rjust(start + len(string))
    
    output += string
    last_column = start + len(string)

print(output)