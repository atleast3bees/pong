"""
Author : Rori Wu

Date : 7/19/23

Description: Contains the PongEnvironment class and all of its functionality
"""

import sys
import pygame
from numpy import random
sys.path.append("agents")
from easy_CPU import EasyAgent
from hard_CPU import HardAgent
from random_CPU import RandomAgent

easyA = EasyAgent()
hardA = HardAgent()
randA = RandomAgent()
agentlist = ("player", "easy_cpu", "hard_cpu", "random_cpu")
agents = (easyA, hardA, randA)

class InvalidAgentError(Exception):
    "Raised when an invalid agent is passed in"
    pass

class InvalidInputError(Exception):
    "Raised when an invalid argument is passed in"
    pass

class PongEnvironment:
    randv = (-5, 5)

    #Intiializes the PongEnvironment class
    def __init__(self, score_limit = 20, agent_name = "player"):
        pygame.font.init()
        pygame.init()
        pygame.display.set_caption("Pong")
        self.screen = pygame.display.set_mode((480, 300))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.left_points = 0
        self.right_points = 0
        self.left_pos = self.screen.get_height() / 2
        self.right_pos = self.screen.get_height() / 2
        self.ball_x = 240
        self.ball_y = 150
        self.ball_xvelocity = random.choice(PongEnvironment.randv)
        self.ball_yvelocity = random.choice(PongEnvironment.randv)

        if isinstance(score_limit, int) and not isinstance(score_limit, bool):
            if score_limit < 1:
                self.score_limit = 1
            else:
                self.score_limit = score_limit
        else:
            raise InvalidInputError("Please enter an integer greater or equal to 1")
        if isinstance(agent_name, str) and not isinstance(agent_name, bool) and agent_name in agentlist:
            self.agent_name = agent_name
        else:
            raise InvalidAgentError("Please select from " + str(agentlist))
        for i in range (0, len(agentlist)-1):
            if self.agent_name == agentlist[i+1]:
                self.agent = agents[i]

   #Updates the time and stops the game when the score limit is reached
    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True

        self.dt = self.clock.tick(60)/1000 
        if self.left_points >= self.score_limit or self.right_points >= self.score_limit:
            return True
        else:
            return False

    #Runs all the ball physics and resets it if someone has scored
    def physics(self):
        self.ball_x += self.ball_xvelocity
        self.ball_y += self.ball_yvelocity
        if ((self.ball_x >= 450 and self.ball_x < 460 and self.right_pos <= self.ball_y and self.right_pos >= self.ball_y - 50) or (self.ball_x <= 25 and self.ball_x > 15 and self.left_pos <= self.ball_y and self.left_pos >= self.ball_y - 50)):
            self.ball_xvelocity *= -1
        if self.ball_y >= 295 or self.ball_y <= 5:
            self.ball_yvelocity *= -1
        if (self.ball_x >= 480 or self.ball_x <= 0):
            if self.ball_x >= 480:
                self.left_points += 1
            else:
                self.right_points += 1
            self.ball_x = 240
            self.ball_y = 150
            self.ball_xvelocity = random.choice(PongEnvironment.randv)
            self.ball_yvelocity = random.choice(PongEnvironment.randv)
    
    #Renders all the visual elements of the game
    def render(self):
        self.screen.fill("black")
        pygame.draw.rect(self.screen, "white", (20, self.left_pos, 8, 50))
        if self.agent_name == "player":
            pygame.draw.rect(self.screen, "white", (455, self.right_pos, 8, 50))
        else:
            pygame.draw.rect(self.screen, "red", (455, self.right_pos, 8, 50))
        for i in range (15):
            pygame.draw.rect(self.screen, "white", (238, i*20 + 5, 4, 10))
        self.left_text = self.my_font.render(str(self.left_points), False, "white")
        self.screen.blit(self.left_text, (160, 10))
        self.right_text = self.my_font.render(str(self.right_points), False, "white")
        self.screen.blit(self.right_text, (270, 10))
        pygame.draw.rect(self.screen, "white", (self.ball_x, self.ball_y, 8, 8))
        pygame.draw.rect(self.screen, "white", (self.ball_x-self.ball_xvelocity, self.ball_y-self.ball_yvelocity, 4, 4))

        pygame.display.flip() 

    #Dictates the actions of the agent
    def get_agentaction(self):
        if self.agent_name != "player":
            if self.agent.get_action((self.ball_y, self.right_pos)) == "UP":
                self.right_pos -= 400 * self.dt
            else:
                self.right_pos += 400 * self.dt

    #Dictates the actions of the player
    def get_playeraction(self, action):
        if self.left_pos > 0:
            if action[pygame.K_w]:
                self.left_pos -= 400 * self.dt 
        if self.left_pos < 250:        
            if action[pygame.K_s]:
                self.left_pos += 400 * self.dt
        if self.agent_name == "player":
            if self.right_pos > 0:
                if action[pygame.K_UP]:
                    self.right_pos -= 400 * self.dt
            if self.right_pos < 250:
                if action[pygame.K_DOWN]:
                    self.right_pos += 400 * self.dt
    
    #Quits the game
    @staticmethod
    def close():
        pygame.quit()
    
    #Returns player input
    @staticmethod
    def get_playerinput():
        return pygame.key.get_pressed()