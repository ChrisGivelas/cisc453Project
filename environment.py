from plant import *
import numpy as np


class Environment:
    def __init__(self, num_plants, reward_func):
        self.observation_space = 2
        self.action_space = 1
        self.timestep = 0
        self.num_plants = num_plants
        self.plants = [Plant() for x in range(num_plants)]
        self.reward_func = reward_func

    def reset(self):
        self.timestep = 0
        for plant in self.plants:
            plant.reset()
        return self.current_state()

    def step(self, amt_watr):
        state, dead = self.plants[self.timestep].current_state()
        plant = self.plants[self.timestep]

        old_moisture = state[0]
        new_moisture = plant.water(amt_watr)

        if self.reward_func:
            reward = self.good_reward(old_moisture, new_moisture, dead, amt_watr)
        else:
            reward = self.bad_reward(dead, amt_watr)

        self.timestep += 1
        self.timestep = self.timestep % self.num_plants
        new_state, dead = self.plants[self.timestep].current_state()

        #print("Timestep: " + str(self.timestep) + " Reward: " + str(reward))

        return new_state, reward, self.is_done()

    def is_done(self):
        all_dead = True
        for plant in self.plants:
            if not plant.dead:
                all_dead = False
                break
        if all_dead: print("ALL DEAD")
        return all_dead

    def bad_reward(self, dead, amt_watr):
        return 1 if amt_watr > 0 and not dead else 0

    def good_reward(self, old_moisture, new_moisture, dead, amt_watr):
        if old_moisture > 0.5 or dead:
            return 0
        else:
            if new_moisture <= 1:
                return 1 + (amt_watr / (1 + old_moisture))
            else:
                return 0

    def current_state(self):
        return np.array(self.plants[self.timestep].current_state()[0])
