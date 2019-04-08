from blinkt import set_pixel, show, clear
from random import randint
from time import sleep

rainbow = [[255,0,0],[255, 127, 0],[255, 255, 0],[0, 255, 0],[0, 0, 255],[75, 0, 130],[148, 0, 211],[0,0,0]]
# rainbow = [[30,30,30],[30,30,30],[30,30,30],[30,30,30],[30,30,30],[30,30,30],[30,30,30]]

while True:
    clear()
    for i, pixel in enumerate(rainbow):
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        set_pixel(7 - i, r, g, b, 0.05)
        show()
        sleep(0.1)