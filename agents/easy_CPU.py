"""
Author : Rori Wu

Date : 7/19/23

Description: Contains the EasyAgent class for use in pong.py
"""

from numpy import random

class EasyAgent:

    #Initializes the EasyAgent class
    def __init__(self):
        self.ball_y = 150
        self.right_pos = 150
        
    #Returns the agent's action given a list argument
    def get_action(self, element):
        self.ball_y = element[0]
        self.right_pos = element[1]
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

