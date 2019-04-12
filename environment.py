from plant import *
import numpy as np
from numpy.random import seed

seed(7)


class Environment:
    def __init__(self, num_plants, good_reward_func):
        self.observation_space = 2  # current_moisture and soil
        self.action_space = 1
        self.num_plants = num_plants
        self.good_reward_func = good_reward_func  # true or false

        # function reset() resets these
        self.time_step = 0
        self.plants = [Plant() for _ in range(num_plants)]

    def reset(self):
        self.time_step = 0
        for plant in self.plants:
            plant.reset()
        return self.current_state()

    def step(self, water_amount):
        # states contains "current_moisture and soil"
        state = self.plants[self.time_step].current_state()
        plant = self.plants[self.time_step]

        old_moisture = state[0][0]  # current_moisture
        # print("Old moisture: " + str(old_moisture))
        # print("-----Watering plant " + str(self.time_step) + str(self.plants[self.time_step])
        #       + "with amount: " + str(water_amount))
        new_moisture, dead = plant.water(water_amount)  # carry out watering
        # print("Plant: " + str(self.time_step) + " with new moisture: " + str(new_moisture) + " and Dead: " + str(dead) + "\n")

        # if self.good_reward_func:
        #     reward = self.good_reward(old_moisture, new_moisture, dead, water_amount)
        # else:
        #     reward = self.bad_reward(dead, water_amount)

        reward = (self.good_reward(new_moisture, dead, water_amount)
                  + self.bad_reward(dead, water_amount)) / 2

        new_state, _ = plant.current_state()

        self.time_step += 1
        self.time_step = self.time_step % self.num_plants

        if self.time_step > 0 and self.time_step % self.num_plants == 0:
            for p in self.plants:
                p.update()

        return new_state, reward, self.is_done()

    def is_done(self):
        all_dead = True
        for plant in self.plants:
            if not plant.dead:
                all_dead = False
                break
        if all_dead:
            pass
            # print("ALL DEAD")
        return all_dead

    @staticmethod
    def bad_reward(dead, water_amount):
        if water_amount > 0 and not dead:
            return 1
        return 0

    @staticmethod
    def good_reward(new_moisture, dead, water_amount):
        if water_amount == 0:
            return 0

        # more than "half-way saturated"
        if dead:
            return 0

        # gaussian function
        reward = np.exp(-np.power(new_moisture - 0.5, 2.) / (2 * np.power(0.25, 2.)))

        return reward

    def current_state(self):
        return np.array(self.plants[self.time_step].current_state()[0])
