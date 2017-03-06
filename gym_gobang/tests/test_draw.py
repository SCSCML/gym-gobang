import gym
import gym_gobang
from gym_gobang.envs.agent import Agent
from itertools import cycle

class SampleAgent(Agent):
    def __init__(self,policy,**kwargs):
        super().__init__(**kwargs)
        self._policy=policy(self.board)

    def search(self):
        """ generator as policy """
        return next(self._policy)

def policy1(board):
    for i in range(len(board)):
        if i//2%2==0:
            for j in range(0,len(board),2):
                yield i*len(board)+j
        else:
            for j in range(1,len(board),2):
                yield i*len(board)+j
            

def policy2(board):
    for i in range(len(board)):
        if i//2%2==1:
            for j in range(0,len(board),2):
                yield i*len(board)+j
        else:
            for j in range(1,len(board),2):
                yield i*len(board)+j

def play(): 
    env = gym.make('Gobang-v0')
    env.agents=[
                SampleAgent(policy=policy1,board=env.board(),color=1),
                SampleAgent(policy=policy2,board=env.board(),color=2),
                ]
    env.reset()

    done=False
    for player in cycle(env.agents):
        action = player.search()
        obs,reward,done,info = env.step(action)
        if done:
            env.render(mode='train')
            break 

if __name__=="__main__":
    play()
