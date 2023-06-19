from combatgame.ui import Ui
from combatgame.scenes import Scenes

def main():
    """Main game flow."""
    while True:

        scenes = Scenes()

        start_menu_dict = {
            "Start": scenes.run_scenes,
            "Help": 1,
            "Settings": 2
        }

        Ui.Animation.display_welcome_screen()

        start_menu = Ui.Menu("CATastrophe Chronicles", start_menu_dict)
        selected = start_menu.select_option(print_line_by_line=True)

        scenes.show_lore = True

        if callable(selected):
            selected()
        else:
            print("Not callable")

def help():
    pass

def settings():
    pass

if __name__ == "__main__":
    main()
