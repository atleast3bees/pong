import yaml
from pong_reorganized import PongEnvironment
try:
    with open('pong_parameters.yaml', 'r') as file:
        configs = yaml.safe_load(file)
    Pong = PongEnvironment(configs['scorelimit'], configs['agent'])
    terminated = False
    while not terminated:
        action = Pong.get_playerinput()
        Pong.get_playeraction(action)
        Pong.get_agentaction()
        Pong.physics()
        Pong.render()
        terminated = Pong.step()
    Pong.close()
except FileNotFoundError:
    print("File not found")