import random


class Players:
    def __init__(self, name):
        self.id = "player" + str(random.randint(0, 1000000))
        self.name = name
        self.score = 0

