import numpy as np


def bad_reward(dead, water_amount):
    if water_amount > 0 and not dead:
        return 1
    return 0


def good_reward(old_moisture, new_moisture):
    # gaussian function
    old_moisture_reward = np.exp(-np.power(old_moisture - 0.5, 2.) / (2 * np.power(0.25, 2.)))
    new_moisture_reward = np.exp(-np.power(new_moisture - 0.5, 2.) / (2 * np.power(0.25, 2.)))

    return new_moisture_reward - old_moisture_reward
