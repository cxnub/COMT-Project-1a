import os
import time
import threading
import random




def thunderstorm():
    """Animate a thunderstorm in console."""

    width, height = os.get_terminal_size()

    running_animation = True

    def lightning_animation():
        # for windows
        if os.name == "nt":
            while running_animation:
                for _ in range(2):
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
    for _ in range(20):
        for _ in range(height-1):
            for _ in range(width//3):
                raindrops += " / " * random.randint(0, 1) + "   " * random.randint(1, 5)
            rain_animation.append(raindrops[:width])
            raindrops = ""

        print("\n".join(rain_animation))
        rain_animation = []
        time.sleep(0.5)
        os.system("cls")

    running_animation = False

thunderstorm()