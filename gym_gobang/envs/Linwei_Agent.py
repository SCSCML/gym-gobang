from .Linwei_policy import evaluation,searcher

class Linwei_Agent(searcher):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.isHuman=False
        self.level=2

if __name__=="__main__":
    #Linwei_Agent().search()
    pass
