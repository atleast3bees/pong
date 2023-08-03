"""
Author : Rori Wu

Date : 7/19/23

Description: Runs the pong program
"""

import yaml
# this is the AI library
import stable_baselines3 as sb3
from stable_baselines3.common.env_checker import check_env
from envs.pong import PongEnvironment



if __name__ == "__main__":
    try:
        with open('config/pong_parameters.yaml', 'r') as file:
            configs = yaml.safe_load(file)
    except FileNotFoundError:
        print("File not found")

    Pong = PongEnvironment(configs['scorelimit'], configs['agent'], configs['colorid'], "human")
    check_env(Pong) # Ensure we match the gym interface
    terminated = False

    # Set up model
    model = sb3.PPO("MultiInputPolicy", Pong, verbose=1)
    model.learn(total_timesteps=250000)
    model.save("ppo_pong")

    del model
    #Load and evaluate agent
    model = sb3.PPO.load("brians_pongAI")
    obs = Pong.reset()

    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = Pong.step(action)
        Pong.render()

    Pong.close()