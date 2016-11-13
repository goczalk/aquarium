"""
"""

import pygame

def load_png(name):
    """ Load image and return image object"""
    try:
        image = pygame.image.load(name)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    return image, image.get_rect()
