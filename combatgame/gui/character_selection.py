"""Module for character selection frame before combat."""
import os
from typing import TYPE_CHECKING

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from combatgame.game_logic.characters import Tank, MirrorMage, Healer, Assassin
from combatgame.gui.combat import CombatFrame

if TYPE_CHECKING:
    from main import GameApp

# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

class CharacterSelectionFrame(ttk.Frame):
    """A frame for character selection."""

    def __init__(self, master: "GameApp", **kw):
        """
        Initialize the CharacterSelectionFrame.

        Parameters
        ----------
        master : GameApp
            The GameApp instance.
        **kw
            Additional keyword arguments for configuring the frame.
        """

        super().__init__(master, **kw)

        self.master = master

        self.characters = {
            "Whiskerwall\n(tank)": Tank("Whiskerwall"),
            "Purrception\n(mirror mage)": MirrorMage("Purrception"),
            "Meowdicine\n(healer)": Healer("Meowdicine"),
            "Shadowpaw\n(assassin)": Assassin("Shadowpaw")
        }

        # list to store character images
        self.character_images = []

        # list to store boolean variables for character selection buttons
        self.buttons_checked = []

        self.create_character_frame()
        self.create_characters_button()

        self.navigation_buttons_label = ["Back", "Next"]

        self.create_navigation_buttons()

    def reset_characters(self):
        """Resets all player character's stats."""

        for character in self.characters.values():
            character.restore_stats()

    def create_character_frame(self):
        "Creates the character selection frame."

        self.character_frame = ttk.Labelframe(self)
        self.character_frame.configure(
            height=350,
            labelanchor="n",
            text='Choose your characters',
            width=400)

        self.character_frame.grid(
            column=0, columnspan=2, padx=5, pady=5, row=3)
        self.character_frame.grid_propagate(0)
        self.character_frame.grid_anchor("center")
        self.character_frame.rowconfigure("all", pad=25)
        self.character_frame.columnconfigure("all", pad=25)

    def create_characters_button(self):
        """Creates the characters buttons."""

        # loop through self.characters
        for index, (label_text, character_instance) in enumerate(self.characters.items()):
            # Calculate column and row for labels and buttons
            column = index % 2
            label_row = 0 if index < 2 else 2
            button_row = 1 if index < 2 else 3

            # variable to store button state
            button_checked = tk.BooleanVar()
            button_checked.set(False)
            self.buttons_checked.append(button_checked)

            # Create and configure the character label
            character_label = ttk.Label(self.character_frame)
            character_label.configure(justify="center", text=label_text)
            character_label.grid(column=column, row=label_row)

            # Create the character button
            character_button = ttk.Checkbutton(self.character_frame, variable=button_checked)

            # Load and configure the character image
            image_path = str(this_file_dir + character_instance.image)
            character_image = tk.PhotoImage(file=image_path)

            # store image and character buttons in a list to prevent garbage collected
            self.character_images.append(character_image)

            # Configure button position, image and command
            character_button.grid(column=column, row=button_row, sticky="nsew", padx=5, pady=5)
            character_button.configure(image=self.character_images[index])

    def create_navigation_buttons(self):
        """Create the navigation buttons."""

        for index, label in enumerate(self.navigation_buttons_label):
            navigation_button = ttk.Button(self)
            navigation_button.configure(text=label)
            navigation_button.grid(column=index, row=4)
            navigation_button.configure(command=lambda l=label: self.on_navigation_pressed(l))

    def on_navigation_pressed(self, label: str):
        """Handles navigation buttons.
        
        Parameters
        ----------
        label : str
            The label text of the navigation button pressed.
        """

        # handle back button press
        if label.lower() == "back":
            self.master.show_frame(self.master.main_frame)
            return

        # handle next button press
        num_of_characters_selected = sum(var.get() for var in self.buttons_checked)

        # handle no character selected
        if num_of_characters_selected < 1:
            print("Please select at least one character.")
            messagebox.showerror("error", "Please select at least one character.")
            return

        # get the index of selected characters
        selected_player_characters_index = [
            index for index, var in enumerate(self.buttons_checked) if var.get()
            ]

        # get the selected characters
        selected_player_characters = [
             list(self.characters.values())[index] for index in selected_player_characters_index
        ]

        self.master.combat_frame = CombatFrame(self.master, selected_player_characters)
        self.master.show_frame(self.master.combat_frame)
