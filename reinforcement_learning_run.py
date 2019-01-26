import os
import random
import time

import numpy as np
import pygame
from pygame.locals import *

from main import initialize, env_step, get_RL_fish_state

# TODO
# test without gui
# test after appriopriate learning
# 1k learning!


ACTIONS_SPACE_LEN = 5
INIT_STATE = [-1, -1, -1, -1, -1]  # this will never happen as normal state

# list of lists, [energy, hp, num of near small plancton, near big, far small, far big]; index of state is same as index
# of its reward in q_table
states = []

# two-dimensional;
# columns are actions: choose near small plancton, near big, far small, far big, random choice
# rows are rewards
q_table = None


def main():
    # set to True if you want to check what will be results for 'random fish', not RL-based
    test_random = True
    # test_random = False

    if not test_random:
        global q_table, states
        # change files depending on q_table you want to use
        old_read_states_and_q_table('statuses_po_1000.txt', 'rewards_po_1000.txt')
        print(states)
        print(len(states))
        print(q_table)
        print(len(q_table))

    loop_range = 1000
    if test_random:
        loop_range = 4
    for loop_counter in range(0, loop_range):

        if not test_random:
            print("Loop number {}".format(loop_counter))

            start = time.time()

            train_agent(loop_counter)

            end = time.time()
            elapsed_time = end - start
            print("Training time: " + str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

        start = time.time()

        evaluate_agent(loop_counter, test_random)

        end = time.time()
        elapsed_time = end - start
        print("Evaluating time: " + str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))


def TODO_STATE_TO_NUMPYARRAY_AND_NICE_WRITE():
    global q_table, states
    old_read_states_and_q_table('statuses.txt', 'rewards.txt')
    print(states)
    print(len(states))
    # print(q_table)
    # print(len(q_table))


    # statenew = np.array([states])

    # print(statenew)
    # write_states_and_rewards_to_files("xxx")
    #
    # states = []
    # print(states)
    # open_states_and_rewards_from_files("xxx")
    # print(states)


def train_agent(loop_count):
    if loop_count == 0:
        return

    """Training the agent"""
    # TODO
    # used?
    global q_table, states

    # Hyperparameters

    #  learning rate (0<α≤1)
    #  Just like in supervised learning settings, α is the extent to which our Q-values
    #  are being updated in every iteration
    alpha = 0.1

    # γ  (gamma) is the discount factor (0≤γ≤1)
    # determines how much importance we want to give to future rewards.
    # A high value for the discount factor (close to 1) captures the long-term effective award
    # whereas, a discount factor of 0 makes our agent consider only immediate reward, hence making it greedy.
    gamma = 0.6

    # We want to prevent the action from always taking the same route, and possibly overfitting,
    # so we'll be introducing another parameter called ϵ "epsilon" to cater to this during training.
    epsilon = 0.1

    for i in range(1, 1001):
        # because it was trained before

        real_episode_count = i + loop_count * 1000

        start = time.time()

        print("Training episode {0}".format(real_episode_count))
        initialize(RL=True)

        done = False
        state = INIT_STATE
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, ACTIONS_SPACE_LEN - 1)  # Explore action space
            else:
                action = get_best_action(state)  # Exploit learned values

            done = env_step(action)
            next_state, reward, _, _ = get_RL_fish_state()

            old_reward_value = get_reward_value(state, action)
            next_max = get_max_reward(next_state)

            new_reward_value = (1 - alpha) * old_reward_value + alpha * (reward + gamma * next_max)
            insert_to_lists(state, action, new_reward_value)

            state = next_state

        if i % 50 == 0:
            write_states_and_rewards_to_files(real_episode_count)
            # old_write_statues_rewards_to_file(real_episode_count)

        end = time.time()
        elapsed_time = end - start
        print("Episode training time: " + str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

    print("Training finished.\n")
    # print(np.array(states))
    # print()
    # print(q_table)


# TODO
# NICER TO SAVE STATES! -> old way now used!
def write_states_and_rewards_to_files(prefix):
    global states, q_table
    states_file_name = str(prefix) + "_states"
    rewards_file_name = str(prefix) + "_rewards"

    np.save(rewards_file_name, q_table)
    np.savetxt(rewards_file_name + ".txt", q_table)

    with open(states_file_name, 'w') as filehandle:
        filehandle.writelines("%s\n" % state for state in states)


# TODO
# NICER TO SAVE/READ STATES! -> old way to save was used!
def open_states_and_rewards_from_files(prefix):
    global states, q_table
    states_file_name = prefix + "_states"
    rewards_file_name = prefix + "_rewards.npy"
    q_table = np.load(rewards_file_name)


def old_write_statues_rewards_to_file(prefix):
    global states, q_table
    states_file_name = prefix + "_states.txt"
    rewards_file_name = prefix + "_rewards.txt"

    # TODO
    # change writing
    with open(states_file_name, 'w') as filehandle:
        filehandle.writelines("%s\n" % state for state in states)

    # TODO
    # change writing
    with open(rewards_file_name, 'w') as filehandle:
        filehandle.writelines("%s\n" % reward for reward in q_table)


# q_table = np.fromfile(rewards_file_name, sep=' ')
# q_table = np.loadtxt(rewards_file_name, dtype=np.ndarray)
def old_read_states_and_q_table(states_file_name, rewards_file_name):
    global q_table, states
    with open(states_file_name, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            items = line.split(',')
            temp = []
            for item in items:
                value = int(item.strip(']').strip('['))
                # results = list(map(int, results))
                temp.append(value)
            states.append(temp)

    count = 0
    lines_count = len(states)
    with open(rewards_file_name, 'r') as file:
        q_table = np.zeros([lines_count, ACTIONS_SPACE_LEN])

        for line in file:
            line = line.rstrip('\n')
            if line[-1] != ']':
                line += next(file)

            items = line.split()
            temp = []

            # print(items)
            for item in items:
                item = item.replace("]", "").replace("[", "")
                if item:
                    value = float(item)
                    temp.append(value)
            q_table[count] = temp
            count += 1


def evaluate_agent(loop_count, test_random):
    """Evaluate agent's performance after Q-learning"""
    global states, q_table

    # TODO
    # boolean to test only random fish
    # action = 4

    total_age, total_rewards, total_average_rewards_per_year = 0, 0, 0
    episodes = 100

    for i in range(episodes):
        print("Testing episode {0}".format(i))

        initialize(RL=True)

        rewards_in_episode = 0

        done = False
        state = INIT_STATE
        while not done:
            if test_random:
                action = ACTIONS_SPACE_LEN - 1
            else:
                action = get_best_action(state)
            done = env_step(action)

            # tuple: ([energy, hp, num of near small placton, near big, far small, far big], reward, age, years_passed)
            state, reward, age, years_passed = get_RL_fish_state()
            # print(state, reward, age, years_passed)
            rewards_in_episode += reward

        # passed one year less because we are starting from "1"
        years_passed -= 1

        total_age += age
        total_rewards += rewards_in_episode
        total_average_rewards_per_year += (rewards_in_episode / years_passed)

    with open("results", 'a') as text_file:
        if test_random:
            print('Results for random fish', file=text_file)

        print('Results in {} loop'.format(loop_count), file=text_file)
        print('Average age per episode: {}'.format(total_age / episodes), file=text_file)
        print('Average total rewards per episode: {}'.format(int(total_rewards / episodes)), file=text_file)
        print('Average of total average rewards per year: {}'.format(int(total_average_rewards_per_year / episodes)),
              file=text_file)

    if test_random:
        print('Results for random fish')
    print('Results in {} loop'.format(loop_count))
    print('Average age per episode: {}'.format(total_age / episodes))
    print('Average total rewards per episode: {}'.format(int(total_rewards / episodes)))
    print('Average of total average rewards per year: {}'.format(int(total_average_rewards_per_year / episodes)))

    # python 3.6
    #print(f'Results after {episodes} episodes:')


def get_best_action(state):
    global q_table, states
    action = random.randint(0, ACTIONS_SPACE_LEN - 1)
    try:
        state_index = states.index(state)
        action = np.argmax(q_table[state_index])
    except ValueError:
        # state not in states, action will be random
        pass
    return action


def get_reward_value(state, action):
    global q_table, states
    reward = 0
    try:
        state_index = states.index(state)
        reward = q_table[state_index][action]
    except ValueError:
        # state not in states, reward should be 0
        pass
    return reward


def get_max_reward(state):
    global q_table, states
    max_reward = 0
    try:
        state_index = states.index(state)
        max_reward = np.max(q_table[state_index])
    except ValueError:
        # state not in states, reward should be 0
        pass
    return max_reward

# TODO
# optimilize: numpy array shouldn't be appended; initilized with good values
def insert_to_lists(state, action, reward):
    global q_table, states
    try:
        state_index = states.index(state)
        q_table[state_index][action] = reward
    except ValueError:
        states.append(state)
        if q_table is None:
            q_table = initialize_q_table(action, reward)
        else:
            temp = np.zeros([1, ACTIONS_SPACE_LEN])
            temp[0, action] = reward
            q_table = np.append(q_table, temp, axis=0)


def initialize_q_table(action, reward):
    table = np.zeros([1, ACTIONS_SPACE_LEN])
    table[0, action] = reward
    return table


if __name__ == '__main__':
    main()
