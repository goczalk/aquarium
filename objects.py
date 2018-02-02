"""
File with classes of creatures
"""

import random
import math
import pygame
from render import load_png

class Plancton:
    def __init__(self):
        self.x = random.randrange(1000)
        self.y = random.randrange(500)
        self.radius = 2
        
    def draw(self, screen):
        pygame.draw.circle(screen, 0x0066ff, (self.x, self.y), self.radius)
        
class Fish(pygame.sprite.Sprite):
    """
    Randomized position and vector.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_png('ball.png')
        self.vector = [0, 0]
        self._randomize_position()
        self._randomize_vector()

        #print (self.rect.x, self.rect.y)
        # screen = pygame.display.get_surface()
        # self.rect = pygame.draw.circle(screen, 663399, (10, 10), 15)
        # self.area = screen.get_rect()

    def _randomize_position(self):
        x = random.randrange(1000 - self.rect.width)
        y = random.randrange(500 - self.rect.height)
        self.rect = self.rect.move(x, y)
        
    def _randomize_vector(self):
        angle = random.uniform(0, 2 * math.pi)
        z = random.randrange(3, 7)
        self.vector = [angle, z]

    def update(self):
        self.rect = self.calc_new_pos(self.rect, self.vector)
        x, y, _, _= self.rect

        #refactor code
        if x > (1000 - self.rect.width):
            x = 1000 - self.rect.width
            self._randomize_vector()
        elif x < 0:
            x = 0
            self._randomize_vector()
        if y > (500 - self.rect.height):
            y = 500 - self.rect.height
            self._randomize_vector()
        elif y < 0:
            y = 0
            self._randomize_vector()
            
        self.rect.x = x
        self.rect.y = y

    def calc_new_pos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle),
                    z * math.sin(angle))
        return rect.move(dx, dy)
