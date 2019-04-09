import random
import math

# (
#   enumerated value,
#   str representation of the size,
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
        # self.pot_size = self.pot[1]
        self.soil = random.randint(*self.pot[2])
        self.max_water_amount = self.soil * 0.3

    def __str__(self):
        return "Size: " + self.pot[1] + "\nSoil: " + str(self.soil) + "\n"

    def reset(self):
        self.current_moisture = self.initial_moisture
        self.dead = False

    def current_state(self):
        return [self.current_moisture, self.soil], self.dead

    def water(self, water_amount):
        # ensure amount_water is less than self.max_amount_water
        self.current_moisture = min(self.current_moisture + (water_amount / self.soil), 1)
        # can only kill by over watering
        if self.current_moisture < 0.01:
            self.dead = True
        return self.current_moisture, self.dead

    def update(self):
        # water level dropping over time

        # TODO rework logic
        self.current_moisture = self.current_moisture * math.exp(-(self.current_moisture * self.pot[2][1]) / self.soil)
