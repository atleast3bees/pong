"""
Author : Rori Wu

Date : 7/19/23

Description: Contains the PongEnvironment class and all of its functionality
"""

import pygame
import yaml
from numpy import random
from agents.easy_CPU import EasyAgent
from agents.hard_CPU import HardAgent
from agents.random_CPU import RandomAgent
import numpy as np

import gym
from gym import spaces

easyA = EasyAgent()
hardA = HardAgent()
randA = RandomAgent()
agents = (easyA, hardA, randA)
with open("./config/agent_list.yaml", 'r') as stream:
    out = yaml.safe_load(stream)
agentlist = out['agents']

class InvalidAgentError(Exception):
    "Raised when an invalid agent is passed in"
    pass

class InvalidInputError(Exception):
    "Raised when an invalid argument is passed in"
    pass

class PongEnvironment(gym.Env):
    randv = (-5, 5)

    #Intiializes the PongEnvironment class
    def __init__(self, score_limit = 20, agent_name = "player", color_id = False, render_mode="human"):
        pygame.font.init()
        pygame.init()
        pygame.display.set_caption("Pong")
        # TODO: move into config
        self.screen_height = 300
        self.screen_width = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
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

        # ---------------------------------------------------------
        # Set Gymnasium fields
        # ---------------------------------------------------------
        self.observation_space = spaces.Dict(
            {
                'ball_y': spaces.Box(0, self.screen_height, shape=(1,), dtype=float),
                "left_pos": spaces.Box(0, self.screen_height, shape=(1,), dtype=float)
            }
        )

        self.action_space = spaces.Discrete(3)
        self.render_mode = render_mode

        #TODO: Move all error handling to helper function for readability
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
        if isinstance(color_id, bool):
            self.color_id = color_id
        else:
            raise InvalidInputError("Please enter in a boolean value, True or False")
        for i in range (0, len(agentlist)-1):
            if self.agent_name == agentlist[i+1]:
                self.agent = agents[i]

    def _get_obs(self):
        return {
            'ball_y': np.array([self.ball_y]),
            'left_pos': np.array([self.left_pos])
        }


   #Updates the time and stops the game when the score limit is reached
    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True

        # Initialize reward signal
        reward = 0
        # ---------------------------------------------------------
        # Handle Player/AI Action: 0 is nothing, 1 is down, 2 is up
        # ---------------------------------------------------------
        if action == 1 and self.left_pos < self.screen_height - 50:        
            self.left_pos += 400 * self.dt
        elif action == 2 and self.left_pos > 0:
            self.left_pos -= 400 * self.dt

        # --------------------------------------------------------
        # Handle CPU Action
        # --------------------------------------------------------
        self.get_agent_action()


        self.ball_x += self.ball_xvelocity
        self.ball_y += self.ball_yvelocity
        # TODO: Always remove as many hardcodes as possible, this would have broke if you adjusted screen size
        if ((self.ball_x >= self.screen_width-30 and self.ball_x < self.screen_width-20 and self.right_pos <= self.ball_y and self.right_pos >= self.ball_y - 50) or (self.ball_x <= 25 and self.ball_x > 15 and self.left_pos <= self.ball_y and self.left_pos >= self.ball_y - 50)):
            # if the ball hits my paddle
            if (self.ball_x <= 25 and self.ball_x > 15 and self.left_pos <= self.ball_y and self.left_pos >= self.ball_y - 50):
                reward += .25 #TODO: feel free to change me, experiment
            self.ball_xvelocity *= -1
        if self.ball_y >= self.screen_height-5 or self.ball_y <= 5:
            self.ball_yvelocity *= -1
        if (self.ball_x >= self.screen_width or self.ball_x <= 0):
            # if we scored on the CPU player
            if self.ball_x >= self.screen_width:
                self.left_points += 1
                reward += 1 #TODO: feel free to change me, experiment
            # if we got scored on
            else:
                self.right_points += 1
                reward -= 1 #TODO: feel free to change me, experiment
            self.ball_x = self.screen_width / 2
            self.ball_y = self.screen_height / 2
            self.ball_xvelocity = random.choice(PongEnvironment.randv)
            self.ball_yvelocity = random.choice(PongEnvironment.randv)

        self.dt = self.clock.tick(60)/1000 

        if self.left_points >= self.score_limit or self.right_points >= self.score_limit:
            terminated = True
        else:
            terminated =  False

        observation = self._get_obs()


        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, {}

    #Renders all the visual elements of the game
    def render(self):
        self.screen.fill("black")
        pygame.draw.rect(self.screen, "white", (20, self.left_pos, 8, 50))
        if self.agent_name == "player":
            pygame.draw.rect(self.screen, "white", (self.screen_width-25, self.right_pos, 8, 50))
        else:
            if self.color_id:
                pygame.draw.rect(self.screen, "red", (self.screen_width-25, self.right_pos, 8, 50))
            else:
                pygame.draw.rect(self.screen, "white", (self.screen_width-25, self.right_pos, 8, 50)) 
        for i in range (int(self.screen_height/20)):
            pygame.draw.rect(self.screen, "white", (self.screen_width/2 - 2, i*20 + 5, 4, 10))
        self.left_text = self.my_font.render(str(self.left_points), False, "white")
        self.screen.blit(self.left_text, (self.screen_width / 2 -80, 10))
        self.right_text = self.my_font.render(str(self.right_points), False, "white")
        self.screen.blit(self.right_text, (self.screen_width / 2 +80, 10))
        pygame.draw.rect(self.screen, "white", (self.ball_x, self.ball_y, 8, 8))
        pygame.draw.rect(self.screen, "white", (self.ball_x-self.ball_xvelocity, self.ball_y-self.ball_yvelocity, 4, 4))

        pygame.display.flip() 

    #Dictates the actions of the agent
    def get_agent_action(self):
        if self.agent_name != "player":
            if self.agent.get_action((self.ball_y, self.right_pos)) == "UP":
                self.right_pos -= 400 * self.dt
            else:
                self.right_pos += 400 * self.dt
        else:
            if self.right_pos > 0:
                if self.get_playerinput()[pygame.K_UP]:
                    self.right_pos -= 400 * self.dt
            elif self.right_pos < self.screen_height - 50:
                if self.get_playerinput()[pygame.K_DOWN]:
                    self.right_pos += 400 * self.dt

    #Dictates the actions of the player
    def get_playeraction(self, action):
        if self.left_pos > 0:
            if action[pygame.K_w]: 
                self.left_pos -= 400 * self.dt 
        if self.left_pos < self.screen_height - 50:        
            if action[pygame.K_s]:
                self.left_pos += 400 * self.dt
        if self.agent_name == "player":
            if self.right_pos > 0:
                if action[pygame.K_UP]:
                    self.right_pos -= 400 * self.dt
            if self.right_pos < self.screen_height - 50:
                if action[pygame.K_DOWN]:
                    self.right_pos += 400 * self.dt
                
    def reset(self):
        self.left_points = 0
        self.right_points = 0
        self.left_pos = self.screen.get_height() / 2
        self.right_pos = self.screen.get_height() / 2
        self.ball_x = 240
        self.ball_y = 150
        self.ball_xvelocity = random.choice(PongEnvironment.randv)
        self.ball_yvelocity = random.choice(PongEnvironment.randv)
        return self._get_obs()
    
    #Quits the game
    @staticmethod
    def close():
        pygame.quit()
    
    #Returns player input
    @staticmethod
    def get_playerinput():
        key =  pygame.key.get_pressed()
        action = 0
        if key[pygame.K_UP] or key[pygame.K_w]:
            action = 2
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            action = 1

        return action