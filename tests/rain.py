import random
import time

WIDTH = 80  # Width of the console
HEIGHT = 25  # Height of the console

RAIN = '/'
EMPTY = ' '

def make_it_rain(total_time, wait_time, num_drops):
    for _ in range(total_time):
        scene = [EMPTY] * WIDTH  # Initialize an empty scene
        for _ in range(num_drops):
            x = random.randint(0, WIDTH - 1)
            scene[x] = RAIN  # Add raindrop at a random position

        # Print the scene
        for char in scene:
            print(char, end='')
        print()  # Move to the next line

        time.sleep(wait_time)

if __name__ == '__main__':
    total_time = 40  # Total time for which it rains (in frames)
    wait_time = 0.2  # Time between redrawing scene (in seconds)
    num_drops = 20  # Number of raindrops in the scene

    make_it_rain(total_time, wait_time, num_drops)
