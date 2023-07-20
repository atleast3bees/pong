import yaml
from pong_reorganized import PongEnvironment
try:
    with open('config.yaml', 'r') as file:
        configs = yaml.safe_load(file)
    Pong = PongEnvironment(configs['scorelimit'],configs['agent'])
    terminated = False
    while not terminated:
        action = Pong.getPlayerInput()
        terminated = Pong.step(action)
        Pong.render()
    Pong.close()
except FileNotFoundError:
    print("File not found")