"""
File with main function
"""

# import time
# import render
#
# since_last_update = 0.0
# last_update = time.clock()
#
# print last_update
#
# accumulator = 0.0
#
# #30 actualizations per sec
# TIME_STEP = 0.03
# #max 1FPS
# MAX_ACCUMULATED_TIME = 1.0
#
#
# i = 0
# while ( i != 10):
#     since_last_update = time.clock() - last_update
#     since_last_update = max(0, since_last_update)
#     last_update += since_last_update
#     accumulator += since_last_update
#     accumulator = min(MAX_ACCUMULATED_TIME, accumulator)
#
#     #grab input
#     if (i == 2):
#         time.sleep(0.5)
#     while( accumulator > TIME_STEP):
#         #update
#         print 'Klaudia'
#         accumulator -= TIME_STEP
#     #render
#     i+=1

from objects import Fish, Plancton
import pygame
from pygame.locals import *

""" CONSTANTS """
""" SCREEN """
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

""" PLANCTON """
PLANCTON_START_NUM = 200
PLACTON_TIMER = 300
PLANCTON_ADD_NUM = 50

""" FISH """
FISH_START_NUM = 10

def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Aquarium')
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # list of fish
    fish_list = []
    fishsprite_list = []
    for _ in range(FISH_START_NUM):
        fish_list.append(Fish())

    for fish in fish_list:
        fishsprite_list.append(pygame.sprite.RenderPlain(fish))

    # ballsprite = pygame.sprite.RenderPlain(ball)
    
    # list of generatated plancton objects
    plankton_list = []
    plancton_add_counter = 0
    for _ in range(PLANCTON_START_NUM):
        plankton_list.append(Plancton())
    
    # Initialise clock
    clock = pygame.time.Clock()
    
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        
        # generate additional plancton every PLACTON_TIMER
        plancton_add_counter += 1
        if plancton_add_counter == PLACTON_TIMER:
            plancton_add_counter = 0
            for _ in range(PLANCTON_ADD_NUM):
                plankton_list.append(Plancton())

        for fish in fish_list:
            fish.update()

            # which index does the ball bump into, -1 => none
            plankton_index = fish.rect.collidelist([plankton.rect for plankton in plankton_list])
            if plankton_index != -1:
                # remove from list and add as much energy as big the plancton was
                fish.increase_energy((plankton_list.pop(plankton_index)).radius)

        for plankton in plankton_list:
            plankton.draw()
        
        for fishsprite in fishsprite_list:
            fishsprite.draw(screen)
        
        pygame.display.flip()

if __name__ == '__main__': main()
