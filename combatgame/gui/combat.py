"Module for handling combat."
import os
from typing import TYPE_CHECKING, List
from functools import partial
from datetime import datetime

import tkinter as tk
from tkinter import ttk, font

from combatgame.game_logic.characters import BaseCharacter
from combatgame.game_logic.enemies import EnemyCharacter
from combatgame.game_logic.game_manager import GameManager

from combatgame.utils.utils import split_text

from combatgame.gui.switch_character import SwitchCharacterFrame
from combatgame.gui.character_frames import PlayerFrame, EnemyFrame

if TYPE_CHECKING:
    from main import GameApp

# get directory of this file
this_file_dir = os.path.dirname(os.path.abspath(__file__))

class CombatFrame(ttk.Frame):
    """The combat frame."""

    def __init__(self, master: "GameApp", player_characters: List[BaseCharacter], **kw):
        """
        Initialize the CombatFrame.

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

        # intialize variables
        self.battle_log_text = tk.StringVar()
        self.skill_one_text = tk.StringVar()
        self.skill_two_text = tk.StringVar()

        # initalize battle log variables
        self.battle_log_label = None
        self.battle_log_scrollbar = None
        self.battle_log_text_widget = None

        # initialize frames
        self.battle_log_frame = ttk.Labelframe(self)
        self.actions_frame = ttk.Labelframe(self)

        # initialize GameManager object
        self.game_manager = GameManager(player_characters)

        # if player turn to make a move
        self.player_thinking = False

        # get turn character
        self.turn_character = self.game_manager.determine_turn_order()

        # list to store action buttons
        self.action_buttons: List[tk.Button] = []

        # create ui
        self.create_ui()

        # update ui
        self.update_ui()

        # start combat game loop
        self.game_loop()

    def game_loop(self):
        """Function for the game loop."""

        winner = self.game_manager.is_game_ended()

        # handle game over
        if winner == "player":
            self.add_battle_log("You won!")
            self.handle_game_over()
            return

        elif winner == "enemy":
            self.add_battle_log("You lost.")
            self.handle_game_over()
            return

        # update character state
        self.check_characters_health()

        if not self.player_thinking:
            self.turn_character = self.game_manager.determine_turn_order()

        if self.turn_character.is_player():
            self.player_thinking = True

        else:
            # temporarily disable action buttons
            self.configure_action_buttons_state("disabled")

            # choose enemy action after 500ms
            self.after(1000, self.run_enemy_turn, self.turn_character)

            # enable actions buttons
            self.after(1000, self.configure_action_buttons_state, "enabled")

            # run game loop after 500ms
            self.after(1000, self.game_loop)

        # set turn label text
        self.turn_label_text.set(f"It's {self.turn_character.name}'s turn.")

    def handle_game_over(self):
        """Handles game over."""

        # disable action buttons
        self.configure_action_buttons_state("disabled")

        # change restart button text to play again
        self.restart_button.configure(text="Play again")

# initialization and configuration functions
    def create_ui(self):
        """Creates the UI for the combat frame."""

        self.player_label_frame = PlayerFrame(self, self.game_manager.active_player)

        # turn label text variable
        self.turn_label_text = tk.StringVar()

        # turn label
        self.turn_label = tk.Label(self, textvariable=self.turn_label_text)
        self.turn_label.grid(row=0, column=1)

        self.enemy_label_frame = EnemyFrame(self, self.game_manager.active_enemy)

        # create battle log frame
        self.create_battle_log_widget()

        # create action buttons
        self.create_action_buttons()

        # navigation frame
        self.nav_frame = tk.Frame(self)
        self.nav_frame.grid(column=3, row=0, sticky="n")

        # configure restart button
        self.restart_button = ttk.Button(self.nav_frame)
        self.restart_button.configure(text='Restart')
        self.restart_button.grid(column=0, row=0, sticky="ne")
        self.restart_button.configure(command=self.on_restart_pressed)

        # configure main menu button
        self.main_menu_button = ttk.Button(self.nav_frame)
        self.main_menu_button.configure(text='Main Menu')
        self.main_menu_button.grid(column=0, row=1, sticky="ne")
        self.main_menu_button.configure(command=self.on_main_menu_pressed)


        self.configure(height=450, width=800)
        self.pack()
        self.grid_anchor("center")

    def create_battle_log_widget(self):
        """Creates the UI for battle log."""

        # battle log frame
        self.battle_log_frame.configure(
            height=150,
            labelanchor="n",
            text='Battle Log',
            width=480
            )

        # create text widget
        self.battle_log_text_widget = tk.Text(
            self.battle_log_frame,
            wrap="none",
            height=140,
            width=470,
            font=font.Font(family="Courier", size=8)
        )
        self.battle_log_text_widget.pack(padx=10, pady=10)

        # create scrollbar
        self.battle_log_scrollbar = ttk.Scrollbar(
            self.battle_log_frame, command=self.battle_log_text_widget
            )
        self.battle_log_scrollbar.pack(side="right", fill="y")
        self.battle_log_text_widget.configure(yscrollcommand=self.battle_log_scrollbar.set)

        # configure battle log label
        self.battle_log_label = tk.Label(self.battle_log_frame, textvariable=self.battle_log_text)
        self.battle_log_label.pack(anchor="w")

        # configure battle log frame
        self.battle_log_frame.grid(
            column=1, columnspan=2, padx=0, row=1
            )
        self.battle_log_frame.propagate(0)
        self.battle_log_frame.rowconfigure(0)

    def create_action_buttons(self):
        """Creates the UI for action buttons."""

        # actions buttons frame
        self.actions_frame.configure(
            height=150,
            labelanchor="n",
            text='Actions',
            width=180)

        # action buttons text
        action_buttons_text = [
            "Attack",
            "Defend",
            self.game_manager.active_player.skills[0].name,
            self.game_manager.active_player.skills[1].name
            ]

        # text variables for skills
        skills_text = [self.skill_one_text, self.skill_two_text]

        # create each action button
        for index, label_text in enumerate(action_buttons_text):

            # get column and row index
            column = index % 2
            row = 0 if index < 2 else 1

            # configure action button
            action_button = ttk.Button(self.actions_frame)
            action_button.configure(text=label_text)
            action_button.grid(column=column, row=row)
            action_button.configure(
                command=lambda l=label_text: self.on_action_pressed(l)
                )

            # configure a dynamic text variable for skill buttons
            if index > 1:
                action_button.configure(
                    textvariable=skills_text[index-2],
                    command=lambda: self.on_action_pressed(
                        skills_text[index-2].get()
                        )
                    )

            # append action button to self.action_buttons
            self.action_buttons.append(action_button)

        # switch character button
        switch_character_button = ttk.Button(self.actions_frame)
        switch_character_button.configure(
            text='Switch Character', width=21
            )
        switch_character_button.grid(column=0, columnspan=2, row=2)
        switch_character_button.configure(
            command=partial(self.on_action_pressed, "Switch Character")
            )

        # append switch character button to self.action_buttons
        self.action_buttons.append(switch_character_button)

        # configure actions frame
        self.actions_frame.grid(column=0, row=1)
        self.actions_frame.grid_propagate(True)
        self.actions_frame.grid_anchor("center")
        self.actions_frame.rowconfigure("all", pad=10)
        self.actions_frame.columnconfigure("all", pad=10)

    def configure_action_buttons_state(self, state: str):
        """Configure the state of action buttons.
        
        Parameters
        ----------
        state : str
            The state of the buttons to configure.
        """

        for button in self.action_buttons:
            button.configure(state=state)

# gameplay functions
    def run_enemy_turn(self, enemy_character: EnemyCharacter):
        """Run the enemy turn.
        
        Parameters
        ----------
        enemy_character : EnemyCharacter
            The active enemy instance.
        """

        # update the idle character stats
        self.game_manager.update_idle_character_stats(self.game_manager.active_player)
        selected_action = enemy_character.select_action(
                self.game_manager.active_player
                )
        log = selected_action()
        self.add_battle_log(log)

        # update ui
        self.update_ui()

    def check_characters_health(self):
        """Check if any character is defeated and handles it."""

        player = self.game_manager.active_player
        enemy = self.game_manager.active_enemy

        # checks if any character died
        if not player.is_alive():
            # handle defeated active player
            self.game_manager.switch_player_character()
            self.add_battle_log(f"{player.name} has been defeated by {enemy.name}!")
            self.update_ui()

        if not enemy.is_alive():
            # handle defeated active enemy
            self.game_manager.switch_enemy_character()
            self.add_battle_log(f"{enemy.name} has been defeated by {player.name}!")
            self.update_ui()

    def update_ui(self):
        """Update the whole combat frame UI."""

        # store character frames and instances in a list
        character_frames = [self.player_label_frame, self.enemy_label_frame]
        character_instances = [self.game_manager.active_player, self.game_manager.active_enemy]

        # zip frames and instances and loop through
        for frame, character in zip(character_frames, character_instances):

            # update character stats
            frame.update_frame(character)

        # update skill buttons
        player_skills = self.game_manager.active_player.skills
        self.skill_one_text.set(player_skills[0].name)
        self.skill_two_text.set(player_skills[1].name)

    def add_battle_log(self, log: str):
        """Adds a battle log with time prefix.
        
        Parameters
        ----------
        battle_log : str
            The log to add.
        """

        # get current time
        current_time = datetime.now().strftime("%H:%M:%S - ")

        # enable text widget
        self.battle_log_text_widget.configure(state="normal")

        # add current time to log
        log = current_time + log

        # makes sure log fits in frame
        log = "\n".join(split_text(log, 65))

        # add log to battle log text widget
        self.battle_log_text_widget.insert("end", log + "\n")

        # scroll to the end
        self.battle_log_text_widget.see("end")

        # disable text widget
        self.battle_log_text_widget.configure(state="disabled")

# callback functions
    def on_action_pressed(self, action: str):
        """Handles action press.
        
        action : str
            The action pressed.
        """

        # block action if enemy is thinking
        if not self.player_thinking:
            return

        # handle switch character pressed
        if action.lower() == "switch character":

            # shows the switch character frame
            self.master.switch_character_frame = SwitchCharacterFrame(
                self.master, self.game_manager.player_characters
                )
            self.master.show_frame(self.master.switch_character_frame)

            # switch character and log it
            log = f"Character switched to {self.game_manager.active_player.name}!"

        # handle attack button pressed
        elif action.lower() == "attack":

            # use attack and get the log
            log = self.game_manager.player_attack()

        # handle defend button pressed
        elif action.lower() == "defend":

            # use defend and get the log
            log = self.game_manager.player_defend()

        # handle skill button pressed
        else:

            # names of player skills
            player_skills_names = [
                skill.name for skill in self.game_manager.active_player.skills
                ]

            # use skill and get the log
            log = self.game_manager.player_use_skill(player_skills_names.index(action))

        # update idle character stats
        self.game_manager.update_idle_character_stats(self.game_manager.active_enemy)

        # set player_thinking to False, except when not enough points for Skill
        if not log.startswith("Not enough"):
            self.player_thinking = False

        # update battle log
        self.add_battle_log(log)

        # update UI
        self.update_ui()

        # run game loop
        self.game_loop()

    def on_restart_pressed(self):
        """Handle restart button pressed."""

        self.master.show_frame(self.master.character_selection_frame)

        # reset characters
        self.master.character_selection_frame.reset_characters()

    def on_main_menu_pressed(self):
        """Handle main menu button pressed."""

        self.master.show_frame(self.master.main_frame)

        # reset characters
        self.master.character_selection_frame.reset_characters()
