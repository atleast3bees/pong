import yaml
from pong_reorganized import PongEnvironment
try:
    with open('pong_parameters.yaml', 'r') as file:
        configs = yaml.safe_load(file)
    Pong = PongEnvironment(configs['scorelimit'], configs['agent'])
    terminated = False
    while not terminated:
        action = Pong.getPlayerInput()
        Pong.getPlayerAction(action)
        Pong.getAgentAction()
        Pong.physics()
        Pong.render()
        terminated = Pong.step()
    Pong.close()
except FileNotFoundError:
    print("File not found")