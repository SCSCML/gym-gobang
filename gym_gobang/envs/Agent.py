class Agent:
    def __init__(self,**kwargs):
        self.name="anomynous"
        self.color=1
        self.level=1
        self.score={"win":0,"lost":0,"draw":0}
        self.introduction=""
        self.board=None

        for k,v in kwargs.items():
            setattr(self,k,v)

    def search(self):
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
    def getCommand(self):
        """ gym-gobang original method"""
        return input().strip('\r\n\t ')

