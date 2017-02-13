import gym
import numpy as np
from gym import error, spaces, utils
from .board import Board
from .rule import Standard
from .agent import Human
from .Linwei_Agent import Linwei_Agent as Linwei

class GobangEnv(gym.Env):
    metadata = {'render.modes': ['play','train']} # For now, only 'single' available
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
        self._history=[] # only used for 'play' mode 
        
        self.agents=[agent1,agent2]

        #self.observation_space=spaces.multi_discrete.MultiDiscrete([[0,self.bSize-1],[0,self.bSize-1],[0,2]])
        #self.action_space=spaces.multi_discrete.Discrete(self.bSize**2)

        spaces.prng.seed(seed=np.random.randint(1000000))
    
    def _render(self,mode='single',close=False):
        if close:
            return
        else:
            if mode=='play':
                print('<ROUND %d>'%(len(self._history) + 1))
                self._board.show()
                print('Your move (u:undo, q:quit):',)

    def _reset(self):
        self._board.reset()
        return self._board.obs()


    def _step(self,action):
        """
            return -----------
            
            ob :  2D list, shape = [bSize][bSize]
            done : if not done, then done=0, else 1 or 2 (indicating winner) 
        """
        row,col = action//self.bSize,action%self.bSize  
        try:
            assert self._board[row][col]==0, "cannot move"
        except AssertionError:
            if self.agents[self._color-1].isHuman:
                print("Cannot move!")
                return self._board.obs(), 0, False, {}
            else:
                raise AssertionError()

        self._board[row][col]=self._color

        done = True if self._board.check(self._color) else False
        reward = 1 if done else 0        

        self._nextColor()     

        return self._board.obs(), reward, done, {}

    def _nextColor(self):
        """ switch color"""
        self._color = self._color%2+1       

    def _command(self,command):
        """
            used in 'play' mode
            params ------
            command : 'command' can be string coordinates like 'DA' or can be string command like 'Q' 
        """
        command.strip()
        if command.upper() == 'U':
            self._undo()
            return None
        elif command.upper() == 'Q':
            exit()

        assert len(command) == 2,"please input correct command."
        tr = ord(command[0].upper()) - ord('A')
        tc = ord(command[1].upper()) - ord('A')
        assert tr >= 0 and tc >= 0 and tr < self.bSize and tc < self.bSize, "out of board"
        return tr*self.bSize+tc
    
    def _undo(self):
        if len(self._history)<2:
            print('no history to undo')
        else:
            print('rollback from history...')
            move = self._history.pop()
            self._board.loads(move)
            self._nextColor()
            self._board.won={}
            if not self.agents[self._color-1].isHuman:
                move = self._history.pop()
                self._board.loads(move)
                self._nextColor()

    def _gameover(self):
        """ used in 'play' mode """
        self._board.show()
        print('')
        print('Player {} WIN !!'.format(self._color))
        print("if you want to undo, insert 'u'.")
        print("if not, insert other key")
        if input().upper()=='U':
            self._undo()
            return False
        return True

    def _turn(self,mode):
        """ used in 'play' mode """
        #print(self._history)

        agent = self.agents[self._color-1]
        done = False

        if mode == "play": 
            if agent.isHuman:
                self._render(mode=mode)
                move = agent.getCommand()
                action = self._command(move)
                if action is not None:
                    self._history.append(self._board.dumps())
                    print("Player{}'s move : {}".format(self._color,move))
                    observation,reward,done,info = self.step(action)
                else: # special command like 'q' or 'u'
                    return done
                if done: done=self._gameover()                    
                return done
            else:
                _,row,col = agent.search(2,agent.level)
                print("Player{}(AI)'s move : {}{}".format(self._color,chr(ord('A')+row),chr(ord('A')+col)))
                self._history.append(self._board.dumps())
                observation,reward,done,info=self.step(row*self.bSize+col)
                if done: done=self._gameover()
                return done
        elif mode == "train":   
            pass
        raise NotImplementedError()
 
    def board(self):
        return self._board.board()

    def play(self,playmode='single'):
        if playmode=='single':
            import random
            openid = random.randint(0, len(GobangEnv.opening) - 1)

            self.agents[0]=Human(color=1)
            self.agents[0].board=self._board.board()
            self.agents[1]=Linwei(color=2)
            self.agents[1].board=self._board.board()
            self.reset()
            self._board.loads(GobangEnv.opening[openid]) 
            #self._history.append(self._board.dumps())
            done=False

            while not done:
                done=self._turn(mode='play')
        elif playmode == 'dual':
            self.agents[0]=Human(color=1)
            self.agents[0].board=self._board.board()
            self.agents[1]=Human(color=2)
            self.agents[1].board=self._board.board()
            self.reset()
            done=False
            
            while not done:
                done=self._turn(mode='play')


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--play", help="single or dual")
    args = parser.parse_args()
    env = GobangEnv()
    env.play(mode=args.play)

