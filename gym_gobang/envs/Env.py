import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
from Board import Board
from Rule import Standard
from Agent import Human
from Linwei_Agent import Linwei_Agent as Linwei

class GobangEnv(gym.Env):
    metadata = {'render.modes': ['single','dual','train']} # For now, only 'single' available
    opening = [
        '1:HH 2:II',
        #'2:IG 2:GI 1:HH',
        '1:IH 2:GI',
        '1:HG 2:HI',
        #'2:HG 2:HI 1:HH',
        #'1:HH 2:IH 2:GI',
        #'1:HH 2:IH 2:HI',
        #'1:HH 2:IH 2:HJ',
        #'1:HG 2:HH 2:HI',
        #'1:GH 2:HH 2:HI',
    ]
    
    def __init__(self,agent1=None,agent2=None,rule=Standard):
        self._board = Board()
        self._color = 1
        self.rule = rule
        self.bSize=rule.board_size
        self.history=[]        

        self.agent1=agent1
        self.agent2=agent2

        #self.observation_space=spaces.multi_discrete.MultiDiscrete([[0,self.bSize-1],[0,self.bSize-1],[0,2]])
        #self.action_space=spaces.multi_discrete.Discrete(self.bSize**2)

        spaces.prng.seed(seed=np.random.randint(1000000))
    
    def _render(self,mode='single',close=False):
        if close:
            return
        else:
            if mode=='single' or mode =='dual':
                print('<ROUND %d>'%(len(self.history) + 1))
                self._board.show()
                print('Your move (u:undo, q:quit):',)

    def _reset(self):
        self._board.reset()
        return self._board.obs()

    def _actionToCoord(self,action):
        """
            params ------
            action : 'action' can be string coordinates like 'DA',
                     can be integer coordinates in action_space,
                    or can be string command like 'Q' 
        """
        if isinstance(action,str):
            action.strip()
            if action.upper() == 'U':
                if len(self.history)==0:
                    print('no history to undo')
                else:
                    print('rollback from history...')
                    move = self.history.pop()
                    done=False
                    self._board.loads(move)
                return None,None
            elif action.upper() == 'Q':
                #print(self._board.dumps())
                exit()
 
            assert len(action) == 2,"please input correct corrdinates."
            tr = ord(action[0].upper()) - ord('A')
            tc = ord(action[1].upper()) - ord('A')
            assert tr >= 0 and tc >= 0 and tr < self.bSize and tc < self.bSize, "out of board"
            return tr, tc
        else:
            return action//self.bSize,action%self.bSize  

    def _step(self,action):
        """
            return -----------
            
            ob : 2D list which has board size square
            done : if not done, then done=0, else 1 or 2 (indicating winner) 
        """
        row,col = self._actionToCoord(action)
        if row is None and col is None:
            return self._board.obs(),0,False,{}
        try:
            assert self._board[row][col]==0, "cannot move"
        except AssertionError:
            print("Cannot move!")
            return self._board.obs(), 0, False, {}

        #self.history.append(self._board.dumps())
        self._board[row][col]=self._color

        done = True if self._board.check(self._color) else False
        reward = 1 if done else 0        

        if done:
            self._board.show()
            #print(self._board.dumps())
            print('')
            print('Player {} WIN !!'.format(self._color))

        # next color
        self._nextColor()     

        return self._board.obs(), reward, done, {}

    def _nextColor(self):
        """ gym-gobang original method"""
        self._color = self._color%2+1       

    def loads(self,info):
        """ gym-gobang original method"""
        self._board.loads(info)

    def board(self):
        return self._board.board()

    @classmethod
    def play(cls,mode='single'):
        if mode=='single':
            import random
            openid = random.randint(0, len(GobangEnv.opening) - 1)

            ge=GobangEnv(agent1=Human(color=1),agent2=Linwei(color=2))
            ge.agent2.board=ge.board()
            ge.reset()
            ge.loads(GobangEnv.opening[openid]) 
            done=False
            DEPTH=2

            while not done:
                ge.render(mode='single')
                observation,reward,done,info = ge.step(ge.agent1.getCommand())
                if done:
                    print("if you want to undo, insert 'u'.")
                    print("if not, insert other key")
                    if input().upper()=='U':
                        ge.step('U')
                        done=False
                _,row,col = ge.agent2.search(2,DEPTH)
                print('Player 2\'s move : ', chr(ord('A'))+row,chr(ord('A')+col))
                observation,reward,done,info=ge.step(row*ge.bSize+col)
        elif mode == 'dual':
            ge=GobangEnv(agent1=Human(color=1),agent2=Human(color=2))
            ge.reset()
            done=False

            while not done:
                ge.render(mode=mode)
                observation,reward,done,info = ge.step(ge.agent1.getCommand())
                if done:
                    print("if you want to undo, insert 'U'.")
                    print("if not, insert other key")
                    if input().upper()=='U':
                        ge.step('U')
                        done=False


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--play", help="single or dual")
    args = parser.parse_args()
    GobangEnv.play(mode=args.play)

