"""Module for character frames in combat."""
import os

import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING

from combatgame.game_logic.characters import BaseCharacter
from combatgame.game_logic.enemies import EnemyCharacter

if TYPE_CHECKING:
    from combatgame.gui.combat import CombatFrame

# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

class CharacterFrame(ttk.Labelframe):
    """
    A base class for frames that display character information.
    """

    def __init__(self, master: "CombatFrame"):
        """
        Initialize the CharacterFrame.

        Parameters
        ----------
        master : CombatFrame
            The parent CombatFrame instance.
        """

        super().__init__(master)

        self.master = master

        # lists to store widgets to avoid garbage collected
        self.widgets = []
        self.progress_bars = []

        # initialize image
        self.image = None
        self.image_label = None

        self.create_character_dynamic_variables()

    def create_character_dynamic_variables(self):
        """Creates dynamic variables for widgets in CharacterFrame."""

        self.dynamic_hp = tk.IntVar()
        self.dynamic_max_hp = tk.IntVar()
        self.dynamic_hp_text = tk.StringVar()

        self.dynamic_dp = tk.IntVar()
        self.dynamic_max_dp = tk.IntVar()
        self.dynamic_dp_text = tk.StringVar()

        self.dynamic_ap = tk.StringVar()
        self.dynamic_sp = tk.StringVar()
        self.dynamic_luck = tk.StringVar()
        self.dynamic_mp = tk.StringVar()
        self.dynamic_active_effects = tk.StringVar()

    def update_frame(self, character: BaseCharacter):
        """Update UI of CharacterFrame.
        
        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        self.update_image(character)
        self.update_character_stats(character)
        self.update_progress_bar_max_value(character)

    def switch_characters(self, character: BaseCharacter):
        """Update UI to switch character.
        
        Parameters
        ----------
        character : BaseCharacter
            The new active character instance.
        """

        self.update_frame(character)

    def update_character_stats(self, character: BaseCharacter):
        """Update character statistics.

        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        # update character name
        name = ("You " if character.is_player() else "Enemy ") + f"({character.name})"
        self.configure(text=name)

        # update hp
        self.dynamic_hp.set(character.health_points)
        self.dynamic_max_hp.set(character.max_health_points)
        self.dynamic_hp_text.set(f"{character.health_points}/{character.max_health_points}")

        # update dp
        self.dynamic_dp.set(character.defense_points)
        self.dynamic_max_dp.set(character.max_defense_points)
        self.dynamic_dp_text.set(f"{character.defense_points}/{character.max_defense_points}")

        # update AP, SP, Luck
        self.dynamic_ap.set(f"AP: {character.attack_points} points")
        self.dynamic_sp.set(f"SP: {character.speed_points} points")
        self.dynamic_luck.set(f"Luck: {character.luck} points")

        if character.is_player():
            # update MP and active effects if character is player
            self.dynamic_mp.set(f"MP: {character.magic_points} points")
            active_effect_names = [effect.name for effect in character.active_effects]
            self.dynamic_active_effects.set(f"Active Effects: {active_effect_names}")

    def update_progress_bar_max_value(self, character: BaseCharacter):
        """Update the maximum value of progress bars.
        
        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        # define max values
        max_values = [character.max_health_points, character.max_defense_points]

        # configure each progress bar with ist max values
        for progress_bar, max_value in zip(self.progress_bars, max_values):
            progress_bar.configure(maximum=max_value)

    def create_image(self, character: BaseCharacter):
        """Create and configure the character image.
        
        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        # configure character image
        self.image_label = tk.Label(self)
        image_file_path = this_file_dir + character.image
        self.image = tk.PhotoImage(file=image_file_path)
        self.image_label.configure(
            height=128,
            image=self.image,
            width=128
            )
        self.image_label.grid(column=0, row=0)

    def update_image(self, character: BaseCharacter):
        """Update the character image.
        
        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        # update character image
        image_file_path = this_file_dir + character.image
        self.image = tk.PhotoImage(file=image_file_path)
        self.image_label.configure(image=self.image)

    def create_stats_progress_bar(
        self, text, int_variable: tk.Variable, text_variable: tk.Variable, value: int,
        max_value: int, row: int
        ):
        """
        Create and configure a progress bar for a specific character statistic.

        Parameters
        ----------
        text : str
            The label text for the statistic.
        int_variable : tk.Variable
            The Tkinter IntVar variable holding the current value of the statistic.
        text_variable : tk.Variable
            The Tkinter StringVar variable holding the text displaying the current value
            of the statistic along with the maximum value.
        value : int
            The current value of the statistic.
        max_value : int
            The maximum value of the statistic.
        row : int
            The grid row where the progress bar will be placed.
        """

        # create progress bar frame
        progress_bar_frame = tk.Frame(self)

        # configure stats label
        stat_label = ttk.Label(progress_bar_frame, text=text)
        stat_label.grid(column=0, row=row)

        # configure progrss bar
        progress_bar = ttk.Progressbar(progress_bar_frame)
        progress_bar.configure(
            maximum=max_value,
            variable=int_variable
            )
        progress_bar.grid(column=1, row=row, padx=5)

        # configure value label
        value_label_text = f"{value}/{max_value}"
        value_label = ttk.Label(
            progress_bar_frame, text=value_label_text, textvariable=text_variable
            )
        value_label.grid(column=2, row=row)

        # configure progress_bar_frame
        progress_bar_frame.grid(row=row, column=0, sticky="w")

        # add to lists to avoid garbage collected
        self.widgets.append(progress_bar_frame)
        self.progress_bars.append(progress_bar)

    def create_stats_widgets(self, character: BaseCharacter):
        """Create and configure various character statistics widgets.
        
        Parameters
        ----------
        character : BaseCharacter
            The character instance.
        """

        # create image
        self.create_image(character)

        # hp and dp parameters for self.create_stats_progress_bar
        progress_bar_parameters = [
            (
                "HP:", self.dynamic_hp, self.dynamic_hp_text,
                character.health_points, character.max_health_points
                ),

            (
                "DP:", self.dynamic_dp, self.dynamic_dp_text,
                character.defense_points, character.max_defense_points
                )
        ]

        # create hp and dp progress bars
        for index, parameters in enumerate(progress_bar_parameters, start=2):
            self.create_stats_progress_bar(*parameters, index)

        # list of stats label text
        stats_labels_text = [
            (f"AP: {character.attack_points} points", self.dynamic_ap),
            (f"SP: {character.speed_points} points", self.dynamic_sp),
            (f"Luck: {character.luck} points", self.dynamic_luck)
        ]

        # add magic point stat if character is a player
        if character.is_player():
            active_effect_names = [effect.name for effect in character.active_effects]
            stats_labels_text.extend(
                    [
                    (f"MP: {character.magic_points} points", self.dynamic_mp),
                    (f"Active Effects: {active_effect_names}", self.dynamic_active_effects)
                    ]
                )

        # create labels for displaying character statistics
        for row, items in enumerate(stats_labels_text, start=4):
            # extract the stat_text and text_variable from the items tuple
            stat_text, text_variable = items

            # configure stat label
            stat_label = ttk.Label(self)
            stat_label.configure(text=stat_text, textvariable=text_variable)
            stat_label.grid(column=0, row=row, sticky="w")

            # add to widget lists to avoid garbage collected
            self.widgets.append(stat_label)


class PlayerFrame(CharacterFrame):
    """
    A frame that displays player character information.
    """
    def __init__(self, master: "CombatFrame", character: BaseCharacter):
        """
        Initialize the PlayerFrame.

        Parameters
        ----------
        master : CombatFrame
            The parent CombatFrame instance.
        character : BaseCharacter
            The player character instance.
        """

        super().__init__(master)

        self.master = master

        self.configure(
            height=200, labelanchor="n", text=f'You ({character.name})', width=200
            )

        self.create_image(character)
        self.create_stats_widgets(character)
        self.update_frame(character)

        self.grid(column=0, row=0)


class EnemyFrame(CharacterFrame):
    """
    A frame that displays enemy character information.
    """

    def __init__(self, master: "CombatFrame", character: EnemyCharacter):
        """
        Initialize the EnemyFrame.

        Parameters
        ----------
        master : CombatFrame
            The parent CombatFrame instance.
        character : EnemyCharacter
            The enemy character instance.
        """

        super().__init__(master)
        self.master = master

        self.configure(
            height=200, labelanchor="n", text=f'Enemy ({character.name})', width=200
            )

        self.create_image(character)
        self.create_stats_widgets(character)
        self.update_frame(character)

        self.grid(column=2, row=0)
