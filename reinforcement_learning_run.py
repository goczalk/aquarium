import random
import time

import numpy as np
import pygame
from pygame.locals import *

from main import initialize, env_step, get_RL_fish_state


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
    start = time.time()
    train_agent()
    end = time.time()
    elapsed_time = end - start
    print("Training time: " + str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))


    start = time.time()
    evaluate_agent()
    end = time.time()
    elapsed_time = end - start
    print("Evaluating time: " + str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))


def train_agent():
    """Training the agent"""
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

    # TODO
    # range?
    for i in range(0, 100000):
        print("Training episode {0}".format(i))
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

    with open('statuses.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % state for state in states)
    with open('rewards.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % reward for reward in q_table)

    print("Training finished.\n")
    print(np.array(states))
    print()
    print(q_table)


def evaluate_agent():
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

    print('Results after {0} episodes:'.format(episodes))
    print('Average age per episode: {0}'.format(total_age / episodes))
    print('Average total rewards per episode: {0}'.format(int(total_rewards / episodes)))
    print('Average of total average rewards per year: {0}'.format(int(total_average_rewards_per_year / episodes)))

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
