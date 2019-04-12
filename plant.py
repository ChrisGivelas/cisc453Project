import random
import math

# Each pot has a string representation of its size, along with a
# tuple containing the min and max amount of soil it can contain

POT_SIZES = [
    ("SMALL", (140, 200)),
    ("MEDIUM", (281, 400)),
    ("LARGE", (561, 800))
]


class Plant:
    def __init__(self):
        self.pot = random.choice(POT_SIZES)

        self.dead = False
        self.initial_moisture = random.random()  # do not generate 0
        self.current_moisture = self.initial_moisture
        self.soil = random.randint(*self.pot[1])

    def reset(self):
        self.current_moisture = self.initial_moisture
        self.dead = False

    def current_state(self):
        return [self.current_moisture, self.soil]

    def water(self, water_amount):
        self.current_moisture = (water_amount / self.soil) + self.current_moisture
        # can kill by barely watering or over watering
        if self.current_moisture < 0.01 or self.current_moisture > 0.99:
            self.dead = True
        return self.current_moisture, self.dead

    def decay_moisture(self):
        # ensures that water level drops over time (moisture decay)
        self.current_moisture = self.current_moisture * math.exp(-self.current_moisture)
