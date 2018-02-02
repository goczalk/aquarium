"""
File with classes of creatures
"""

import random
import math
import pygame
from render import load_png

class Plancton:
    """
    self.xy
    self.rect
    self.radius
    """
    
    def __init__(self):
        x = random.randrange(1000)
        y = random.randrange(500)
        self.radius = random.randrange(2, 4)
        self.xy = (x, y)
        self.rect = pygame.Rect(self.xy, (self.radius, self.radius))
        
    def draw(self, screen):
        pygame.draw.circle(screen, 0x0066ff, self.xy, self.radius)
        
class Fish(pygame.sprite.Sprite):
    """
    self.velocity
    self.angle
    self.image
    self.rect
    self.vector
    self.energy
    self.FONT
    """
    MAX_ENERGY = 300
    ENERGY_LABEL_HEIGHT = 5
    ENERGY_LABEL_WIDTH = 30
    
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # initilize font
        self.FONT = pygame.font.SysFont("monospace", 15)

        self.image, self.rect = load_png('ball.png')
        self.vector = [0, 0]
        self._randomize_position()
        self._randomize_vector()
        self.energy = Fish.MAX_ENERGY

        #print (self.rect.x, self.rect.y)
        # screen = pygame.display.get_surface()
        # self.rect = pygame.draw.circle(screen, 663399, (10, 10), 15)
        # self.area = screen.get_rect()

    def _randomize_position(self):
        x = random.randrange(1000 - self.rect.width)
        y = random.randrange(500 - self.rect.height)
        self.rect = self.rect.move(x, y)
        
    def _randomize_vector(self):
        self.angle = random.uniform(0, 2 * math.pi)
        # random speed
        self.velocity = random.randrange(3, 6)

    def update(self, screen):
        # check if dead
        if self.energy > 0:
            self.rect = self.calc_new_pos()
            x, y, _, _= self.rect

            # refactor code
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
            self.energy -= 1
            self.draw_energy_indicators(screen)
        
    def draw_energy_indicators(self, screen):
        # render text
        energy_num_label = self.FONT.render(str(self.energy), 1, (0, 0, 0))
        x, y, width, height = self.rect
        y_label = y - height/1.5
        if y <= 0:
            y_label = y + height*1.5
        screen.blit(energy_num_label, (x, y_label))

        # draw rect with energy
        energy_ratio = self.energy/Fish.MAX_ENERGY
        energy_label_width = Fish.ENERGY_LABEL_WIDTH * energy_ratio
        Rgb = 255
        if energy_ratio > 0.5:
            Rgb = 255 - 255 * energy_ratio
        y_rect = y - height/5
        if y <= 0:
            y_rect = y + height*1.2
        pygame.draw.rect(screen, (Rgb, 200, 0), (x, y_rect, energy_label_width, Fish.ENERGY_LABEL_HEIGHT))
            
            
    def calc_new_pos(self):
        (dx, dy) = (self.velocity * math.cos(self.angle),
                    self.velocity * math.sin(self.angle))
        return self.rect.move(dx, dy)
    
    def increase_energy(self, value):
        self.energy += 20*value
        if self.energy > Fish.MAX_ENERGY:
            self.energy = Fish.MAX_ENERGY
    
