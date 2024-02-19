import random


class Team:
    def __init__(self, name):
        self.id = random.randint(0, 1000000)
        self.name = name
        self.score = 0

