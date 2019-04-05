import random
import math as mt

# (
#   enumerated value,
#   str representation of the size,
#   (minimum soil it must contain, max soil it can contain)
# )

POT_SIZES = [
    (1, "SMALL", (100, 200)),
    (2, "MEDIUM", (201, 400)),
    (3, "LARGE", (401, 800))
]


class Plant:
    def __init__(self):
        self.pot = random.choice(POT_SIZES)

        self.dead = False
        self.initial_moisture = random.random()
        self.moisture = self.initial_moisture
        self.pot_size = self.pot[1]
        self.soil = random.randint(*self.pot[2])

    def __str__(self):
        return "Size: " + self.pot[1] + "\nSoil: " + str(self.soil) + "\n"

    def reset(self):
        self.moisture = self.initial_moisture
        self.dead = False

    def current_state(self):
        return [self.moisture, self.soil], self.dead

    def water(self, amt_watr):
        self.moisture = min(self.moisture + (amt_watr/self.soil), 1)
        # can only kill by over watering
        if self.moisture < 0.01:
            self.dead = True
        return self.moisture, self.dead


    def update(self):
        self.moisture = self.moisture * mt.exp(-self.moisture / self.soil)



