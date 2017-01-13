import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
#from gym_gobang.envs.gobang import chessboard as cb 
from gobang import chessboard as cb 

class GobangEnv(gym.Env):
    metadata = {'render.modes': ['play','train']} # For now, only 'play' available
    def __init__(self,bSize=15,gobangAI=None):
        self._cb = cb()
        self._color = 1
        self.bSize=bSize
        self.history=[]        

        self.gobangAI=gobangAI
        if self.gobangAI is None and self.bSize == 15 :
            from Linwei_policy import searcher
            self.gobangAI = searcher()
            self.gobangAI.board=self._cb.board()

        self.observation_space=spaces.multi_discrete.MultiDiscrete([[0,bSize-1],[0,bSize-1],[0,2]])
        self.action_space=spaces.multi_discrete.Discrete(bSize**2)

        spaces.prng.seed(seed=np.random.randint(1000000))
    
    def _render(self,mode='play',close=False):
        if close:
            return
        else:
            if mode=='play':
                print('<ROUND %d>'%(len(self.history) + 1))
                self._cb.show()
                print('Your move (u:undo, q:quit):',)

    
    def _reset(self):
        self._cb.reset()
        return self._cb.obs


    def _actionToCoord(self,action):
        """
            params ------
            action : 'action' can be string coordinates like 'DA',
                     can be integer coordinates in action_space,
                    or can be string command like 'Q' 
        """
        action.strip()
        if isinstance(action,str):
            if action.upper() == 'U':
                if len(self.history)==0:
                    print('no history to undo')
                else:
                    print('rollback from history...')
                    move = self.history.pop()
                    self._cb.loads(move)
                return None,None
            elif action.upper() == 'Q':
                print(self._cb.dumps())
                exit()
 
            assert len(action) == 2,"please input correct corrdinates."
            tr = ord(action[0].upper()) - ord('A')
            tc = ord(action[1].upper()) - ord('A')
            assert tr >= 0 and tc >= 0 and tr < self.bSize and tc < self.bSize, "out of board"
            return tr, tc
                
        else:
            return action%self.bSize,action//self.bSize  

    def _step(self,action,mode='play'):
        """
            return -----------
            
            ob : 2D list which has board size square
            done : if not done, then done=0, else 1 or 2 (indicating winner) 
        """
        row,col = self._actionToCoord(action)
        if row is None and col is None:
            return self._cb.obs,0,False,{}
        assert self._cb[row][col]==0, "cannot move"
        self.history.append(self._cb.dumps())
        self._cb[row][col]=self._color

        done = True if self._cb.check() else False
        reward = 1 if done else 0        
        self._nextColor()     

        if done:
            self._cb.show()
            print(self._cb.dumps())
            print('')
            print('YOU WIN !!')
        elif mode=='play':
            print('robot is thinking now...')
            _,row,col = self.gobangAI.search(2,1)# second is depth    
            cord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))
            print('robot move to %s'%(cord))
            self._cb[row][col] = self._color
            self._nextColor()

            if self._cb.check() == 2:
                self._cb.show()
                print(self._cb.dumps())
                print('')
                print('YOU LOSE.')
                done = True
                reward = -1

        return self._cb.obs, reward, done, {}

    def _nextColor(self):
        """ gym-gobang original method"""
        self._color = self._color%2+1       
    
    def getCommand(self):
        """ gym-gobang original method"""
        return input().strip('\r\n\t ')

    def loads(self,info):
        """ gym-gobang original method"""
        self._cb.loads(info)

if __name__=="__main__":
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

    import random
    openid = random.randint(0, len(opening) - 1)

    ge=GobangEnv()
    ge.reset()
    ge.loads(opening[openid]) 
    done=False

    while not done:
        ge.render(mode='play')
        observation,reward,done,info = ge.step(input())
        if done:
            print("if you want to undo, insert 'u'.")
            print("if not, insert other key")
            if input()=='u':
                ge.step(u)
                done=False

    #print(ge.observation_space.sample())
    #print(ge.action_space.sample())
