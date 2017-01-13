#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from builtins import range,input
from Linwei_policy import *
import sys, time,copy


class chessboard (object):
    """
        gobang board for playing
        boardsize : 15 by 15
    """
    def __init__ (self, forbidden = 0,env=None):
        self.__board = [ [ 0 for n in range(15) ] for m in range(15) ]
        self.__forbidden = forbidden
        self.__dirs = ( (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), \
            (1, -1), (0, -1), (-1, -1) )
        self.DIRS = self.__dirs
        self.won = {}
    
    def reset (self):
        for j in range(15):
            for i in range(15):
                self.__board[i][j] = 0
        return 0
    
    def __getitem__ (self, row):
        return self.__board[row]

    def __str__ (self):
        text = '  A B C D E F G H I J K L M N O\n'
        mark = ('. ', 'O ', 'X ')
        nrow = 0
        for row in self.__board:
            line = ''.join([ mark[n] for n in row ])
            text += chr(ord('A') + nrow) + ' ' + line
            nrow += 1
            if nrow < 15: text += '\n'
        return text
    
    def __repr__ (self):
        return self.__str__()

    def get (self, row, col):
        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return 0
        return self.__board[row][col]

    def put (self, row, col, x):
        if row >= 0 and row < 15 and col >= 0 and col < 15:
            self.__board[row][col] = x
        return 0
    
    def board(self):
        return self.__board

    def check (self):
        board = self.__board
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0: continue
                id = board[i][j]
                for d in dirs:
                    x, y = j, i
                    count = 0
                    for k in range(5):
                        if self.get(y, x) != id: break
                        y += d[0]
                        x += d[1]
                        count += 1
                    if count == 5:
                        self.won = {}
                        r, c = i, j
                        for z in range(5):
                            self.won[(r, c)] = 1
                            r += d[0]
                            c += d[1]
                        return id
        return 0
    
    def board (self):
        return self.__board

    @property
    def obs(self):
        return copy.deepcopy(self.__board)
    
    def dumps (self):
        try: from StringIO import StringIO
        except ImportError: from io import StringIO
        sio = StringIO()
        board = self.__board
        for i in range(15):
            for j in range(15):
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
        print('  A B C D E F G H I J K L M N O')
        mark = ('. ', 'O ', 'X ')
        nrow = 0
        self.check()
        color1 = 10
        color2 = 13
        for row in range(15):
            print(chr(ord('A') + row),end="")
            for col in range(15):
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



#----------------------------------------------------------------------
# psyco speedup
#----------------------------------------------------------------------
def psyco_speedup ():
    try:
        import psyco
        psyco.bind(chessboard)
        psyco.bind(evaluation)
    except:
        pass
    return 0

psyco_speedup()


#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
def gamemain():
    b = chessboard()
    s = searcher()
    s.board = b.board()

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
    b.loads(opening[openid])
    turn = 2
    history = []
    undo = False

    # ÉèÖÃÄÑ¶È
    DEPTH = 1

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'hard':
            DEPTH = 2

    while 1:
        print('')
        while 1:
            print('<ROUND %d>'%(len(history) + 1))
            b.show()
            print('Your move (u:undo, q:quit):',)
            text = input().strip('\r\n\t ')
            if len(text) == 2:
                tr = ord(text[0].upper()) - ord('A')
                tc = ord(text[1].upper()) - ord('A')
                if tr >= 0 and tc >= 0 and tr < 15 and tc < 15:
                    if b[tr][tc] == 0:
                        row, col = tr, tc
                        break
                    else:
                        print('can not move there')
                else:
                    print('bad position')
            elif text.upper() == 'U':
                undo = True
                break
            elif text.upper() == 'Q':
                print(b.dumps())
                return 0
        
        if undo == True:
            undo = False
            if len(history) == 0:
                print('no history to undo')
            else:
                print('rollback from history ...')
                move = history.pop()
                b.loads(move)
        else:
            history.append(b.dumps())
            b[row][col] = 1

            if b.check() == 1:
                b.show()
                print(b.dumps())
                print('')
                print('YOU WIN !!')
                return 0

            print('robot is thinking now ...')
            score, row, col = s.search(2, DEPTH)
            cord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))
            print('robot move to %s (%d)'%(cord, score))
            b[row][col] = 2

            if b.check() == 2:
                b.show()
                print(b.dumps())
                print('')
                print('YOU LOSE.')
                return 0

    return 0


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        b = chessboard()
        b[10][10] = 1
        b[11][11] = 2
        for i in range(4):
            b[5 + i][2 + i] = 2
        for i in range(4):
            b[7 - 0][3 + i] = 2
        print(b)
        print('check', b.check())
        return 0
    def test2():
        b = chessboard()
        b[7][7] = 1
        b[8][8] = 2
        b[7][9] = 1
        eva = evaluation()
        for l in eva.POS: print(l)
        return 0
    def test3():
        e = evaluation()
        line = [ 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]
        record = []
        e.analysis_line(line, record, len(line), 6)
        print(record[:10])
        return 0
    def test4():
        b = chessboard()
        b.loads('2:DF 1:EG 2:FG 1:FH 2:FJ 2:GG 1:GH 1:GI 2:HG 1:HH 1:IG 2:IH 1:JF 2:JI 1:KE')
        b.loads('2:CE 2:CK 1:DF 1:DK 2:DL 1:EG 1:EI 1:EK 2:FG 1:FH 1:FI 1:FJ 1:FK 2:FL 1:GD 2:GE 2:GF 2:GG 2:GH 1:GI 1:GK 2:HG 1:HH 2:HJ 2:HK 2:IG 1:JG 2:AA')
        eva = evaluation()
        print(b)
        score = 0
        t = time.time()
        for i in range(10000):
            score = eva.evaluate(b.board(), 2)
        #eva.test(b.board())
        t = time.time() - t
        print(score, t)
        print(eva.textrec(3))
        return 0
    def test5():
        import profile
        profile.run("test4()", "prof.txt")
        import pstats
        p = pstats.Stats("prof.txt")
        p.sort_stats("time").print_stats()
    def test6():
        b = chessboard()
        b.loads('1:CJ 2:DJ 1:dk 1:DL 1:EH 1:EI 2:EJ 2:EK 2:FH 2:FI 2:FJ 1:FK 2:FL 1:FM 2:GF 1:GG 2:GH 2:GI 2:GJ 1:GK 1:GL 2:GM 1:HE 2:HF 2:HG 2:HH 2:HI 1:HJ 2:HK 2:HL 1:IF 1:IG 1:IH 2:II 1:IJ 2:IL 2:JG 1:JH 1:JI 1:JJ 1:JK 2:JL 1:JM 1:KI 2:KJ 1:KL 1:LJ 2:MK')
        #b.loads('1:HH,1:HI,1:HJ,1:HK')
        s = searcher()
        s.board = b.board()
        t = time.time()
        score, row, col = s.search(2, 3)
        t = time.time() - t
        b[row][col] = 2
        print(b)
        print(score, t)
        print(chr(ord('A') + row) + chr(ord('A') + col))
    def test7():
        b = chessboard()
        s = searcher()
        s.board = b.board()
        b.loads('2:HH 1:JF')
        turn = 2
        while 1:
            score, row, col = s.search(2, 2)
            print('robot move %s%s (%d)'%(chr(ord('A') + row), chr(ord('A') + col), score))
            b[row][col] = 2
            if b.check() == 2:
                print(b)
                print(b.dumps())
                print('you lose !!')
                return 0
            while 1:
                print(b)
                print('your move (pos):',)
                text = input().strip('\r\n\t ')
                if len(text) == 2:
                    tr = ord(text[0].upper()) - ord('A')
                    tc = ord(text[1].upper()) - ord('A')
                    if tr >= 0 and tc >= 0 and tr < 15 and tc < 15:
                        if b[tr][tc] == 0:
                            row, col = tr, tc
                            break
                        else:
                            print('can not move there')
                    else:
                        print('bad position')
                elif text.upper() == 'Q':
                    print(b.dumps())
                    return 0
            b[row][col] = 1
            if b.check() == 1:
                print(b)
                print(b.dumps())
                print('you win !!')
                return 0
        return 0
    #test6()
    gamemain()



