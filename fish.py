"""
File with classes of creatures
"""

import random

class Fish:
    def __init__(self):
        self.length = 10
        self.x = random.randrange(200)
        self.y = random.randrange(200)
        self.vx = random.randrange(-5, 5)
        self.vy = random.randrange(-5, 5)

    def move(self, t):
        self.x += self.vx * t
        self.y += self.vy * t

    def accelarate(self):
        self.vx = random.randrange(-5, 5)
        self.vy = random.randrange(-5, 5)
        print 'accel:'
        print self.vx, self.vy

    def print_pos(self):
        print self.x, self.y