from main import run_simulation, initialize, simulation_step
import pygame
from pygame.locals import *
import random

application = None


def test():

    # plancton_max_to_add = 80
    # plancton_timer = 400
    # energy_point = 0.0015
    # multiplier_for_food = 3

    for plancton_timer in range(300, 530, 30):
        for plancton_max_to_add in range(80, 140, 10):
            for energy_point in range(15, 30, 5):
                energy_point = energy_point / 10000
                for multiplier_for_food in range(3, 6, 1):
                    if plancton_timer == 300 and (plancton_max_to_add == 80 or plancton_max_to_add == 90 or plancton_max_to_add == 100):

                              # and (multiplier_for_food == 3 or multiplier_for_food == 4 or multiplier_for_food == 5))
                        continue

                    random.seed(1)
                    whole_simulation(plancton_max_to_add, plancton_timer, energy_point, multiplier_for_food)



def whole_simulation(plancton_max_to_add, plancton_timer, energy_point, multiplier_for_food):
    try:

        initialize(plancton_max_to_add, plancton_timer, energy_point, multiplier_for_food)

        print("\nSimulation run with:")
        print("plancton_max_to_add:" + str(plancton_max_to_add))
        print("plancton_timer:" + str(plancton_timer))
        print("energy_point:" + str(energy_point))
        print("multiplier_for_food:" + str(multiplier_for_food))

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True

            are_all_fish_dead, time_passed, fish_sum = simulation_step()
            if are_all_fish_dead:
                print("Finished after: " + str(time_passed) + " steps")
                print("Average fish num: " + str(round(fish_sum/time_passed, 1)) + "\n")
                done = True
    except Exception as e:
        print("EXCEPTION")
        print(e)
        print("Finished after: " + str(time_passed) + " steps")
        print("Average fish num: " + str(round(fish_sum / time_passed, 1)) + "\n")


if __name__ == '__main__':
    test()
