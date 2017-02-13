class Rule:
    name=None
    board_size=0
    hasOpening=False

    @classmethod    
    def opening(cls,step,action):
        pass   
 
    @classmethod
    def getOpeningActions(cls,step):
        pass

    @classmethod    
    def check(cls,board,color):
        """specific color check"""
        raise NotImplementedError

#class Renju(Rule):
#    name="renju"
#    board_size=15
#    #TODO

class Standard(Rule):
    name="standard"
    board_size=15
    hasOpening=False

    @classmethod
    def check(cls,board,color):
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(cls.board_size):
            for j in range(cls.board_size):
                if not board[i][j] == color: continue
                id = board[i][j]
                for d in dirs:
                    x, y = j, i
                    count = 0
                    for k in range(5):
                        if board.get(y, x) != id: break
                        y += d[0]
                        x += d[1]
                        count += 1
                    if count == 5:
                        won = {}
                        r, c = i, j
                        for z in range(5):
                            won[(r, c)] = 1
                            r += d[0]
                            c += d[1]
                        return id,won
        return 0,{}

    

if __name__=="__main__":
    print(Standard.name)
    
