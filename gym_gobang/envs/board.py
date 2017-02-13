from .rule import Standard
import string,sys,copy


class Board:
    def __init__(self,rule=Standard):
        self.rule = rule
        self.board_size=self.rule.board_size
        self.__board = [ [ 0 for n in range(self.board_size) ] for m in range(self.board_size) ]
        #self.__dirs = ( (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), \
        #self.DIRS = self.__dirs
        self.won = {}

        self.text ="  "+" ".join(string.ascii_uppercase[:self.board_size])+"\n"

        self.reset()

    def check(self,color):
        color,won = self.rule.check(self,color)
        self.won=won
        return color

    def reset (self):
        for j in range(self.board_size):
            for i in range(self.board_size):
                self.__board[i][j] = 0

    def __getitem__(self,index):
        return self.__board[index]

    def __str__ (self):
        text = self.text
        mark = ('. ', 'O ', 'X ')
        nrow = 0
        for row in self.__board:
            line = ''.join([ mark[n] for n in row ])
            text += chr(ord('A') + nrow) + ' ' + line
            nrow += 1
            if nrow < self.board_size: text += '\n'
        return text

    def __repr__ (self):
        return self.__str__()
    
    def get (self, row, col):
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return 0
        return self.__board[row][col]

    def put (self, row, col, x):
        if row >= 0 and row < self.board_size and col >= 0 and col < self.board_size:
            self.__board[row][col] = x
        return 0
    
    def board (self):
        return self.__board
    
    def obs(self):
        return copy.deepcopy(self.__board)
    
    def dumps (self):
        try: from StringIO import StringIO
        except ImportError: from io import StringIO
        sio = StringIO()
        board = self.__board
        for i in range(self.board_size):
            for j in range(self.board_size):
                stone = board[i][j]
                if stone != 0:
                    ti = chr(ord('A') + i)
                    tj = chr(ord('A') + j)
                    sio.write('%d:%s%s '%(stone, ti, tj))
        return sio.getvalue()
    
    def loads (self, text):
        self.reset()
        board = self.__board
        for item in text.strip('\r\n\t ').replace(',', ' ').split(' '):
            n = item.strip('\r\n\t ')
            if not n: continue
            n = n.split(':')
            stone = int(n[0])
            i = ord(n[1][0].upper()) - ord('A')
            j = ord(n[1][1].upper()) - ord('A')
            board[i][j] = stone
        return 0

    def console (self, color):
        if sys.platform[:3] == 'win':
            try: import ctypes
            except: return 0
            kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')
            GetStdHandle = kernel32.GetStdHandle
            SetConsoleTextAttribute = kernel32.SetConsoleTextAttribute
            GetStdHandle.argtypes = [ ctypes.c_uint32 ]
            GetStdHandle.restype = ctypes.c_size_t
            SetConsoleTextAttribute.argtypes = [ ctypes.c_size_t, ctypes.c_uint16 ]
            SetConsoleTextAttribute.restype = ctypes.c_long
            handle = GetStdHandle(0xfffffff5)
            if color < 0: color = 7
            result = 0
            if (color & 1): result |= 4
            if (color & 2): result |= 2
            if (color & 4): result |= 1
            if (color & 8): result |= 8
            if (color & 16): result |= 64
            if (color & 32): result |= 32
            if (color & 64): result |= 16
            if (color & 128): result |= 128
            SetConsoleTextAttribute(handle, result)
        else:
            if color >= 0:
                foreground = color & 7
                background = (color >> 4) & 7
                bold = color & 8
                sys.stdout.write(" \033[%s3%d;4%dm"%(bold and "01;" or "", foreground, background))
                sys.stdout.flush()
            else:
                sys.stdout.write(" \033[0m")
                sys.stdout.flush()
        return 0
     
    def show (self):
        print(self.text[:-1])
        mark = ('. ', 'O ', 'X ')
        nrow = 0
        color1 = 10
        color2 = 13
        for row in range(self.board_size):
            print(chr(ord('A') + row),end="")
            for col in range(self.board_size):
                ch = self.__board[row][col]
                if ch == 0: 
                    self.console(-1)
                    print('.',end="")
                elif ch == 1:
                    if (row, col) in self.won:
                        self.console(9)
                    else:
                        self.console(10)
                    print('O',end="")
                    #self.console(-1)
                elif ch == 2:
                    if (row, col) in self.won:
                        self.console(9)
                    else:
                        self.console(13)
                    print('X',end="")
                    #self.console(-1)
            self.console(-1)
            print('')
        return 0




if __name__=="__main__":
    board = Board()
    board.put(1,2,1)
    #print(board)
    board.show()
    d=board.dumps()
    board.check(1) 
