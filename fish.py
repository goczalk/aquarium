"""
File with classes of creatures
"""

import random
from Tkinter import *

class Fish:
    def __init__(self, can):
        self.radius = 10
        self.x = random.randrange(1000) - self.radius
        self.y = random.randrange(500) - self.radius
        self.canvas = can

        self.id = Canvas.create_oval(self.canvas, self.x, self.y, self.x + self.radius, self.y + self.radius)

        self.vx = random.randrange(-5, 5)
        self.vy = random.randrange(-5, 5)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.canvas.move(self.id, self.vx, self.vy)
        self.canvas.after(1, self.move)

    # def accelarate(self):
    #     self.vx = random.randrange(-5, 5)
    #     self.vy = random.randrange(-5, 5)
    #     print 'accel:'
    #     print self.vx, self.vy
    #
    # def print_pos(self):
    #     print self.x, self.y