"""Module for managing the whole gameplay, turns, and win/lose conditions of the game."""
from typing import List, Union
import random
import time
from datetime import datetime
from functools import partial
from collections import deque

from combatgame.characters import BaseCharacter, Tank, MirrorMage, Healer, Assassin
from combatgame.enemies import EnemyCharacter
from combatgame.ui import Ui


class GameManager:
    """Game Manager class responsible for managing the gameplay and interactions between
    player characters and enemies during a combat.

    Parameters
    ----------
    player_characters : List[Union[Tank, MirrorMage, Healer, Assassin]]
        A list of player characters participating in the game.
        Each player character can be an instance of Tank, MirrorMage, Healer, or Assassin class.

    enemies : List[EnemyCharacter]
        A list of enemy characters participating in the game. Each enemy character is an instance
        of the EnemyCharacter class.

    Attributes
    ----------
    player_characters List[Union[Tank, MirrorMage, Healer, Assassin]]
        A list of player characters participating in the game.

    enemies : List[EnemyCharacter]
        A list of enemy characters participating in the game.

    active_player_character : BaseCharacter
        The active player character that the player selected.

    active_enemy_character : BaseCharacter
        The active enemy character.
    """

    def __init__(
        self,
        player_characters: List[Union[Tank, MirrorMage, Healer, Assassin]],
        enemies: List[EnemyCharacter],
    ):
        """Initializes a GameManager instance.

    Parameters
    ----------
    player_characters : List[Union[Tank, MirrorMage, Healer, Assassin]]
        A list of player characters participating in the game.
        Each player character can be an instance of Tank, MirrorMage, Healer, or Assassin class.

    enemies : List[EnemyCharacter]
        A list of enemy characters participating in the game. Each enemy character is an instance
        of the EnemyCharacter class.
        """

        self.player_characters = player_characters
        self.enemies = enemies

        # assign first character in player_characters as the active character
        self.active_player_character = player_characters[0]

        # assign first character in enemies as the active character
        self.active_enemy_character = enemies[0]

        # assign turn character
        self.turn_character = self.determine_turn_order()

        # battle log (limits to 5 items only)
        self.battle_log = deque(maxlen=5)

    def start_combat(self):
        """Start the combat.
        
        Returns
        -------
        player_won : bool
            True if player_won, False otherwise.
        """

        while not self.is_game_over():
            self.run_battle_logic()

        Ui.clear_terminal()

        Ui.display_combat_screen(
            self.active_player_character, self.active_enemy_character, self.battle_log
            )
        input("You won!\nPress enter to continue...")
        return self.player_won()

    def run_battle_logic(self, flag: bool=False):
        """The logic implementation for the combat battle.
        
        Parameters
        ----------
        flag : bool
            If function is running within itself.
        """
        # get active characters
        player = self.active_player_character
        enemy = self.active_enemy_character

        # turn character doesnt change if flag is True
        if not flag:
            # set the turn order character
            self.turn_character = self.determine_turn_order()

        Ui.clear_terminal()
        Ui.display_combat_screen(player, enemy, self.battle_log)

        if player is self.turn_character:
            # lets player know its their turn
            print("\nIt's your turn!")

            # define dictionary of available player options for Menu
            available_player_options = {
                "Attack": partial(player.basic_attack, enemy),
                "Heal": player.heal
            }

            # add skills options to available_player_options dict
            for index, skill in enumerate(player.skills):
                available_player_options[f"{skill.name} (skill)"] = partial(
                    player.use_skill,
                    index,
                    enemy
                    )

            # add the option to switch active characters
            available_player_options["Switch characters"] = self.switch_active_player_characters

            # create the menu and let user select their action
            select_action_menu = Ui.Menu("Choose an Action", available_player_options)
            selected_action = select_action_menu.select_option(
                invalid_handler=self.invalid_option_handler
                )
            # get current time
            current_time = datetime.now().strftime("%H:%M:%S - ")

            # success and combat log
            log = selected_action()

            # tuple is returned only when there's an error using skill
            if isinstance(log, tuple):
                self.battle_log.append(log[1])
                return self.run_battle_logic(flag=True)

            self.battle_log.append(current_time + log)

            if selected_action != available_player_options["Switch characters"]:
                # update idle character's stat (enemy)
                self.update_idle_character_stats(enemy)

        else:
            # lets player know its enemy's turn
            print(f"\nIt's {enemy.name} turn.")
            enemy_action = enemy.select_action(player)

            # get current time
            current_time = datetime.now().strftime("%H:%M:%S - ")
            self.battle_log.append(current_time + enemy_action())

            time.sleep(2)

            # update idle character's stat (player)
            self.update_idle_character_stats(player)

        current_time = datetime.now().strftime("%H:%M:%S - ")

        if not player.is_alive():
            player.health_points = 0
            self.battle_log.append(
                current_time + f"{player.name} has been defeated by {enemy.name}!"
                )

            if not self.is_game_over():
                # set new active player character
                self.active_player_character = next(
                    (character for character in self.player_characters if character.is_alive()), None
                    )

        elif not enemy.is_alive():
            enemy.health_points = 0
            self.battle_log.append(
                current_time + f"{enemy.name} has been defeated by {player.name}!"
                )

            if not self.is_game_over():
                # set new active enemy character
                self.active_enemy_character = next(
                    (character for character in self.enemies if character.is_alive()), None
                    )

    @staticmethod
    def update_idle_character_stats(idle_character: BaseCharacter):
        """Update the stats for characters when its not their turn.
        
        Parameters
        ----------
        idle_character : BaseCharacter
            The character that is idle.
        """

        idle_character.speed_points += 1

        idle_character.defense_points = max(idle_character.defense_points, 0)

        if not isinstance(idle_character, EnemyCharacter):
            idle_character.magic_points += 1

    def invalid_option_handler(self):
        """Handler for invalid option input for menus.
        """

        print("Invalid choice. Please choose again.")
        time.sleep(1)
        Ui.clear_terminal()
        Ui.display_combat_screen(
            self.active_player_character, self.active_enemy_character, self.battle_log
            )

    def switch_active_player_characters(self):
        """switch active player characters.
        
        Returns
        -------
        log : str
            The log to display.
        """

        Ui.clear_terminal()

        # get available characters
        available_characters_dict = {}
        for character in self.player_characters:
            # the display string in the menu
            display_str = f"{character.name} {character.job_class}"

            if self.active_player_character is character:
                # shows player the current active character
                display_str += " (current)"

            if not character.is_alive():
                # shows player the current active character
                display_str += " (defeated)"

            available_characters_dict[display_str] = character

        # create menu for character switch options
        character_switch_menu = Ui.Menu("Switch Active Characters", available_characters_dict)

        # old active character
        old_active_character = self.active_player_character

        # get chosen character
        chosen_character = character_switch_menu.select_option(
            invalid_handler=partial(
                GameManager.invalid_option_handler,
                self.active_player_character,
                self.active_enemy_character
                )
            )

        if chosen_character.is_alive():
            self.active_player_character = chosen_character
            log = f"Active character switched from {old_active_character.name} to " \
                f"{self.active_player_character.name}."

        else:
            log = f"{chosen_character.name} is defeated and can't be chosen!"

        return log

    def determine_turn_order(self) -> BaseCharacter:
        """Determine who's turn it is based on speed points.

        Returns
        -------
        BaseCharacter : The BaseCharacter with higher speed points.

        Notes
        -----
        The function returns a random active character if both active
        characters have same speed points
        """

        # stores active player and enemy characters in a list
        active_characters = [self.active_enemy_character,
                             self.active_player_character]

        # sorts active_characters by speed points in descending order
        # if both active characters have the same speed_points,
        # randomize the sort order
        sorted_entities = sorted(
            active_characters,
            key=lambda entity: (entity.speed_points, random.random()),
            reverse=True,
        )

        # returns the character for the turn
        return sorted_entities[0]

    def is_game_over(self) -> bool:
        """Check the win/lose conditions of the game.

        Returns
        -------
        game_ended : bool
            True if the game has been won or lost, False otherwise.
        player_won : bool
            True if the player won, False otherwise.

        Notes
        -----
        If game_end is False, player_won would be False too.
        """

        # checks if all player or enemy characters are defeated
        if not any(character.is_alive() for character in self.player_characters) \
            or not any(character.is_alive() for character in self.enemies):
            return True

        else:
            return False

    def player_won(self):
        """Returns True if game ended and player won, False otherwise.
        
        Returns
        -------
        bool : Returns True if game ended and player won, False otherwise.
        """

        if not self.is_game_over():
            print("Game not over yet.")
            return False

        # checks if all enemies are dead and at least one character is alive
        if any(character.is_alive() for character in self.player_characters) \
            and not any(character.is_alive() for character in self.enemies):
            return True

        else:
            return False


    def end_combat(self):
        """End the game."""
        return
