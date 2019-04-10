from plant import *
import numpy as np


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
        state, dead = self.plants[self.time_step].current_state()
        plant = self.plants[self.time_step]

        old_moisture = state[0]  # current_moisture
        # print("-----Watering plant " + str(self.time_step) + str(self.plants[self.time_step])
        #       + "with amount: " + str(water_amount))
        new_moisture = plant.water(water_amount)  # carry out watering

        if self.good_reward_func:
            reward = self.good_reward(old_moisture, new_moisture, dead, water_amount)
        else:
            reward = self.bad_reward(dead, water_amount)

        self.time_step += 1
        self.time_step = self.time_step % self.num_plants
        new_state, dead = self.plants[self.time_step].current_state()

        # print("Time step: " + str(self.time_step) + " Reward: " + str(reward))

        return new_state, reward, self.is_done()

    def is_done(self):
        all_dead = True
        for plant in self.plants:
            if not plant.dead:
                all_dead = False
                break
        if all_dead:
            print("ALL DEAD")
        return all_dead

    @staticmethod
    def bad_reward(dead, water_amount):
        if water_amount > 0 and not dead:
            return 1
        return 0

    @staticmethod
    def good_reward(old_moisture, new_moisture, dead, water_amount):
        # more than "half-way saturated"
        if old_moisture > 0.5 or dead:
            return 0
        else:
            # not fully saturated
            if new_moisture[0] <= 1:
                # TODO rework logic?
                return (new_moisture[0] - old_moisture) / old_moisture
            return 0

    def current_state(self):
        return np.array(self.plants[self.time_step].current_state()[0])
