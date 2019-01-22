from main import initialize, env_step, get_RL_fish_state
import pygame
from pygame.locals import *
import random
import numpy as np

q_table = []


def main():
    # global q_table


    # TODO
    # change action, implement RL
    action = 1

    total_age, total_rewards, total_average_rewards_per_year = 0, 0, 0
    episodes = 100

    # TODO
    # delete
    episodes = 2
    for i in range(episodes):
        print("Episode {0}".format(i))

        initialize(RL=True)

        done = False
        rewards_in_episode = 0

        while not done:
            done = env_step(action)

            # tuple: ([energy, hp, num of near small placton, near big, far small, far big], reward, age)
            state, reward, age, years_passed = get_RL_fish_state()
            print(state, reward, age, years_passed)
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


    # q_table = np.zeros([env.observation_space.n, env.action_space.n])

    # python 3.6
    #print(f'Results after {episodes} episodes:')



"""Training the agent"""
#
# def train_agent():
#     global q_table
#
#     # Hyperparameters
#
#     #  learning rate (0<α≤1)
#     #  Just like in supervised learning settings, α is the extent to which our Q-values
#     #  are being updated in every iteration
#     alpha = 0.1
#
#
#     # γ  (gamma) is the discount factor (0≤γ≤1)
#     # determines how much importance we want to give to future rewards.
#     # A high value for the discount factor (close to 1) captures the long-term effective award
#     # whereas, a discount factor of 0 makes our agent consider only immediate reward, hence making it greedy.
#     gamma = 0.6
#
#     # We want to prevent the action from always taking the same route, and possibly overfitting,
#     # so we'll be introducing another parameter called ϵ "epsilon" to cater to this during training.
#     epsilon = 0.1
#
#     # For plotting metrics
#     # all_epochs = []
#     # all_penalties = []
#
#
#     # TODO
#     #smaller range?
#
#     # for i in range(1, 100001):
#     for i in range(1, 11):
#         # state = env.reset()
#
#         # epochs, penalties, reward, = 0, 0, 0
#         reward = 0
#         done = False
#
#         while not done:
#             if random.uniform(0, 1) < epsilon:
#                 action = env.action_space.sample()  # Explore action space
#             else:
#                 action = np.argmax(q_table[state])  # Exploit learned values
#
#             next_state, reward, done, info = env.step(action)
#
#             old_value = q_table[state, action]
#             next_max = np.max(q_table[next_state])
#
#             new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
#             q_table[state, action] = new_value
#
#             # if reward == -10:
#             #     penalties += 1
#
#             state = next_state
#             # epochs += 1
#
#         # if i % 100 == 0:
#         #     clear_output(wait=True)
#         #     print(f"Episode: {i}")
#
#     print("Training finished.\n")
#
#
# def evaluate_agent():
#     """Evaluate agent's performance after Q-learning"""
#
#     total_epochs, total_penalties = 0, 0
#     episodes = 100
#
#     for _ in range(episodes):
#         state = env.reset()
#         epochs, penalties, reward = 0, 0, 0
#
#         done = False
#
#         while not done:
#             action = np.argmax(q_table[state])
#             state, reward, done, info = env.step(action)
#
#             if reward == -10:
#                 penalties += 1
#
#             epochs += 1
#
#         total_penalties += penalties
#         total_epochs += epochs
#
#     print(f"Results after {episodes} episodes:")
#     print(f"Average timesteps per episode: {total_epochs / episodes}")
#     print(f"Average penalties per episode: {total_penalties / episodes}")


if __name__ == '__main__':
    main()
