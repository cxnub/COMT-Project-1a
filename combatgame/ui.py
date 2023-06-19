"""
User Interface Module
=====================

This module contains UI elements and utilities for the game.

"""

import os
import sys
import msvcrt
import time
import random
import threading
import textwrap
from typing import AnyStr, Dict, TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from characters import BaseCharacter
    from enemies import EnemyCharacter


class Ui:
    """
    User Interface class to handle user input, displays game prompts and messages,
    and interacts with the game manager.
    """

    @staticmethod
    def create_percentage_bar(
        current_stat: int,
        max_stat: int,
        bar_length: int=20,
        filled_char: str="█",
        empty_char: str="▒"
        ):
        """Creates a percentage bar.

        Parameters
        ----------
        current_stat : int
            The current amount of that stat.
        max_stat : int
            The max amount of that stat.
        bar_length : int
            The length of the bar in number of characters. Defaults to 20.
        """

        # makes sure the bar dont over extend
        current_stat = min(current_stat, max_stat)

        # calculate the length of the bar to be filled
        filled_length = int(bar_length * current_stat / max_stat)

        # return the percentage bar string
        percentage_bar = f"{filled_char * filled_length:{empty_char}<{bar_length}s}"
        return f"{percentage_bar} {current_stat}/{max_stat}"

    @staticmethod
    def clear_terminal():
        """Clear the terminal screen"""

        # for others
        if os.name == "posix":
            os.system("clear")

        # for windows
        elif os.name == "nt":
            os.system("cls")

    @staticmethod
    def ordinal(number: int):
        """Returns the ordinal string of integer.

        Parameters
        ----------
        number : int
            The number to convert to ordinal string.

        Returns
        -------
        str : ordinal string of the integer.
        """

        # special for 11th, 12th and 13th as it ends with th.
        if 11 <= (number % 100) <= 13:
            suffix = 'th'

        # select the appropriate suffix based on the last digit of the number
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(number % 10, 4)]
        return str(number) + suffix

    @staticmethod
    def execute_lore(lore: str = None):
        """prints the lore given. 
        Use "|" to split sentences into paragraphs.

        Parameters
        ----------
        lore : str
        the lore to be displayed. Defaults to None.
        """
        # clear terminal
        Ui.clear_terminal()

        # splits lore into paragraphs
        paragraphs = lore.split("|")

        # loops through paragraphs to print to console
        for paragraph in paragraphs:
            paragraph = paragraph.rstrip()
            Ui.Animation.print_with_animation(paragraph)
            input("\n\n\nPress enter to continue...")
            Ui.clear_terminal()

    @staticmethod
    def display_ascii_art(*characters, sep: str = "|") -> list:
        """Prints ASCII art side by side and sets the starting_column_position for the characters.

        Parameters
        ----------
        *arts : List[str]
            List of ASCII arts to print out.
        sep : str, optional
            The seperator used to separate the arts horizontally. Defaults to "|".

        Returns
        -------
        sep_column_position: int
            Starting column position for seperator.
        """

        # store all the character's ASCII Art in a list
        arts = [character.ascii_art for character in characters]

        # get the height of the tallest art
        tallest_art_height = max(map(len, arts), default=0)

        # iterate through every art
        for index, art in enumerate(arts):

            # Calculate the number of extra lines needed for alignment
            height_difference = tallest_art_height - len(art)

            # append and prepend extra lines to align to bottom
            art = [" "] * height_difference + art + [" "]

            # Get the width of the longest line
            longest_width = max(map(len, art), default=0)

            # longest_width has to be at least 35 characters long or else percentage bars
            # for combat stats would not fit
            longest_width = max(longest_width, 35)

            # add trailing whitespace to each line to match longest_width
            arts[index] = [line.ljust(longest_width) for line in art]

        starting_column_positions = [0]
        seperator_column_positions = []

        # print every line
        for lines in zip(*arts):
            print(sep.join(lines))

            # runs the following code only once
            if len(starting_column_positions) == 1:

                # iterate through every art line
                for line in lines:
                    # calculate the seperator starting column position
                    seperator_starting_column = starting_column_positions[-1] + len(line)

                    # appends the calculated position to the seperator_column_position list
                    seperator_column_positions.append(seperator_starting_column)

                    # calculate the starting column position of the art
                    line_starting_column = starting_column_positions[-1] + len(line) + len(sep)

                    # appends the calculated position to the starting_column_positions list
                    starting_column_positions.append(line_starting_column)

        # store starting column position
        for index, character in enumerate(characters):
            character.starting_column_position = starting_column_positions[index]

        return seperator_column_positions

    @staticmethod
    def place_string(string: str, start: int=0):
        """Format a string to start at a specific column.

        Parameters
        ----------
        string : str
            The string to format.
        start : int
            The starting column position. Defaults to 0.

        Return
        ------
        string : The formatted string.
        """

        return " " * (start - 1) + string

    @staticmethod
    def display_combat_stats(
        player_character: "BaseCharacter",
        enemy_character: "EnemyCharacter",
        sep_column_position: int,
        sep: str="|"
        ):
        """Displays the statistics of both player and enemy characters.
        
        Parameters
        ----------
        player_character : BaseCharacter
            The player character object.
        enemy_character : EnemyCharacter
            The enemy character object.
        sep : str
            The seperator string between player character and enemy character stats.
        seperator_column_position : int
            The column position of the seperator.
        """

        def add_seperator(string: str):
            # add the seperator at its start position in a string and return back the string
            return string[:sep_column_position] + sep + string[len(sep) + sep_column_position - 1:]

        def create_stats_line(character):
            # define the stat title and the display of that stat
            stats = {
                "Name": character.name,
                "HP": Ui.create_percentage_bar(
                    character.health_points,
                    character.max_health_points
                    ),
                "DP": Ui.create_percentage_bar(
                character.defense_points,
                character.max_defense_points
                ),
                "Attack": f"{character.attack_points} Points",
                "Speed": f"{character.speed_points} Points",
                "Luck": f"{character.luck} Points"
            }

            # list of stats line
            stats_line = []

            # iterate through each and every stats
            for stat_name, stat_display in stats.items():

                # place the stat line string at the character's starting position
                line = Ui.place_string(
                    f"{stat_name}: {stat_display}",
                    character.starting_column_position
                )

                # append the line to stats_line list
                stats_line.append(line)

            return stats_line

        # create stats_line for player and enemy characters
        player_stats_lines = create_stats_line(player_character)
        enemy_stats_lines = create_stats_line(enemy_character)

        stat_display_lines = []

        # combine both player_stats_lines and enemy_stats_lines into a single line
        # as well as add the seperator in
        for line1, line2 in zip(player_stats_lines, enemy_stats_lines):
            stat_display_lines.append(add_seperator(f"{line1}{line2[len(line1):]}"))

        # append for additional player character stats
        stat_display_lines.append(f"Magic: {player_character.magic_points} Points")

        # active effects
        active_effects = ', '.join(str(effect) for effect in player_character.active_effects) \
            if player_character.active_effects else ""
        stat_display_lines.append(f"Effects: {active_effects}")

        # print out the stats
        print("\n".join(stat_display_lines))


    @staticmethod
    def display_combat_screen(
        player_character: "BaseCharacter",
        enemy_character: "EnemyCharacter",
        battle_log: List[str]
        ):
        """Displays the whole combat screen.
        
        player_character : BaseCharacter
            The player character object.
        enemy_character : EnemyCharacter
            The enemy character object.
        battle_log : list of str
            The battle logs.
        """
        # define the seperator between character and enemy
        seperator = " " * 20

        # print ASCII Art and get the start position of seperator
        seperator_column_position = Ui.display_ascii_art(
            player_character,
            enemy_character,
            sep=seperator
            )

        # display the stats of the characters
        Ui.display_combat_stats(
            player_character,
            enemy_character,
            seperator_column_position[0],
            sep=seperator
            )

        print()

        # display's battle log
        print("COMBAT LOG")
        print("==========")
        print("\n".join(battle_log))
        print("==========")

    class Animation:
        """Container class for animation functions."""

        @staticmethod
        def print_with_animation(
            string: AnyStr = None,
            line_length: int = 80,
            speed: int = 500
        ) -> None:
            """Prints text with typing animation.

            Parameters
            ----------
            string : str
                The string to print. Defaults to None.

            line_length : int
                Max number of characters per line. Defaults to 80.

            speed : int 
                The speed of the typing animation (characters per minute).
                Defaults to 500.
            """
            skip = False
            finished = False
            string = string.replace("\n", "")

            def listen_for_skip():
                # listens for skip
                nonlocal skip
                # for windows
                if os.name == "nt":
                    while not finished:
                        # listen for spacebar
                        if msvcrt.kbhit() and ord(msvcrt.getch()) == 32:
                            skip = True
                            break

                # for unix based systems
                else:
                    while not finished:
                        # listen for spacebar
                        if sys.stdin.read(1) == " ":
                            skip = True
                            break

            # create and start the skip listening thread
            space_bar_thread = threading.Thread(target=listen_for_skip)
            space_bar_thread.start()

            buffer = ""

            print("Press [space bar] to skip...")

            # loops through every character in the string provided and prints
            # it one by one
            for char in string:

                # check if skip is activated
                if skip:
                    Ui.clear_terminal()
                    print()
                    # prints everything with line break
                    print('\n'.join(textwrap.wrap(string, line_length)))
                    break

                buffer += char
                sys.stdout.write(char)

                # checks if line exceeded line_length limit
                if char == " " and len(buffer) > line_length:
                    sys.stdout.write("\n")  # insert new line
                    buffer = ""  # resets buffer

                # sets the speed of typing animation, skips if char is a space
                if not char.isspace():
                    time.sleep(speed / (5*3600))

                # pause at a fullstop
                if char == ".":
                    time.sleep(0.3)

                sys.stdout.flush()

            finished = True

        @staticmethod
        def print_line_by_line(string, delay=0.15):
            """Scrolling up animation for printing text.
            
            Parameters
            ----------
            string : str
                The string to print.
            delay : float
                The delay in seconds. Defaults to 0.15.
            """

            lines = string.split("\n")

            for line in lines:
                print(line)
                time.sleep(delay)

        @staticmethod
        def display_welcome_screen():
            """Prints the welcome screen."""

            # clears terminal screen
            Ui.clear_terminal()

            Ui.Animation.print_line_by_line(r"""
CATastrophe Chronicles: The Wildcat Cafe
──────────┰──────────────────┰──────────
          ┃                  ┃
      ╭──━┸━─━─━─━─━─━─━─━─━─┷─━─╮
      ┃                          ┃
      │        Welcome To        │
      │    The Wildcat Cafe!     │
      ┃                          ┃
      ╰─━─━─━─━─━─━─━─━─━─━─━─━─━╯
            """)

            Ui.Animation.print_line_by_line(r"""
           _   _._
          |_|-'_~_`-._
       _.-'-_~_- _-~-_`-._
   _.-'_~-_~-_-~-_~_~-_~-_`-._
  ━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━
    ┃  ┌─┬─┐    σ    ┌─┬─┐  ┃
    ┃  ├─┼─┤  ┏━━━┓  ├─┼─┤  ┃   
  ._┃  └─┴─┘  ┃  .┃  └─┴─┘  ┃_._._._._._._._._._._._._._._._._.  
  |=┗━━━━━━━━━┻━━━┻━━━━━━━━━┛|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=| 
^^^^^^^^^^^^^^ === ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
    __________    ===             : ¨·.·¨ :
   <_CatσCafe_>     ===            ` ·. 🦋
       ^|^            ===                   ╱|、
        |                ===              (˚ˎ。7               
                            ===            |、˜〵        
                            ===            じしˍ,)ノ          
            """)

        @staticmethod
        def display_combat_start(
            player_characters: List["BaseCharacter"],
            enemy_characters: List["EnemyCharacter"]
            ):
            """Displays the animation before the start of combat.
            
            Parameters
            ----------
            player_characters : List of BaseCharacter
                The player characters involved in the combat.
            enemy_characters : List of EnemyCharacter
                The enemy characters involved in the combat.
            """

            def display_teams(team: list):
                # display the whole team and the characters names

                # variable to store each characters name and their starting column position
                character_names_list = []

                Ui.display_ascii_art(*team, sep="")

                # loop through every character
                for character in team:

                    # add names below their ascii art respectively
                    character_names_list.append(
                        (f"Name: {character.name}", character.starting_column_position)
                        )

                # align character names to their respective position
                character_names_line = ''
                for string, column in character_names_list:
                    character_names_line += ("\t"+string).expandtabs(column-len(string))

                # print the formatted line
                print(character_names_line)

            Ui.clear_terminal()

            # display player characters
            display_teams(player_characters)
            time.sleep(1)
            Ui.clear_terminal()

            print("""\n\n\n
 oooooo     oooo  .oooooo..o 
  `888.     .8'  d8P'    `Y8 
   `888.   .8'   Y88bo.      
    `888. .8'     `"Y8888o.  
     `888.8'          `"Y88b 
      `888'      oo     .d8P 
       `8'       8""88888P'  
            """)
            time.sleep(1)
            Ui.clear_terminal()

            # display enemy characters
            display_teams(enemy_characters)
            time.sleep(1)
            Ui.clear_terminal()

            print("""\n\n\n
________  ______   ______   __    __  ________  __ 
/        |/      | /      \\ /  |  /  |/        |/ |
$$$$$$$$/ $$$$$$/ /$$$$$$  |$$ |  $$ |$$$$$$$$/ $$ |
$$ |__      $$ |  $$ | _$$/ $$ |__$$ |   $$ |   $$ |
$$    |     $$ |  $$ |/    |$$    $$ |   $$ |   $$ |
$$$$$/      $$ |  $$ |$$$$ |$$$$$$$$ |   $$ |   $$/ 
$$ |       _$$ |_ $$ \\__$$ |$$ |  $$ |   $$ |    __ 
$$ |      / $$   |$$    $$/ $$ |  $$ |   $$ |   /  |
$$/       $$$$$$/  $$$$$$/  $$/   $$/    $$/    $$/                              
            """)
            time.sleep(1)

        @staticmethod
        def display_game_over():
            """Displays game over ASCII Art,"""

            Ui.Animation.print_line_by_line(
                """\n\n\n
  ______    ______   __       __  ________ 
 /      \\  /      \\ /  \\     /  |/        |
/$$$$$$  |/$$$$$$  |$$  \\   /$$ |$$$$$$$$/ 
$$ | _$$/ $$ |__$$ |$$$  \\ /$$$ |$$ |__    
$$ |/    |$$    $$ |$$$$  /$$$$ |$$    |   
$$ |$$$$ |$$$$$$$$ |$$ $$ $$/$$ |$$$$$/    
$$ \\__$$ |$$ |  $$ |$$ |$$$/ $$ |$$ |_____ 
$$    $$/ $$ |  $$ |$$ | $/  $$ |$$       |
 $$$$$$/  $$/   $$/ $$/      $$/ $$$$$$$$/ 
            """
            )
            Ui.Animation.print_line_by_line("""
  ______   __     __  ________  _______  
 /      \\ /  |   /  |/        |/       \\ 
/$$$$$$  |$$ |   $$ |$$$$$$$$/ $$$$$$$  |
$$ |  $$ |$$ |   $$ |$$ |__    $$ |__$$ |
$$ |  $$ |$$  \\ /$$/ $$    |   $$    $$< 
$$ |  $$ | $$  /$$/  $$$$$/    $$$$$$$  |
$$ \\__$$ |  $$ $$/   $$ |_____ $$ |  $$ |
$$    $$/    $$$/    $$       |$$ |  $$ |
 $$$$$$/      $/     $$$$$$$$/ $$/   $$/                                                                                       
            """)

        @staticmethod
        def display_thunderstorm(frames: int=20):
            """Animate a thunderstorm in console.
            
            Parameters
            ----------
            frames : int
                The amount of frames to animate. Defaults to 20.
            """

            width, height = os.get_terminal_size()

            running_animation = True

            def lightning_animation():
                # for windows
                if os.name == "nt":
                    while running_animation:
                        for _ in range(2):
                            # flash twice
                            os.system("color 70")
                            time.sleep(0.2)
                            os.system("color 07")
                            time.sleep(0.2)

                        time.sleep(3)

            # run the lightning animation in the background
            lightning_animation = threading.Thread(target=lightning_animation)
            lightning_animation.start()

            raindrops = ""
            rain_animation = []

            # create raining animation
            for _ in range(frames):
                for _ in range(height-1):
                    for _ in range(width//3):
                        raindrops += " / " * random.randint(0, 1) + "   " * random.randint(1, 5)
                    rain_animation.append(raindrops[:width])
                    raindrops = ""

                print("\n".join(rain_animation))
                rain_animation = []
                time.sleep(0.5)
                Ui.clear_terminal()

            running_animation = False


    class Menu:
        """Represents a UI Menu.

        Attributes
        ----------
        title : str
            The title of the menu.
        options : Dict
            The available options in the menu.
        """

        def __init__(self, title: str, options_dict: Dict):
            """Initialize a UI Menu instance.

            Parameters
            ----------
            title : str
                The title of the menu.
            options_dict : Dict
                A dictionary where the key represents the display text of each option, and the
                values represent the corresponding return values.
            """ 
            self.title = title
            self.options = {}

            # set the last menu option to be quit
            options_dict["Quit"] = "Quit"

            # assign values to self.options
            for index, items in enumerate(options_dict.items(), start=1):
                # structure of self.options:
                # self.options = {
                #     index: {
                #         "display": items[0],
                #         "return": items[1]
                #         }
                # }

                # set key as index and value as empty dict
                options_index = self.options[index] = {}

                # set display and return values
                options_index["display"] = items[0]
                options_index["return"] = items[1]

        def display(self, padding: int = 5, print_line_by_line: bool=False):
            """Display the UI Menu.

            Parameters
            ----------
            padding : int, optional
                The number of spaces for padding around the menu content (default is 5).
            print_line_by_line : bool
                Whether to print the menu line by line. Default to False.
            """

            def wrap_string(string: str, wrapper: str):
                # wrap a string with a given wrapper string.
                return wrapper + string + wrapper

            title_length = len(self.title)

            # the length of the longest display string
            max_display_length = max(len(str(item['display'])) for item in self.options.values())

            # account for the numbering at the start of every option
            max_display_length += 2

            # if title_length more than or equals to max_display_length, box length will
            # correspond to the title_length
            if title_length >= max_display_length:
                box_length = title_length + (padding * 2) + 2

            # else, box length will correspond to the max_display_length
            else:
                box_length = max_display_length + (padding * 2) + 2

            # the lines in the menu display
            menu_lines = []

            # add the top border of the menu box
            menu_lines.append("╔" + "═" * (box_length - 2) + "╗")

            # add the menu title with padding and wrap it with border
            menu_lines.append(wrap_string(self.title.center(box_length - 2), "║"))

            # add the middle border of the menu box
            menu_lines.append("╠" + "═" * (box_length - 2) + "╣")

            # add each option with leading index and trailing whitespace for alignment
            for index, items in self.options.items():
                # get the display text from the nested dict
                display_text = items["display"]

                # format index and option
                option_str =f"{index}. {display_text}"

                # add trailling whitespace for alignment
                formatted_option_str = f"{option_str:<{box_length-2}}"

                # add formatted_option_str and wraps it with the box border
                menu_lines.append(wrap_string(formatted_option_str, "║"))

            # add the bottom border of the menu box
            menu_lines.append("╚" + "═" * (box_length - 2) + "╝")

            # string combined with newline
            menu_string = "\n".join(menu_lines)

            if print_line_by_line:
                Ui.Animation.print_line_by_line(menu_string)

            else:
                print(menu_string)


        def select_option(self, print_line_by_line: bool=False, invalid_handler: Callable=None):
            """Select an option from the menu and return the chosen option.

            Parameters
            ----------
            print_line_by_line : bool
                Whether to print the menu line by line. Default to False.
            invalid_handler : Callable
                The function to run when an invalid option is given.

            Returns
            -------
            Any : 
                The value associated with the selected option.

            """

            # runs forever until a valid input is given
            while True:
                # display the menu
                self.display(print_line_by_line=print_line_by_line)

                # gets user input
                choice = input("> ")

                # checks if user input is valid
                if choice.isdigit() and int(choice) in self.options:
                    # checks if Quit option is selected
                    if str(self.options[int(choice)]["return"]).lower() == "quit":
                        print("Quitting game...")

                        # wait 1 second before exiting script
                        time.sleep(1)
                        sys.exit()

                    # return chosen option corresponding return value
                    return self.options[int(choice)]["return"]

                else:
                    # check if invalid_handler is given
                    if invalid_handler:
                        invalid_handler()

                    else:
                        # auto handles invalid input by running itself again
                        print("Invalid choice. Please enter again.")

                        # clears terminal after 1 second
                        time.sleep(1)
                        Ui.clear_terminal()
