"""Module for settings frame."""
import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from combatgame.gui.main_screen import GameApp

class SettingsFrame(ttk.Frame):
    """The settings frame."""

    def __init__(self, master: "GameApp", **kw):
        """
        A frame that displays the settings screen for the game.

        Parameters
        ----------
        master : GameApp
            The GameApp instance.
        **kw
            Additional keyword arguments for configuring the frame.
        """

        super().__init__(master, **kw)

        self.master = master

        # create the settings label frame
        self.settings_label_frame = ttk.Labelframe(self, text='Settings')
        self.settings_label_frame.configure(height=400, labelanchor="n", width=400)

        # sound option
        self.sound_button = ttk.Checkbutton(self.settings_label_frame, text='Sound')
        self.sound_button.grid(column=0, columnspan=2, row=0)

        # difficulty scale
        self.difficulty_scale = tk.Scale(self.settings_label_frame, from_=1, to=3,
                                         label='Difficulty Level', length=150, orient="horizontal",
                                         showvalue=True, takefocus=False)
        self.difficulty_scale.grid(column=0, columnspan=2, row=2)

        # language option menu
        langauge_options = ['English', 'Chinese', 'Malay', 'Hindu']
        self.option_variable = tk.StringVar(value="Choose an Option")
        self.langauge_options = tk.OptionMenu(
            self.settings_label_frame, self.option_variable, *langauge_options
            )
        self.langauge_options.grid(column=1, row=3)

        # language label
        self.language_label = ttk.Label(self.settings_label_frame, text='Language')
        self.language_label.grid(column=0, row=3)

        # button frame
        self.button_frame = ttk.Frame(self.settings_label_frame, height=200, width=200)

        # save button
        self.save_button = ttk.Button(self.button_frame, text='Save')
        self.save_button.grid(column=0, row=0)

        # reset button
        self.reset_button = ttk.Button(self.button_frame, text='Reset')
        self.reset_button.grid(column=0, row=1)

        # back button
        self.back_button = ttk.Button(
            self.button_frame, text='Back', command=self.on_back_pressed
            )
        self.back_button.grid(column=0, row=2)

        self.button_frame.grid(column=0, columnspan=2, row=8)
        self.button_frame.rowconfigure("all", pad=5)

        # place settings label frame
        self.settings_label_frame.grid(column=0, row=0)
        self.settings_label_frame.grid_propagate(0)
        self.settings_label_frame.grid_anchor("n")
        self.settings_label_frame.rowconfigure("all", pad=50)
        self.settings_label_frame.columnconfigure("all", pad=15)

    def on_back_pressed(self):
        """Handle back button pressed."""

        self.master.show_frame(self.master.main_frame)
