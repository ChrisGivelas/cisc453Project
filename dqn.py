from environment import *
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import pylab
from multiprocessing import Process
import os

DEFAULT_EPISODES = 80
DEFAULT_EPISODE_LENGTH = 40


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.out_threshold = 0.5
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        # each add is another layer with a specified number of neurons
        model.add(Dense(48, input_dim=self.state_size, activation='relu'))
        model.add(Dense(48, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        act_values = self.model.predict(state)
        return act_values[0][0]  # 0 < act_values[0][0] < 1

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, _, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * self.model.predict(next_state)[0][0])
                # int(self.model.predict(next_state)[0][0] < self.out_threshold))
            target_f = self.model.predict(state)
            target_f[0][0] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def run_simulation(title, good_reward_func, num_plants=20, episodes=DEFAULT_EPISODES,
                   episode_length=DEFAULT_EPISODE_LENGTH):
    env = Environment(num_plants=num_plants, good_reward_func=good_reward_func)
    state_size = env.observation_space
    action_size = env.action_space
    agent = DQNAgent(state_size, action_size)
    batch_size = 32

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(episode_length):
            pour_amount = agent.act(state)
            next_state, reward, done = env.step(pour_amount)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, pour_amount, reward, next_state, done)

            state = next_state
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

        print("episode: {}/{}\n\n".format(e, episodes))

    path = title + "_" + str(episodes) + "_" + str(episode_length)

    os.mkdir("plots/" + path)

    for index in range(num_plants):
        plot_plant(agent.memory, num_plants, index, title + " - Plant #" + str(index), env.plants[index], path)

    print("Simulation " + path + " done")


def plot_plant(memory, numb_plants, plant_index, title, plant, path):
    water_amount_array = []
    reward = []
    moisture_level_array = []

    for index in range(len(memory)):
        if index % numb_plants == plant_index:
            water_amount_array.append(memory[index][1])
            reward.append(memory[index][2])
            moisture_level_array.append(memory[index][0].min())

    pylab.title(title)
    pylab.plot(water_amount_array, '-r', label="Water Amount")
    pylab.plot(reward, '-b', label="Reward")
    pylab.plot(moisture_level_array, '-g', label="Moisture")
    pylab.plot([], '-o', label="Pot size: " + plant.pot[1])
    pylab.plot([], '-p', label="Soil amount: " + str(plant.soil))
    pylab.legend(loc='upper right')

    pylab.savefig('plots/' + path + "/" + title + '.png')

    pylab.close()


# def sim1():
#     # run_simulation("Good Reward Function", True, episodes=500, episode_length=200)
#     # run_simulation("Good Reward Function", True, episodes=600, episode_length=300)
#     # run_simulation("Good Reward Function", True, episodes=700, episode_length=400)
#     run_simulation("Good Reward Function", True, episodes=800, episode_length=400)
#
#
# def sim2():
#     # run_simulation("Bad Reward Function", False, episodes=500, episode_length=200)
#     # run_simulation("Bad Reward Function", False, episodes=600, episode_length=300)
#     # run_simulation("Bad Reward Function", False, episodes=700, episode_length=400)
#     run_simulation("Bad Reward Function", False, episodes=500, episode_length=200)
#
#
# if __name__ == "__main__":
#     # p1 = Process(target=sim1)
#     # p1.start()
#     # p2 = Process(target=sim2)
#     # p2.start()
#     # p1.join()
#     # p2.join()
#     sim1()
