from agent import Agent
from environment import Environment
from time import gmtime, strftime
from tkinter import *
import numpy
import matplotlib.pyplot as pp
import os

DEFAULT_EPISODES = 80
DEFAULT_EPISODE_LENGTH = 40


def run_simulation(title="", num_plants=20, episodes=DEFAULT_EPISODES, episode_length=DEFAULT_EPISODE_LENGTH):
    print("START SIMULATION")

    env = Environment(num_plants=num_plants)
    state_size = env.observation_space
    action_size = env.action_space
    agent = Agent(state_size, action_size)
    batch_size = 32

    for e in range(episodes):
        state = env.reset()
        state = numpy.reshape(state, [1, state_size])
        for time in range(episode_length):
            pour_amount = agent.act(state)
            next_state, reward, done = env.step(pour_amount)
            next_state = numpy.reshape(next_state, [1, state_size])
            agent.remember(state, pour_amount, reward, next_state, done)

            state = next_state
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

        print("Episode {} of {} done...\n".format(e, episodes))

    generate_graphs(agent, env, title, num_plants, episodes, episode_length)

    print("END SIMULATION")


def generate_graphs(agent, environment, title, num_plants, episodes, episode_length):
    if not os.path.exists("plots"):
        os.mkdir("plots")

    if title == "":
        path = strftime("%Y-%m-%d %H_%M_%S", gmtime()) + " (" + str(episodes) + "_" + str(episode_length) + ")"
    else:
        path = title + "_" + str(episodes) + "_" + str(episode_length)

    if not os.path.exists(path):
        os.mkdir("plots/" + path)

    for plant_index in range(num_plants):
        plot_plant(agent.memory, num_plants, plant_index, "Plant #" + str(plant_index + 1),
                   environment.plants[plant_index], path)


def plot_plant(data_points, num_plants, plant_index, title, plant, path):
    water_amount_array = []
    reward = []
    moisture_level_array = []

    for index in range(len(data_points)):
        if index % num_plants == plant_index:
            water_amount_array.append(data_points[index][1])
            reward.append(data_points[index][2])
            moisture_level_array.append(data_points[index][0].min())

    pp.title(title + " | " + "Size: " + plant.pot[0] + " | " + "Soil: " + str(plant.soil))
    pp.plot(water_amount_array, '-r', label="Water Amount")
    pp.plot(reward, '-b', label="Reward")
    pp.plot(moisture_level_array, '-g', label="Moisture")
    pp.legend(loc='upper right')

    pp.savefig('plots/' + path + "/" + title + '.png')

    pp.close()


if __name__ == "__main__":
    episodes = input("Number of Training Episodes:")

    while not episodes.isdigit():
        episodes = input("Number of Training Episodes:")

    time_steps = input("Number of Time Steps per Episode:")

    while not time_steps.isdigit():
        time_steps = input("Number of Time Steps per Episode:")

    num_plants = input("Number of Plants:")

    while not num_plants.isdigit():
        num_plants = input("Number of Plants:")

    run_simulation(num_plants=int(num_plants), episodes=int(episodes), episode_length=int(time_steps))
