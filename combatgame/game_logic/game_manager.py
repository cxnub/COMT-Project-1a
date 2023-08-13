"""Module for GameManger class."""
import random

from typing import List

from combatgame.game_logic.characters import BaseCharacter
from combatgame.game_logic.enemies import EnemyCharacter
from combatgame.game_logic.skills import BaseSkill

class GameManager:
    """GameManager class for handling game logic."""

    def __init__(self, player_characters: List[BaseCharacter]):
        """
        Initialize the GameManager.

        Parameters
        ----------
        player_characters : list of BaseCharacter
            A list containing player characters participating in the game.
        """

        self.player_characters = player_characters

        # define enemies
        self.enemy_characters = [
            EnemyCharacter("Doomshroud"),
            EnemyCharacter("Viperstrike"),
            EnemyCharacter("Mistwalker")
        ]

        # shuffle enemy characters
        random.shuffle(self.enemy_characters)

        # set initial characters
        self.active_player: BaseCharacter = self.player_characters[0]
        self.active_enemy: EnemyCharacter = self.enemy_characters[0]

    def is_game_ended(self):
        """Checks if game has ended. Returns winner if so, None otherwise. 
        
        Returns
        -------
        winner : str
            "player" if player won, "enemy" if enemy won, None otherwise.
        """

        # checks if all players are dead
        if all(not character.is_alive() for character in self.player_characters):
            return "enemy"

        # checks if all enemies are dead
        if all(not character.is_alive() for character in self.enemy_characters):
            return "player"

        return None

    def select_enemy_action(self):
        """Makes turn for enemy."""

        enemy_action = self.active_enemy.select_action(self.active_player)
        return enemy_action()

    def determine_turn_order(self):
        """Get turn order character based on characters speed points.
        
        Returns
        -------
        turn_character : BaseCharacter
            The turn character instance.
        """

        if self.active_player.speed_points > self.active_enemy.speed_points:
            return self.active_player

        if self.active_player.speed_points < self.active_enemy.speed_points:
            return self.active_enemy

        # returns random active character if both active characters have same speed points
        return random.choice([self.active_enemy, self.active_player])

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

    def switch_player_character(self, character: BaseCharacter=None):
        """
        Switch the active player character to the next alive player character.

        If a character is provided, it becomes the new active player character. If no
        character is given, the method assigns the next alive player character as the
        active player.

        Parameters
        ----------
        character : BaseCharacter, optional
            The character to set as the active player character. If not provided,
            the next alive player character is selected.
        """

        # assign the next alive player character if character not given
        if not character:
            self.active_player = next(
            character for character in self.player_characters if character.is_alive()
        )
            return

        # assign active_player to character
        if character.health_points > 0:
            self.active_player = character

    def switch_enemy_character(self):
        """
        Switch the active enemy character to the next alive enemy character.
        """

        # assign the next alive enemy character
        self.active_enemy = next(
            character for character in self.enemy_characters if character.is_alive()
        )

    def player_attack(self):
        """
        Execute a basic attack action for the active player character.

        Returns
        -------
        log : str
            The log of the player's basic attack action.
        """

        return self.active_player.basic_attack(self.active_enemy)

    def player_defend(self):
        """
        Execute a defend action for the active player character.

        Returns
        -------
        log : str
            The log of the player's defend action.
        """

        return self.active_player.defend()

    def player_use_skill(self, skill_index: int):
        """Use a skill.
        
        Parameters
        ---------
        skill_index : int
            The index of the skill.
        """

        player = self.active_player
        skill: BaseSkill = player.skills[skill_index]

        # checks if player have enough magic and speed points
        if skill.magic_points_cost > player.magic_points:
            return "Not enough magic points!"

        elif skill.speed_points_cost > player.speed_points:
            return "Not enough speed points!"

        # deduct points
        player.magic_points -= skill.magic_points_cost
        player.speed_points -= skill.speed_points_cost

        # return log from using skill
        return skill.use(self.active_player, self.active_enemy)
