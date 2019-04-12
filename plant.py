import random
import math
from numpy.random import seed

random.seed(7)  # REMOVE
seed(7)  # REMOVE

# (
#   enumerated value,
#   str representation of the pot size,
#   (minimum soil it must contain, max soil it can contain)
# )

POT_SIZES = [
    (1, "SMALL", (140, 200)),
    (2, "MEDIUM", (281, 400)),
    (3, "LARGE", (561, 800))
]


class Plant:
    def __init__(self):
        self.pot = random.choice(POT_SIZES)

        self.dead = False
        self.initial_moisture = random.random()  # do not generate 0
        self.current_moisture = self.initial_moisture
        self.soil = random.randint(*self.pot[2])

    def __str__(self):
        return "\nSize: " + self.pot[1] + "\nSoil: " + str(self.soil) + "\n"

    def reset(self):
        self.current_moisture = self.initial_moisture
        self.dead = False

    def current_state(self):
        return [self.current_moisture, self.soil], self.dead

    def water(self, water_amount):
        self.current_moisture = min(((self.current_moisture * self.soil) + water_amount) / self.soil, 1)
        # can kill by barely watering or over watering
        if self.current_moisture < 0.01 or self.current_moisture > 0.99:
            self.dead = True
        return self.current_moisture, self.dead

    def update(self):
        # ensures that water level drops over time (moisture decay)
        # TODO rework logic
        self.current_moisture = self.current_moisture * math.exp(-self.current_moisture)
