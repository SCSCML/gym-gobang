class Agent:
    def __init__(self,board,**kwargs):
        self.name="anomynous"
        self.color=1
        self.level=1
        self.score={"win":0,"lost":0,"draw":0}
        self.introduction=""
        self.board=board
        self.isHuman=None

        for k,v in kwargs.items():
            setattr(self,k,v)

    def search(self):
        """ This method can be modified freely """
        raise NotImplementedError()
    
    def __str__(self):
        result ="""
name : {0}
color : {1}
level : {2}
score : {3}
introduction : {4}
""".format(self.name,self.color,self.level,self.score,self.introduction)
        return result

class Human(Agent):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.isHuman=True
    def getCommand(self):
        return input().strip('\r\n\t ')

