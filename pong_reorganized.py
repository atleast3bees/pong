import sys
import pygame
from numpy import random
sys.path.append("agents")
from easy_CPU import EasyAgent
from hard_CPU import HardAgent

easy = EasyAgent()
hard = HardAgent()

class InvalidAgentError(Exception):
    "Raised when an invalid agent is passed in"
    pass

class PongEnvironment:
    randv = (-5, 5)

    def __init__(self, score_limit = 20, agent = "random_action"):
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
        self.agent = agent
    
    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 return True

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

        if self.left_pos > 0:
            if action[pygame.K_w]:
                self.left_pos -= 400 * self.dt 
        if self.left_pos < 250:        
            if action[pygame.K_s]:
                self.left_pos += 400 * self.dt
        
        if self.agent == "player":
            if self.right_pos > 0:
                if action[pygame.K_UP]:
                    self.right_pos -= 400 * self.dt
            if self.right_pos < 250:
                if action[pygame.K_DOWN]:
                    self.right_pos += 400 * self.dt
        elif self.agent == "random_agent":
            if random.choice((0, 1)) == 1:
                if self.right_pos > 0:
                    self.right_pos -= 400 * self.dt
            else:
                if self.right_pos < 250:
                    self.right_pos += 400 * self.dt
        elif self.agent == "easy_cpu":
            easy.update(self.ball_y, self.right_pos)
            if easy.get_action() == "UP":
                self.right_pos -= 400 * self.dt
            else:
                self.right_pos += 400 * self.dt
        elif self.agent == "hard_cpu":
            hard.update(self.ball_y, self.right_pos)
            if hard.get_action() == "UP":
                self.right_pos -= 400 * self.dt
            else:
                self.right_pos += 400 * self.dt
        else:
            raise InvalidAgentError("Please select from ['player', 'random_agent', 'easy_cpu', 'hard_cpu']")
        if self.left_points >= self.score_limit or self.right_points >= self.score_limit:
            return True
        else:
            return False

    def render(self):
        self.screen.fill("black")
        pygame.draw.rect(self.screen, "white", (20, self.left_pos, 8, 50))
        pygame.draw.rect(self.screen, "white", (455, self.right_pos, 8, 50))
        for i in range (15):
            pygame.draw.rect(self.screen, "white", (238, i*20 + 5, 4, 10))
        self.left_text = self.my_font.render(str(self.left_points), False, "white")
        self.screen.blit(self.left_text, (160, 10))
        self.right_text = self.my_font.render(str(self.right_points), False, "white")
        self.screen.blit(self.right_text, (270, 10))
        pygame.draw.rect(self.screen, "white", (self.ball_x, self.ball_y, 8, 8))
        pygame.draw.rect(self.screen, "white", (self.ball_x-self.ball_xvelocity, self.ball_y-self.ball_yvelocity, 4, 4))

        pygame.display.flip()
        self.dt = self.clock.tick(60)/1000 
    
    @staticmethod
    def close():
        pygame.quit()
    
    @staticmethod
    def getPlayerInput():
        return pygame.key.get_pressed()