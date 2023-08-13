"""Module for main screen frame."""
from tkinter import ttk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameApp

class MainFrame(ttk.Frame):
    """The main screen frame."""

    def __init__(self, master: "GameApp"):
        """Initializes MainFrame.
        
        Parameters
        ----------
        master : GameApp
            The GameApp instance.
        """

        super().__init__(master)

        self.master = master

        self.buttons_label = ["Start", "Help", "Settings", "Quit"]

        self.create_widgets()

    def create_widgets(self):
        """Create widgets in main screen frame."""

        # title label
        self.title_label = ttk.Label(self)
        self.title_label.configure(
            compound="center",
            font="{Bangers} 20 {}",
            justify="center",
            text='CATastrophe Chronicles:\nJust the Combat Only')
        self.title_label.grid(column=0, row=0)

        # empty labels to make space between title and buttons
        ttk.Label(self).grid(column=0, row=2)
        ttk.Label(self).grid(column=0, row=1)

        # create buttons
        self.create_buttons()

    def create_buttons(self):
        """Create buttons in main screen frame."""

        # create every button in self.buttons_label

        for row, label in enumerate(self.buttons_label, start=3):
            # create and configure button
            button = ttk.Button(self)
            button.configure(text=label, width=12)
            button.grid(column=0, pady=5, row=row)
            button.configure(command=lambda l=label: self.on_button_pressed(l))

    def on_button_pressed(self, label: str):
        """Handle button pressed.
        
        Parameters
        ----------
        label : str
            The label of the button pressed.
        """

        # handle start button pressed
        if label == "Start":
            self.master.show_frame(self.master.character_selection_frame)

        # handle settings button pressed
        elif label == "Settings":
            self.master.show_frame(self.master.settings_frame)

        # handle help button pressed
        elif label == "Help":
            self.master.show_frame(self.master.help_frame)

        # handle quit button pressed
        else:
            exit()
