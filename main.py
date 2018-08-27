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
from AquariumLabels import AquariumLabels
import pygame
from pygame.locals import *
from pgu import gui

import random
import math
import time

""" CONSTANTS """
""" SCREEN """
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

""" PLANCTON """
PLANCTON_START_NUM = 50
PLANCTON_TIMER = 360
PLANCTON_MAX_TO_ADD = 80
MAX_RADIANS_VALUE = 180 * 0.017
RADIANS_CHANGE = MAX_RADIANS_VALUE/8 # how many radians are added to random range max to calculate sinus of how much plancton will be produced. bigger the division, slower the sinusoidal func will go

""" FISH """
FISH_START_NUM = 10


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, SWSURFACE)
    pygame.display.set_caption('Aquarium')
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # For labels and sliders 
    app = gui.App()
    aqLabel = AquariumLabels()
    c = gui.Container(align=-1,valign=-1)
    c.add(aqLabel, 0, 0)
    app.init(c)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # list of fish
    fish_list = []
    fishsprite_list = []
    for _ in range(FISH_START_NUM):
        fish_list.append(Fish())
    #male_fish_list = []
    #female_fish_list = []
    #for fish in fish_list:
    #    if fish.gender == "female":
    #        female_fish_list.append(fish)
    #    else:
    #        male_fish_list.append(fish)

    # list of fish eggs
    eggs_list = []    

    # list of generatated plancton objects
    plancton_list = []
    plancton_add_counter = 0
    plancton_random_range_radians = 0
    for _ in range(PLANCTON_START_NUM):
        plancton_list.append(Plancton())
    
    # Initialise clock
    clock = pygame.time.Clock()
    done = False
    # accumulator = 0
    #kork_Czasowy (dt) = 1 [ms]
    while not done:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)
        
        # roznica w czasie miedzy kolejnymi ramkami

        # delta = current - last
        # last = current
        # acumulator += delta
        # while(acumulator > dt ){
        # for (ile-razy-szybciej) {krok symulacji}
        # acumulator -= dt}

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
          #  elif e.type is KEYDOWN and e.key == K_ESCAPE: 
          #      done = True
            else:
                app.event(event)

        screen.blit(background, (0, 0))
        
        # male and female counters
        male_counter = 0
        female_counter = 0 

        # generate additional plancton every PLANCTON_TIMER
        plancton_add_counter += 1
        if plancton_add_counter == PLANCTON_TIMER:
            plancton_add_counter = 0

            random_start = int(plancton_random_range_radians * 1000)
            plancton_random_range_radians += RADIANS_CHANGE
            random_stop = int(plancton_random_range_radians * 1000)

            sinus_value = math.sin(
                                random.randrange(
                                    random_start,
                                    random_stop)/1000)

            number_of_plancton_to_add = int(PLANCTON_MAX_TO_ADD * sinus_value)

            if plancton_random_range_radians >= MAX_RADIANS_VALUE :
                plancton_random_range_radians = 0

            for _ in range(number_of_plancton_to_add):
                plancton_list.append(Plancton())

        copy_list = list(fish_list)
        for fish in copy_list:
            if fish.gender == "female":
                female_counter += 1
            else:
                male_counter += 1

            fish.update()
            egg = fish.lay_eggs()
            eggs_list += [egg] if egg is not None else []
            fish.draw()

            # check if bumped into plancton
            # which index does the ball bump into, -1 => none
            plancton_index = fish.rect.collidelist([plancton.rect for plancton in plancton_list])
            if plancton_index != -1:
                # remove from list and add as much energy as big the plancton was
                fish.increase_energy((plancton_list.pop(plancton_index)).radius)

            # check if bumped into other fish

            # uwazaj na przypadek samozjadania gdy rybka rosnie
            fish_index = fish.rect.collidelist(fish_list)
            if fish_index != -1:
                if fish.size > fish_list[fish_index].size:
                    eaten_fish = fish_list.pop(fish_index)
                    # remove from list and add as much energy as big the fish was
                    fish.increase_energy(eaten_fish.size)
                    if eaten_fish.gender == "female":
                        female_counter -= 1
                    else:
                        male_counter -= 1

            # check if bumped into egg
            egg_index = fish.rect.collidelist([egg.rect for egg in eggs_list])
            if egg_index != -1:
                if fish.fertilize_eggs():
                    # remove from list and add fish
                    eggs_list.pop(egg_index)
                    new_fish = Fish()
                    fish_list.append(new_fish)
                    if new_fish.gender == "female":
                        female_counter += 1
                    else:
                        male_counter += 1

        # update labels in Statistic
        aqLabel.update_plancton_fish_labels(len(plancton_list), male_counter, female_counter)

        # check eggs and draw
        for egg in list(eggs_list):
            if not egg.is_fresh():
                eggs_list.remove(egg)
        for egg in eggs_list:
            egg.draw()

        # check plancton and draw
        for plancton in plancton_list:
            if not plancton.is_fresh():
                plancton_list.remove(plancton)
        for plancton in plancton_list:
            plancton.draw()

        # For labels and sliders 
        app.paint()

        pygame.display.flip()

if __name__ == '__main__': main()
