from numpy import random

class EasyAgent:
    def __init__(self):
        self.ball_y = 150
        self.right_pos = 150
        
    def update(self, ball_y, right_pos):
        self.ball_y = ball_y
        self.right_pos = right_pos 

    def get_action(self):
        if self.right_pos >= 250:
            return "UP"
        elif self.right_pos <= 0:
            return "DOWN"
        elif self.ball_y > self.right_pos + 25:
            if random.rand() >= .7:
                return "UP"
            else:
                return "DOWN"
        else:
            if random.rand() >= .7:
                return "DOWN"
            else:
                return "UP"

