from numpy import random

class RandomAgent:
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
        else:
            if random.choice((0, 1)) == 1:
                return "UP"
            else:
                return "DOWN"