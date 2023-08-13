"""Utility functions for project."""
import csv

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

def split_text(text, max_chars_per_line):
    """
    Split a text into lines of a maximum number of characters.

    Parameters
    ----------
    text : str
        The input text to be split.
    max_chars_per_line : int
        The maximum number of characters allowed per line.

    Returns
    -------
    list of str
        A list containing lines of the split text, where each line has
        a maximum of `max_chars_per_line` characters.
    """
    # store the lines of split text
    lines = []

    # split the text into words
    words = text.split()

    # initialize the current line with the first word
    current_line = words[0]

    # iterate through the remaining words
    for word in words[1:]:

        # Check if adding the next word to the current line exceeds the maximum length
        if len(current_line) + 1 + len(word) <= max_chars_per_line:
            # Add the word to the current line
            current_line += " " + word

        else:
            # add the current line to the list
            lines.append(current_line)

            # start a new line with the current word
            current_line = word
    # add the last line to the list
    lines.append(current_line)

    # return the list of split lines
    return lines
