"""
File with main function
"""

from objects import Fish, Plancton, FISH_YEAR, MAX_FISH_VISION, VISION_MULTIPLIER
from AquariumLabels import AquariumLabels
import pygame
from pygame.locals import *
from pgu import gui

import random
import math
import time

from speed import Speed

""" CONSTANTS """

""" SIMMULATION TIME """
# 30 actualizations per sec
TIME_STEP = 0.03
# max 1FPS
MAX_ACCUMULATED_TIME = 1.0

""" SCREEN """
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

""" PLANCTON """
PLANCTON_START_NUM = 50
PLANCTON_TIMER = 360
PLANCTON_MAX_TO_ADD = 80
HUNGER_PLANCTON_LIMIT = PLANCTON_MAX_TO_ADD * 0.6

MAX_RADIANS_VALUE = 180 * 0.017
# how many radians are added to random range max to calculate sinus of how much plancton will be produced. bigger the division, slower the sinusoidal func will go
RADIANS_CHANGE = MAX_RADIANS_VALUE / 8

""" FISH """
FISH_START_NUM = 10

DISEASE_DEADLINE = 3000  # number of units of screen refresh
DISEASE_PROBABILITY = 99

""" /CONSTANTS """

# list of fish
fish_list = []
fishsprite_list = []

# list of fish eggs
eggs_list = []

# list of generatated plancton objects
plancton_list = []
plancton_add_counter = 0
plancton_random_range_radians = 0

application = None
screen = None
background = None
aqLabel = None

time_unit_counter = 0
fish_year_passed = 1
disease_counter = 0


def main():
    initialize()

    last_update = time.clock()
    accumulator = 0.0
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            #  elif e.type is KEYDOWN and e.key == K_ESCAPE:
            #      done = True
            else:
                application.event(event)

        since_last_update = time.clock() - last_update
        last_update = time.clock()
        accumulator += since_last_update * Speed.get_sim_speed()
        accumulator = min(MAX_ACCUMULATED_TIME, accumulator)

        while accumulator > TIME_STEP:
            simulation_step()
            accumulator -= TIME_STEP


def initialize():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    global screen
    screen = pygame.display.set_mode(size, SWSURFACE)
    pygame.display.set_caption('Aquarium')
    # Fill background
    global background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    # For labels and sliders
    global application
    application = gui.App()
    global aqLabel
    aqLabel = AquariumLabels()
    c = gui.Container(align=-1, valign=-1)
    c.add(aqLabel, 0, 0)
    application.init(c)
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    global fish_list
    for _ in range(FISH_START_NUM):
        fish_list.append(Fish())

    global plancton_list
    for _ in range(PLANCTON_START_NUM):
        plancton_list.append(Plancton())


def simulation_step():
    global fish_list, fishsprite_list, eggs_list, plancton_list, plancton_add_counter, \
        plancton_random_range_radians, application, screen, background, aqLabel, \
        time_unit_counter, fish_year_passed

    time_unit_counter += 1

    check_is_disease_strikes()

    screen.blit(background, (0, 0))

    # male, female, ill counters
    male_counter = 0
    female_counter = 0
    ill_fish_counter = 0

    # generate additional plancton every PLANCTON_TIMER
    plancton_add_counter += 1
    plancton_add_counter, \
    plancton_list, \
    plancton_random_range_radians = generate_additional_plancton(plancton_add_counter, plancton_list,
                                                                 plancton_random_range_radians)

    # TODO
    # czy dobry taki warunek? czy rybka może wiedzieć ile w CAŁYM AKWARIUM jest jedzenia?
    # TODO
    # tylko dla ryb drapieznych
    set_fish_chasing_each_other()

    copy_list = list(fish_list)
    for fish in copy_list:

        if fish.is_ill:
            ill_fish_counter += 1

        if fish.gender == "female":
            female_counter += 1
        else:
            male_counter += 1

        egg = fish.lay_eggs()
        eggs_list += [egg] if egg is not None else []
        fish.draw()

        # check if bumped into plancton
        # which index does the ball bump into, -1 => none
        plancton_index = fish.rect.collidelist([plancton.rect for plancton in plancton_list])
        if plancton_index != -1:
            # remove from plancton_list and add as much energy as big the plancton was
            fish.increase_energy((plancton_list.pop(plancton_index)).radius)

        # check if bumped into other fish
        # uwazaj na przypadek samozjadania gdy rybka rosnie
        # fish_index = fish.rect.collidelist(fish_list)
        # if fish_index != -1:
        #     if fish.size > fish_list[fish_index].size:
        #         eaten_fish     = fish_list.pop(fish_index)
        #         # remove from list and add as much energy as big the fish was
        #         fish.increase_energy(eaten_fish.size)
        #         if eaten_fish.gender == "female":
        #             female_counter -= 1
        #         else:
        #             male_counter -= 1

        # TODO zjedzenie chorej rybki powoduje chorobę -> nie tylko przebywanie!
        # check_if_bumped_into_ill_fish(fish, fish_list)

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

    if time_unit_counter >= FISH_YEAR:
        fish_year_passed += 1
        time_unit_counter = 0

    # update labels in Statistic
    aqLabel.update_plancton_fish_labels(fish_year_passed, len(plancton_list), male_counter, female_counter,
                                        ill_fish_counter)

    eggs_list = check_freshness_and_draw(eggs_list)
    plancton_list = check_freshness_and_draw(plancton_list)

    # For labels and sliders
    application.paint()

    pygame.display.flip()


def set_fish_chasing_each_other():
    global plancton_list, fish_list
    if len(plancton_list) <= HUNGER_PLANCTON_LIMIT:
        for i, fish in enumerate(fish_list):
            closest_fish = get_closest_fish_in_sight(fish)
            if closest_fish is not None:
                fish.set_chased_fish(closest_fish)


def get_closest_fish_in_sight(current_fish):
    global fish_list
    min_dist = math.inf
    index = -1
    for i, fish in enumerate(fish_list):
        if fish != current_fish:
            dist = math.sqrt((current_fish.x - fish.x) * (current_fish.x - fish.x) +
                             (current_fish.y - fish.y) * (current_fish.y - fish.y))
            if dist <= MAX_FISH_VISION and dist <= fish.size * VISION_MULTIPLIER:
                if dist < min_dist:
                    min_dist = dist
                    index = i

    if index == -1:
        return None
    return fish_list[index]


def check_if_bumped_into_ill_fish(fish, fish_list):
    # check if bumped into ill fish and caught disease
    fish_index = fish.rect.collidelist(fish_list)
    if fish_index != -1:
        fish_bumped_into = fish_list[fish_index]
        if fish_bumped_into.is_ill:
            fish.catch_disease()


def check_is_disease_strikes():
    global disease_counter, fish_list
    disease_counter += 1
    if disease_counter >= DISEASE_DEADLINE:
        q = random.randrange(0, DISEASE_PROBABILITY)
        if q == 0:
            random_index = random.randrange(0, len(fish_list))
            fish_list[random_index].catch_disease()
            disease_counter = 0


def check_freshness_and_draw(item_list):
    for item in item_list:
        if not item.is_fresh():
            item_list.remove(item)
    for item in item_list:
        item.draw()
    return item_list


def generate_additional_plancton(plancton_add_counter, plancton_list, plancton_random_range_radians):
    if plancton_add_counter == PLANCTON_TIMER:
        plancton_add_counter = 0

        random_start = int(plancton_random_range_radians * 1000)
        plancton_random_range_radians += RADIANS_CHANGE
        random_stop = int(plancton_random_range_radians * 1000)

        sinus_value = math.sin(
            random.randrange(
                random_start,
                random_stop) / 1000)

        number_of_plancton_to_add = int(PLANCTON_MAX_TO_ADD * sinus_value)

        if plancton_random_range_radians >= MAX_RADIANS_VALUE:
            plancton_random_range_radians = 0

        for _ in range(number_of_plancton_to_add):
            plancton_list.append(Plancton())
    return plancton_add_counter, plancton_list, plancton_random_range_radians


if __name__ == '__main__': main()
