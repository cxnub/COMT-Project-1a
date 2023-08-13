"""Module for help screen frame."""
import os
from typing import TYPE_CHECKING

import tkinter as tk
from tkinter import ttk

from combatgame.game_logic.characters import Tank, MirrorMage, Healer, Assassin, BaseCharacter
from combatgame.game_logic.skills import BaseSkill

from combatgame.utils.utils import split_text

if TYPE_CHECKING:
    from main import GameApp

# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

class HelpFrame(ttk.Frame):
    """The help screen frame."""

    def __init__(self, master="GameApp", **kw):
        """
        Initialize the HelpFrame.

        Parameters
        ----------
        master : GameApp
            The GameApp instance.
        **kw
            Additional keyword arguments for configuring the frame.
        """

        super().__init__(master, **kw)

        # define characters
        self.characters = [
            Tank("Whiskerwall"),
            MirrorMage("Purrception"),
            Healer("Meowdicine"),
            Assassin("Shadowpaw")
        ]

        # define skills
        self.skills = []

        # add every character skills into self.skills
        for character in self.characters:
            self.skills.extend(character.skills)

        # character image
        self.character_image = None

        # create character frame
        self.create_character_frame()
        self.character_page_number = 1

        # create skill frame
        self.create_skill_frame()
        self.skill_page_number = 1

        # update character
        self.update_character(self.characters[0])

        # update skill
        self.update_skill(self.skills[0])

        # configure frame
        self.grid_columnconfigure("all", pad=10)

    def create_character_frame(self):
        """Creates the character frame and its widgets."""

        # characters frame
        self.characters_frame = ttk.Labelframe(self, text="Characters")
        self.characters_frame.configure(height=350, labelanchor="n", width=300)

        # previous character button
        self.previous_character_button = ttk.Button(
            self.characters_frame, text="Previous Page", command=self.show_previous_character
            )
        self.previous_character_button.grid(column=0, padx=5, row=3, sticky="w")

        # next character button
        self.next_character_button = ttk.Button(
            self.characters_frame, text="Next Page", command=self.show_next_character
            )
        self.next_character_button.grid(column=2, padx=5, row=3, sticky="e")

        # character page number label
        self.character_page_number_label = ttk.Label(self.characters_frame, text="1/1")
        self.character_page_number_variable = tk.StringVar(value="1/1")
        self.character_page_number_label.configure(textvariable=self.character_page_number_variable)
        self.character_page_number_label.grid(column=1, row=3)

        # character name labels
        self.character_name_label = ttk.Label(self.characters_frame)
        self.character_name = tk.StringVar()
        self.character_name_label.configure(textvariable=self.character_name)
        self.character_name_label.grid(column=0, columnspan=3, row=0)

        # character image labels
        self.character_image = None
        self.character_image_label = ttk.Label(self.characters_frame)
        self.character_image_label.grid(column=0, columnspan=3, row=1)

        # character stats label
        self.character_stats_label = ttk.Label(self.characters_frame)
        self.character_stats = tk.StringVar()
        self.character_stats_label.configure(textvariable=self.character_stats)
        self.character_stats_label.grid(column=0, columnspan=3, row=2)

        # place characters frame
        self.characters_frame.grid(column=0, row=1)
        self.characters_frame.rowconfigure("all", pad=5)
        self.characters_frame.columnconfigure("all", pad=20)

    def create_skill_frame(self):
        """Creates the skill frame and its widgets."""

        # skills label frame
        self.skills_label_frame = ttk.Labelframe(self, text="Skills")
        self.skills_label_frame.configure(labelanchor="n")

        # skills frame
        self.skills_frame = tk.Frame(self.skills_label_frame)
        self.skills_frame.configure(width=350, height=180)
        self.skills_frame.grid(row=0, column=0, columnspan=3)
        self.skills_frame.grid_propagate(0)
        self.skills_frame.columnconfigure(0, weight=1)
        self.skills_frame.rowconfigure(0, weight=1)

        # previous skill button
        self.previous_skill_button = ttk.Button(
            self.skills_label_frame, text="Previous Page", command=self.show_previous_skill
            )
        self.previous_skill_button.grid(column=0, padx=5, row=2, sticky="w")

        # next skill button
        self.next_skill_button = ttk.Button(
            self.skills_label_frame, text="Next Page", command=self.show_next_skill
            )
        self.next_skill_button.grid(column=2, padx=5, row=2, sticky="e")

        # skill page number label
        self.skill_page_number_label = ttk.Label(self.skills_label_frame)
        self.skill_page_number_variable = tk.StringVar(value="1/1")
        self.skill_page_number_label.configure(textvariable=self.skill_page_number_variable)
        self.skill_page_number_label.grid(column=1, row=2)

        # skill name labels
        self.skill_name_label = ttk.Label(self.skills_frame, justify="center", text="Skill Name")
        self.skill_name = tk.StringVar(value="Skill Name")
        self.skill_name_label.configure(textvariable=self.skill_name)
        self.skill_name_label.grid(column=0, row=0)
        self.skill_info_label = ttk.Label(
            self.skills_frame, justify="left", text="Description:\nBelongs to:\nMP cost:\nSP cost:"
            )

        # skill info label
        self.skill_info = tk.StringVar(value="Description:\nBelongs to:\nMP cost:\nSP cost:")
        self.skill_info_label.configure(textvariable=self.skill_info)
        self.skill_info_label.grid(column=0, row=1)

        # configure skills label frame
        self.skills_label_frame.grid(column=1, row=1)
        self.skills_label_frame.rowconfigure("all", pad=5)
        self.skills_label_frame.columnconfigure("all", pad=20)

        # Back Button
        self.back_button = ttk.Button(self, text="Back", command=self.on_back_pressed)
        self.back_button.grid(column=0, columnspan=2, padx=5, pady=5, row=0, sticky="ne")

    def update_character_image(self, character: BaseCharacter):
        """Update the character image.
        
        Parameters
        ----------
        character : BaseCharacter
            The player character instance.
        """

        image_file_path = this_file_dir + character.image

        # configure the new image
        self.character_image = tk.PhotoImage(file=image_file_path)
        self.character_image_label.configure(image=self.character_image)

    def update_character(self, character: BaseCharacter):
        """Update character information.

        Parameters
        ----------
        character : BaseCharacter
            The player character instance.
        """

        self.update_character_image(character)

        # update character name
        self.character_name.set(character.name)

        # get character's page number and update the page number variable
        character_page_number = self.characters.index(character) + 1
        self.character_page_number_variable.set(f"{character_page_number}/{len(self.characters)} characters")

        # set new character info
        self.character_stats.set(
            f"""
Job Class: {character.job_class}
Skills: {[skill.name for skill in character.skills]}

 Statistics
------------
HP: {character.max_health_points}
DP: {character.max_defense_points}
AP: {character.attack_points}
SP: {character.speed_points}
MP: {character.magic_points}
Luck: {character.luck}
            """
        )

    def update_skill(self, skill: BaseSkill):
        """Update skill information.
        
        Parameters
        ----------
        skill : BaseSkill
            The skill instance.
        """

        # get skill's page number and update the page number variable
        skill_page_number = self.skills.index(skill) + 1
        self.skill_page_number_variable.set(f"{skill_page_number}/{len(self.skills)} skills")

        # format skill description to fit in frame
        skill_description = '\n'.join(split_text(skill.description, 50))

        # update skill name
        self.skill_name.set(skill.name)

        # set new skill info
        self.skill_info.set(
            f"""
Description: {skill_description}

Belongs to: {skill.belongs_to}
MP cost: {skill.magic_points_cost} points
SP cost: {skill.speed_points_cost} points
            """
        )

    def show_previous_character(self):
        """Handle previous button press in character frame."""

        # assign new page number
        self.character_page_number -= 1

        # change page number to max if less than 1
        if self.character_page_number < 1:
            self.character_page_number = len(self.characters)

        character = self.characters[self.character_page_number - 1]
        self.update_character(character)

    def show_next_character(self):
        """Handle next button press in character frame."""

        # assign new page number
        self.character_page_number += 1

        # reset page number to 1 if more than max
        if self.character_page_number > len(self.characters):
            self.character_page_number = 1

        character = self.characters[self.character_page_number - 1]
        self.update_character(character)

    def show_previous_skill(self):
        """Handle previous button press in skill frame."""

        # assign new page number
        self.skill_page_number -= 1

        # change page number to max if less than 1
        if self.skill_page_number < 1:
            self.skill_page_number = len(self.skills)

        skill = self.skills[self.skill_page_number - 1]
        self.update_skill(skill)

    def show_next_skill(self):
        """Handle next button press in skill frame."""  

        # assign new page number
        self.skill_page_number += 1

        # reset page number to 1 if more than max
        if self.skill_page_number > len(self.skills):
            self.skill_page_number = 1

        skill = self.skills[self.skill_page_number - 1]
        self.update_skill(skill)

    def on_back_pressed(self):
        """Handle back button press."""

        self.master.show_frame(self.master.main_frame)
