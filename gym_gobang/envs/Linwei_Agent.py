from .Linwei_policy import evaluation,searcher

class Linwei_Agent(searcher):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.isHuman=False
        self.level=2

    def search (self):
        _,row,col = super().search(self.color, depth=1)
        return row * self.board.board_size + col


if __name__=="__main__":
    #Linwei_Agent().search()
    pass
