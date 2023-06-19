"""Utility functions for project."""

import sys
import os
import csv
import time
from typing import AnyStr


# use "|" to seperate paragraphs
# TEXT = """
# Once upon a time, in a far away land, there once existed a cozy little cat cafe that goes by the name of “The Wildcat Cafe”. The cafe housed multifarious species of cats, each with their own unique personalities and quirks. They lived a peaceful life, being pampered by the cafe’s patrons. |
# One day, a mysterious virus broke out at the cat cafe, taking down every cat one by one. The virus was relentless and deadly, causing nausea, fever, seizures and eventually death. The cafe owners were left with no choice and hence, had to close down the cafe and release the remaining cats back into the forest. |
# Left stranded in the wild, the cats were anxious and traumatized by the catastrophe. They had to navigate through the forest fighting off potential predators, while also trying to unravel the mystery of the sudden virus outbreak. Upon a discussion amongst the cats, they have decided to choose [number_of_playable_character] cat(s) to protect them from predators while the rest help in navigation and finding clues to the mystery...
# """

def print_with_animation(string: AnyStr=None, line_length: int=80, speed: int=500) -> None:
    """Prints text with typing animation.

    Parameters
    ----------
    string : str
        The string to print. Defaults to None.
    
    line_length : int
        Max number of characters per line. Defaults to 80.

    speed : int 
        The speed of the typing animation (characters per minute).
        Defaults to 500.
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

        # sets the speed of typing animation, skips if char is a space
        if not char.isspace():
            time.sleep(speed / (5*3600))

        # pause at a fullstop
        if char == ".":
            time.sleep(0.3)

        sys.stdout.flush()

# prints string like a storyline
def execute_lore(lore: str=None):
    """
    prints the lore given. 
    Use "|" to split sentences into paragraphs.

    Parameters
    ----------
    lore : str
      the lore to be displayed. Defaults to None.
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

def csv_to_dict(file_path: str, key_column: str) -> dict:
    """Reads csv config file and store it in a dictionary.
    
    Parameters
    ----------
    file_path : str
        The file path of the csv file.
    key : str
        The column for keys.
    """
    result_dict = {}

    # open the CSV file
    with open(file_path, "r", encoding="utf-8") as file:
        # converts csv file to python dictionary
        csv_to_dict_reader = csv.DictReader(file)

        # iterate over each row and convert it to a dictionary
        for row in csv_to_dict_reader:

            # assign the key name to its dict of attributes
            key = str(row.pop(key_column))
            result_dict[key] = row

    return result_dict
