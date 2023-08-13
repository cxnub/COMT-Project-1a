"""Module for switch character frame."""
import os
from functools import partial
from typing import TYPE_CHECKING, List

import tkinter as tk
from tkinter import ttk

from combatgame.game_logic.characters import BaseCharacter

if TYPE_CHECKING:
    from main import GameApp

# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

class SwitchCharacterFrame(ttk.Frame):
    """The switch character frame."""

    def __init__(self, master: "GameApp", player_characters: List[BaseCharacter], **kw):
        """
        Initialize the SwitchCharacterFrame.

        Parameters
        ----------
        master : GameApp
            The GameApp instance.
        player_characters : List[BaseCharacter]
            A list of player characters participating in the combat.
        **kw
            Additional keyword arguments for configuring the frame.
        """

        super().__init__(master, **kw)

        self.master = master

        # store character options
        self.character_options = {}

        for character in player_characters:
            self.character_options[f"{character.name}\n({character.job_class})"] = character

        # list to store character images
        self.character_images = []

        # list to store boolean variables for character selection buttons
        self.buttons_checked = []

        self.create_character_frame()
        self.create_characters_buttons()

        self.navigation_buttons_label = ["Cancel"]

        self.create_navigation_buttons()


    def create_character_frame(self):
        """Create the character frame."""

        # configure character label frame
        self.character_frame = ttk.Labelframe(self)
        self.character_frame.configure(
            height=350,
            labelanchor="n",
            text='Switch a Character',
            width=400)

        self.character_frame.grid(
            column=0, columnspan=2, padx=5, pady=5, row=3)
        self.character_frame.grid_propagate(0)
        self.character_frame.grid_anchor("center")
        self.character_frame.rowconfigure("all", pad=20)
        self.character_frame.columnconfigure("all", pad=20)

    def create_characters_buttons(self):
        """Create the characters buttons"""

        for index, (label_text, character_instance) in enumerate(self.character_options.items()):
            # Calculate column and row for labels and buttons
            column = index % 2
            label_row = 0 if index < 2 else 2
            button_row = 1 if index < 2 else 3

            # Create and configure the character label
            character_label = ttk.Label(self.character_frame)
            character_label.configure(justify="center", text=label_text)
            character_label.grid(column=column, row=label_row)

            # Create the character button
            character_button = ttk.Button(self.character_frame)

            # Load and configure the character image
            image_path = str(this_file_dir + character_instance.image)
            character_image = tk.PhotoImage(file=image_path)

            # store image and character buttons in a list to prevent garbage collected
            self.character_images.append(character_image)

            # Configure button position, image and command
            character_button.grid(column=column, row=button_row, sticky="nsew")
            character_button.configure(image=self.character_images[index])

            # disable button if character is dead
            if not character_instance.is_alive():
                character_button.configure(state="disabled")

            # partial function for button press event
            on_character_pressed_function = partial(
                self.on_character_pressed,
                character_instance
                )
            character_button.configure(command=on_character_pressed_function)

    def create_navigation_buttons(self):
        """Create navigation buttons."""

        # loop through all navigation button
        for index, label in enumerate(self.navigation_buttons_label):

            # create and configure the navigation buttons
            navigation_button = ttk.Button(self)
            navigation_button.configure(text=label)
            navigation_button.grid(column=index, row=4)
            navigation_button.configure(command=lambda l=label: self.on_navigation_pressed(l))

    def on_character_pressed(self, character: BaseCharacter):
        """Handle character pressed event.
        
        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        # change new active character
        self.master.combat_frame.game_manager.active_player = character

        # update the combat frame
        self.master.combat_frame.update_ui()
        self.master.show_frame(self.master.combat_frame)

    def on_navigation_pressed(self, label: str):
        """Handles navigation button pressed event.
        
        Parameters
        ----------
        label : str
            The label of the navigation button.
        """

        # handle cancel button pressed
        if label.lower() == "cancel":
            self.master.show_frame(self.master.combat_frame)
            return
