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

PLANCTON_NUM = 100

def main():
    pygame.init()

    size = [1000, 500] #width, height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Aquarium')
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    ball = Fish()
    
    # lista przechowująca plankton
    plankton_list = []
    for _ in range(PLANCTON_NUM):
        plankton_list.append(Plancton())
    
    ballsprite = pygame.sprite.RenderPlain(ball)

    # Initialise clock
    clock = pygame.time.Clock()
    
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        # screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, (0, 0))
        
        ball.update(screen)
        
        # which index does the ball bump into, -1 => none
        plankton_index = ball.rect.collidelist([plankton.rect for plankton in plankton_list])
        if plankton_index != -1:
            # remove from list and add as much energy as big the plancton was
            ball.increase_energy((plankton_list.pop(plankton_index)).radius)
        
        #TODO
        #narysuj plankton raz i sprawdzaj czy zjedzony?? -> da się?
        for plankton in plankton_list:
            plankton.draw(screen)
        
        ballsprite.draw(screen)
        
        pygame.display.flip()

if __name__ == '__main__': main()
