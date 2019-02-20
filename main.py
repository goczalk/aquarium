"""
File with main function
"""

import math
import random
import time

import pygame
from pgu import gui
from pygame.locals import *

from AquariumLabels import AquariumLabels
from objects import Fish, Plancton, FISH_YEAR, is_in_vision, calculate_distance, Shelter
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

SHELTERS_START_NUM = 3

""" FISH """
FISH_START_NUM = 10

""" PLANCTON """
PLANCTON_START_NUM = 50
PLANCTON_TIMER = 300
PLANCTON_MAX_TO_ADD = 110
# if there will be less than 5 planctons per fish, hunters gonna hunt
MIN_PLANCTON_NUM_PER_FISH_NOT_HUNGRY = 5

MAX_RADIANS_VALUE = 180 * 0.017
# how many radians are added to random range max to calculate sinus of how much plancton will be produced.
# bigger the division, slower the sinusoidal func will go
RADIANS_CHANGE = MAX_RADIANS_VALUE / 8

""" DISEASE """
DISEASE_DEADLINE = 75 * FISH_YEAR  # number of units of screen refresh
DISEASE_PROBABILITY = 251

""" /CONSTANTS """

# list of fish
fish_list = []
fishsprite_list = []
dead_fish_list = []
fish_sum = 0 # for average purposes

# list of fish eggs
eggs_list = []

# list of generatated plancton objects
plancton_list = []
plancton_add_counter = 0
plancton_random_range_radians = 0

# list of shelters
shelters_list = []

application = None
screen = None
background = None
aqLabel = None

time_unit_counter = 0
fish_year_passed = 1
disease_counter = 0

fishRL = None


def run_simulation():
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


def init_global_variables():
    global fish_list, fishsprite_list, dead_fish_list, eggs_list, plancton_list, plancton_add_counter,\
        plancton_random_range_radians, shelters_list, application, screen, background, aqLabel, time_unit_counter,\
        fish_year_passed, disease_counter

    # list of fish
    fish_list = []
    fishsprite_list = []
    dead_fish_list = []
    fish_sum = 0

    # list of fish eggs
    eggs_list = []

    # list of generatated plancton objects
    plancton_list = []
    plancton_add_counter = 0
    plancton_random_range_radians = 0

    # list of shelters
    shelters_list = []

    application = None
    screen = None
    background = None
    aqLabel = None

    time_unit_counter = 0
    fish_year_passed = 1
    disease_counter = 0


def initialize(RL=False, plancton_max_to_add=None, plancton_timer=None, energy_point=None, multiplier_for_food=None):
    init_global_variables()

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
        # when config tests
        if energy_point:
            fish_list.append(Fish(energy_point, multiplier_for_food))
        else:
            fish_list.append(Fish())

    if RL:
        global fishRL
        fishRL = Fish(rl=True)
        fish_list.append(fishRL)

    global plancton_list
    for _ in range(PLANCTON_START_NUM):
        plancton_list.append(Plancton())

    global shelters_list
    for _ in range(SHELTERS_START_NUM):
        shelters_list.append(Shelter())

    # when config tests
    if plancton_max_to_add:
        global PLANCTON_MAX_TO_ADD
        PLANCTON_MAX_TO_ADD = plancton_max_to_add

    if plancton_timer:
        global PLANCTON_TIMER
        PLANCTON_TIMER = plancton_timer


def simulation_step():
    global fish_list, fishsprite_list, eggs_list, plancton_list, shelters_list, plancton_add_counter, \
        plancton_random_range_radians, application, screen, background, aqLabel, \
        time_unit_counter, fish_year_passed, fish_sum

    time_unit_counter += 1


    # TODO
    # DISEASES ARE TURNED OFF AS FOR RL TRANING AND TESTING IT IS TOO RANDOM TO GET ILL
    # check_is_disease_strikes()

    screen.blit(background, (0, 0))

    # male, female, ill counters
    male_counter = 0
    female_counter = 0
    predators_counter = 0
    ill_fish_counter = 0

    # generate additional plancton every PLANCTON_TIMER
    plancton_add_counter += 1
    plancton_add_counter, \
        plancton_list, \
        plancton_random_range_radians = generate_additional_plancton(plancton_add_counter, plancton_list,
                                                                     plancton_random_range_radians)

    remove_dead_fish_from_list()
    # dead fish are not printed !


    # for dead_fish in dead_fish_list:
    #     dead_fish.draw_circles_and_age()

    check_which_fish_in_shelter()
    # TODO
    # czy dobry taki warunek? czy rybka może wiedzieć ile w CAŁYM AKWARIUM jest jedzenia?
    set_fish_chasing_each_other()
    set_fish_escaping_from_each_other()

    copy_list = list(fish_list)
    for fish in copy_list:
        if fish.is_predator:
            predators_counter += 1

        if fish.is_ill:
            ill_fish_counter += 1

        if fish.gender == "female":
            female_counter += 1
        else:
            male_counter += 1

        fish.draw()
        check_if_bumped_into_plancton(fish)

        # TODO
        # uwazaj na przypadek samozjadania gdy rybka rosnie
        female_counter, male_counter = check_if_fish_eats_other_fish(female_counter, fish, male_counter)

        lay_egg(fish)
        female_counter, male_counter = check_if_bumped_into_egg(female_counter, fish, male_counter)

    if time_unit_counter >= FISH_YEAR:
        fish_year_passed += 1
        time_unit_counter = 0
        fish_sum += len(fish_list)

    # update labels in Statistic
    aqLabel.update_plancton_fish_labels(fish_year_passed, len(plancton_list), male_counter, female_counter,
                                        predators_counter, ill_fish_counter)

    eggs_list = check_freshness_and_draw(eggs_list)
    plancton_list = check_freshness_and_draw(plancton_list)

    # TODO
    # shorter for loop?
    for shelter in shelters_list:
        shelter.draw()

    # For labels and sliders
    application.paint()

    pygame.display.flip()

    # to return for looping when finding optimal configuration
    if not fish_list:
        are_all_fish_dead = True
    else:
        are_all_fish_dead = False

    return are_all_fish_dead, fish_year_passed, fish_sum


def check_which_fish_in_shelter():
    for shelter in shelters_list:
        for fish in fish_list:
            if shelter.rect.contains(fish.rect):
                fish.in_shelter = True
            else:
                fish.in_shelter = False


def remove_dead_fish_from_list():
    for fish in list(fish_list):
        if fish.hp <= 0:
            dead_fish_list.append(fish)
            fish_list.remove(fish)


def check_if_fish_eats_other_fish(female_counter, fish, male_counter):
    if fish.is_predator:
        fish_index = fish.rect.collidelist(fish_list)
        if fish_index != -1:
            if fish.size > fish_list[fish_index].size:
                # remove from list and add as much energy as big the fish was
                eaten_fish = fish_list.pop(fish_index)
                eaten_fish.hp = 0
                fish.increase_energy(eaten_fish.size)

                if eaten_fish.gender == "female":
                    female_counter -= 1
                else:
                    male_counter -= 1

                if eaten_fish.is_ill:
                    fish.catch_disease()

    return female_counter, male_counter


def lay_egg(fish):
    global eggs_list
    egg = fish.lay_eggs()
    eggs_list += [egg] if egg is not None else []


def check_if_bumped_into_egg(female_counter, fish, male_counter):
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
    return female_counter, male_counter


def check_if_bumped_into_plancton(fish):
    # which index does the ball bump into, -1 => none
    plancton_index = fish.rect.collidelist([plancton.rect for plancton in plancton_list])
    if plancton_index != -1:
        # remove from plancton_list and add as much energy as big the plancton was
        fish.increase_energy((plancton_list.pop(plancton_index)).radius)


def set_fish_chasing_each_other():
    global plancton_list, fish_list

    hunger_plancton_limit = MIN_PLANCTON_NUM_PER_FISH_NOT_HUNGRY * len(fish_list)
    if len(plancton_list) <= hunger_plancton_limit:
        for fish in fish_list:
            if fish.is_predator:
                closest_fish = get_closest_appropriate_fish_in_sight(fish, fish_is_smaller_and_not_in_shelter)
                fish.set_chased_fish(closest_fish)
    else:
        for fish in fish_list:
            fish.set_chased_fish(None)


def set_fish_escaping_from_each_other():
    global plancton_list, fish_list
    for fish in fish_list:
        if fish.in_shelter:
            continue
        closest_fish = get_closest_appropriate_fish_in_sight(fish, fish_is_bigger_predator)
        fish.set_escape_from_fish(closest_fish)


def get_closest_appropriate_fish_in_sight(current_fish, size_relation_func):
    global fish_list
    min_dist = math.inf
    index = -1
    for i, fish in enumerate(fish_list):
        if fish != current_fish and size_relation_func(fish, current_fish):
            dist = calculate_distance(current_fish, fish)
            if is_in_vision(fish, dist):
                if dist < min_dist:
                    min_dist = dist
                    index = i

    if index == -1:
        return None
    return fish_list[index]


def fish_is_smaller_and_not_in_shelter(fish, current_fish):
    if not fish.in_shelter and fish.size < current_fish.size:
        return True
    return False


def fish_is_bigger_predator(fish, current_fish):
    if fish.is_predator and fish.size > current_fish.size:
        return True
    return False


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


""" Functions for RL """

# HARDCODED VALUES FOR SMALL/BIG AND NEAR/FAR !
BIG_PLANCTON = 4
NEAR_PLANCTON = 80
FAR_PLANCTON = 180

def calculate_plancton_distances():
    near_small, near_big, far_small, far_big = 0, 0, 0, 0

    for plancton in plancton_list:
        if plancton.radius == BIG_PLANCTON:
            is_big = True
        else:
            is_big = False

        distance = calculate_distance(fishRL, plancton)
        if distance <= NEAR_PLANCTON:
            if is_big:
                near_big += 1
            else:
                near_small += 1
        elif distance <= FAR_PLANCTON:
            if is_big:
                far_big += 1
            else:
                far_small += 1

    new_numbers = []
    for number in [near_small, near_big, far_small, far_big]:
        if number >= 13:
            number = 13
        elif number >= 8:
            number = 8
        elif number >= 5:
            number = 5
        elif number >= 3:
            number = 3
        elif number >= 1:
            number = 1

        new_numbers.append(number)
        continue

    near_small, near_big, far_small, far_big = new_numbers
    return near_small, near_big, far_small, far_big


def round_to_five(x):
    base = 5
    if x == 1:
        return x
    return int(base * round(float(x)/base))

def calculate_reward():
    x = fishRL.hp
    y = fishRL.energy
    reward = int((2 * x * x + y * y) - 3000)
    return reward

def get_RL_fish_state():
    """
    energy and hp and rounded to five
    distance to plancton is rounded to Fibonnaci numbers (except for 2; maximum 13)
    :return: tuple: ([energy, hp, num of near small placton, near big, far small, far big],
                    reward, fishRL.age, fish_year_passed)
    """
    near_small, near_big, far_small, far_big = calculate_plancton_distances()

    reward = calculate_reward()
    return [round_to_five(fishRL.energy), round_to_five(fishRL.hp), near_small, near_big, far_small, far_big],\
           reward, fishRL.age, fish_year_passed


# TODO
# optimise
def env_step(action):
    """
    :param action
    Env step, chooses placton to chase (for RL fish), based on action (int).

    0 - near and small
    1 - near and big
    2 - far and small
    3 - far and big
    else (ex. 4) - random

    One env step is one fish year. RL algorithm can change decision based on changing E and HP. Also, to compare results
    we have to have consitent number of rewards gathered.
    :return: True if RL fish is dead or False if it isn't. Dead fish means episode 'done'.
    """
    choose_point_randomly = False

    if action == 0:
        is_big = False
        is_near = True
    elif action == 1:
        is_big = True
        is_near = True
    elif action == 2:
        is_big = False
        is_near = False
    elif action == 3:
        is_big = True
        is_near = False
    else:
        choose_point_randomly = True

    if choose_point_randomly:
        fishRL.choose_random_point_to_chase()
    else:
        found_plancton = find_matching_plancton(is_big, is_near)
        if found_plancton is None:
            fishRL.choose_random_point_to_chase()
        else:
            # found_plancton.colour = 0x000000
            fishRL.point_x = found_plancton.x
            fishRL.point_y = found_plancton.y

    # env_step returns every FISH_YEAR
    is_fish_dead = False
    for _ in range(FISH_YEAR):
        if fishRL.hp <= 0:
            is_fish_dead = True
            return is_fish_dead

        simulation_step()

    return is_fish_dead


def find_matching_plancton(is_big, is_near):
    found_plancton = None

    for plancton in plancton_list:
        if is_big:
            if plancton.radius == BIG_PLANCTON:
                if _plancton_if_near_enough(plancton, is_near):
                    found_plancton = plancton
                    break
        else:
            if plancton.radius != BIG_PLANCTON:
                if _plancton_if_near_enough(plancton, is_near):
                    found_plancton = plancton
                    break

    return found_plancton


def _plancton_if_near_enough(plancton, is_near):
    distance = calculate_distance(fishRL, plancton)
    if is_near:
        if distance <= NEAR_PLANCTON:
           return True
        else:
            return False
    else:
        if distance <= FAR_PLANCTON:
            return True
        else:
            return False


if __name__ == '__main__':
    run_simulation()
