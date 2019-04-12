from plant import *
from rewards import *
import numpy


class Environment:
    def __init__(self, num_plants):
        self.observation_space = 2  # current_moisture and soil
        self.action_space = 1
        self.num_plants = num_plants

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
        plant = self.plants[self.time_step]
        state = plant.current_state()

        old_moisture = state[0]  # current_moisture
        new_moisture, dead = plant.water(water_amount)  # carry out watering

        reward = (good_reward(old_moisture, new_moisture) + bad_reward(dead, water_amount)) / 2

        self.decay_plant_moistures()

        return plant.current_state(), reward, self.is_done()

    def decay_plant_moistures(self):
        if self.time_step + 1 % self.num_plants == 0:
            for p in self.plants:
                p.decay_moisture()

        self.time_step += 1
        self.time_step = self.time_step % self.num_plants

    def is_done(self):
        all_dead = True
        for plant in self.plants:
            if not plant.dead:
                all_dead = False
                break
        return all_dead

    def current_state(self):
        return numpy.array(self.plants[self.time_step].current_state())
