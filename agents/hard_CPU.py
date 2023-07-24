from numpy import random

class HardAgent:
    def __init__(self):
        self.ball_y = 150
        self.right_pos = 150
        
    def update(self, element):
        self.ball_y = element[0]
        self.right_pos = element[1]

    def get_action(self):
        if self.right_pos >= 250:
            return "UP"
        elif self.right_pos <= 0:
            return "DOWN"
        elif self.ball_y > self.right_pos + 25:
            if random.rand() >= .9:
                return "UP"
            else:
                return "DOWN"
        else:
            if random.rand() >= .9:
                return "DOWN"
            else:
                return "UP"