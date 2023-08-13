"""CATastrophe Chronicles: The Wildcat Cafe

This is the main script for CATastrophe Chronicles: Just the Combat Only.
It is the entry point for running the game.

Author: Koh Cheng Xi
Date: 13/8/2023

Usage:
    python main.py
"""
import tkinter as tk
from combatgame.gui import character_selection, main_screen, settings, help_screen

class GameApp(tk.Tk):
    """
    The main application class for the game.

    This class initializes and manages different frames of the game's user interface.

    Attributes
    ----------
    current_frame : tk.Frame or None
        The currently displayed frame.
    main_frame : main_screen.MainFrame
        The main screen frame of the game.
    settings_frame : settings.SettingsFrame
        The settings frame of the game.
    help_frame : help_screen.HelpFrame
        The help screen frame of the game.
    character_selection_frame : character_selection.CharacterSelectionFrame
        The character selection frame of the game.
    switch_character_frame : None or SwitchCharacterFrame
        The switch character frame of the game (initialized when needed).
    combat_frame : None or CombatFrame
        The combat frame of the game (initialized when needed).
    """

    def __init__(self):
        """
        Initialize the GameApp class.

        This method sets up the main application window, initializes frame instances,
        and displays the main frame initially.
        """

        super().__init__()

        # Build ui
        self.configure(height=450, width=800)
        self.minsize(800, 450)

        # set current frame
        self.current_frame = None

        # Create instances of frames
        self.main_frame = main_screen.MainFrame(self)
        self.settings_frame = settings.SettingsFrame(self)
        self.help_frame = help_screen.HelpFrame(self)
        self.character_selection_frame = character_selection.CharacterSelectionFrame(self)
        self.switch_character_frame = None
        self.combat_frame = None

        # Show the main frame initially
        self.show_frame(self.main_frame)

    def show_frame(self, frame: tk.Frame):
        """
        Switch to the specified frame.

        This method hides the current frame (if any), displays the specified frame,
        and configures its layout within the main application window.

        Parameters
        ----------
        frame : tk.Frame
            The frame to be displayed.
        """

        # Remove current frame
        if self.current_frame:
            self.current_frame.forget()

        # Set new current frame
        self.current_frame = frame

        # Configure the new frame
        frame.configure(height=450, width=800)
        frame.pack(anchor="center", expand=True)
        frame.grid_propagate(0)
        frame.grid_anchor("center")

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
