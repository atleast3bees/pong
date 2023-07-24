from numpy import random

class RandomAgent:
    def __init__(self):
        self.ball_y = 150
        self.right_pos = 150

    def get_action(self, element):
        self.ball_y = element[0]
        self.right_pos = element[1]
        if self.right_pos >= 250:
            return "UP"
        elif self.right_pos <= 0:
            return "DOWN"
        else:
            if random.choice((0, 1)) == 1:
                return "UP"
            else:
                return "DOWN"