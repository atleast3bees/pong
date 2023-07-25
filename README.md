# Pong

A simple recreation of the classic video game 'Pong' using PyGame. Comes with three premade agents (easy, hard, random) as well as player vs player capabilities. Player controls are WASD to move up and down. If pvp is selected, player 2 controls use the arrow keys.

## Example Agents

Easy: The easy agent can be beaten with relative ease.

![ezgif com-video-to-gif](https://github.com/atleast3bees/pong/assets/111519324/89a37118-1e1b-4c23-9c25-8f47c6b4b18f)

Hard: The hard agent is much more difficult to beat.

![ezgif com-video-to-gif](https://github.com/atleast3bees/pong/assets/111519324/525ffd85-d0bc-404a-8f8a-22fae6895709)

Random: The random agent moves randomly, and is by far the easiest agent to beat.

![ezgif com-video-to-gif](https://github.com/atleast3bees/pong/assets/111519324/3361229c-d26a-41f8-b69e-0274c0fb38e6)

Player: Manual control for two players.

![ezgif com-video-to-gif](https://github.com/atleast3bees/pong/assets/111519324/ba55139b-7405-4db1-94f6-ee109090e9c2)

## Installation and Usage

The repo comes with a .yaml file for easy configuration. The default score limit (when the game ends) is 20 and the default agent (what's controlling the right paddle) is 'player', but these can easily be adjusted. Additionally, there is the option 'colorid' which when True, colors all computer controlled paddles to red. It is set to False by default.


Example of colorid being set to True

![ezgif com-video-to-gif](https://github.com/atleast3bees/pong/assets/111519324/ebb71117-fa07-4a42-be06-a934b2cc028e)

To add extra agents, add its file to the agents folder. Then, import the class into pong.py and create a new object. This object must be added to the tuple 'agents' first. 

<img width="141" alt="Screenshot 2023-07-24 at 2 15 03 PM" src="https://github.com/atleast3bees/pong/assets/111519324/96f5c28c-69c2-4001-bbbb-5b002c176d65">

<img width="252" alt="Screenshot 2023-07-24 at 2 29 09 PM" src="https://github.com/atleast3bees/pong/assets/111519324/58e8bfa0-6618-45ce-837f-c19070d2392d">

Finally, adjust 'agentlist' to add the name of the new agent. You should be able to use the agent by setting the argument in the .yaml file to whatever you named it.

## Development

This project was developed using PyGame.
