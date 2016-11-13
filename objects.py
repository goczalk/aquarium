"""
File with classes of creatures
"""

import random
import math
import pygame
from render import load_png


class Fish(pygame.sprite.Sprite):
    """
    Randomized position and vector.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_png('ball.png')
        self.vector = [0, 0]
        self._randomize_position_and_vector()

        # screen = pygame.display.get_surface()
        # self.rect = pygame.draw.circle(screen, 663399, (10, 10), 15)
        # self.area = screen.get_rect()

    def _randomize_position_and_vector(self):
        x = random.randrange(1000 - self.rect.width)
        y = random.randrange(500 - self.rect.height)
        self.rect = self.rect.move(x, y)
        angle = random.uniform(0, 2 * math.pi)
        z = random.randrange(3, 7)
        self.vector = [angle, z]

    def update(self):
        newpos = self.calc_new_pos(self.rect, self.vector)
        self.rect = newpos

    def calc_new_pos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle),
                    z * math.sin(angle))
        return rect.move(dx, dy)
