import random
import os
import time
import msvcrt

class Snake:
    def __init__(self, n):
        self.length = n
        self.head = []
        self.tail = []

class SnakeGame:
    direction = {"LEFT":-2, "DOWN":-1, "NON_DIR":0, "UP":1, "RIGHT":2}
    sprite = {"EMPTY":0, "BODY":1, "HEAD":2, "FOOD":3}
    element = {"SPRITE":0, "DIRECTION":1}
    
    def __init__(self, w, h, length, delay):
        self.W = w
        self.H = h
        self.initLen = length
        self.snake = Snake(length)
        self.delay = delay  
        self.board = [[[0]*2 for x in range(self.W)] for y in range(self.H)]
        #self.board[a][b][c]

        self.snake.head = [self.H//2, self.snake.length-1]
        self.snake.tail = [self.H//2, 0]

        for i in range(0, self.snake.length):
            self.board[self.H//2][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
            self.board[self.H//2][i][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        self.board[self.H//2][self.snake.length-1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]#element->sprite=2
        self.board[self.H//2][self.snake.length-1][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]#element->direction=2

        
        x = random.randint(0, self.W-1)
        y = random.randint(0, self.H-1)
        while self.board[y][x][SnakeGame.element["SPRITE"]]\
              != SnakeGame.sprite["EMPTY"]:
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)

        self.board[y][x][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]

    def DrawScene(self):
        os.system('cls||clear')
        for x in range(0, self.W+2):
            print("=", end="")
        print("")
        for y in range(0, self.H):
            print("|", end="")
            for x in range(0, self.W):
                if self.board[y][x][SnakeGame.element["SPRITE"]]\
                   == SnakeGame.sprite["BODY"]:
                    print("+", end="")
                elif  self.board[y][x][SnakeGame.element["SPRITE"]]\
                     == SnakeGame.sprite["HEAD"]:
                    print("@", end="")
                elif  self.board[y][x][SnakeGame.element["SPRITE"]]\
                     == SnakeGame.sprite["FOOD"]:
                    print("*", end="")
                else:
                    print(" ", end="")
            print("|")

        for x in range(0, self.W+2):
            print("=", end="")
        print("")
                

    @staticmethod
    def GetDirection():
        rtn = SnakeGame.direction["NON_DIR"]
        msvcrt.getch()
        ch = msvcrt.getch().decode()
        
        if ch == chr(72):
            print("UP")
            rtn = SnakeGame.direction["UP"]
        elif ch == chr(75):
            print("LEFT")
            rtn = SnakeGame.direction["LEFT"]
        elif ch == chr(77):
            print("RIGHT")
            rtn = SnakeGame.direction["RIGHT"]
        elif ch == chr(80):
            print("DOWN")
            rtn = SnakeGame.direction["DOWN"]

        return rtn

    def GameLoop(self):
        self.DrawScene()

        current = SnakeGame.direction["RIGHT"]
        ret = SnakeGame.direction["RIGHT"]
        
        while True:
            start = time.time()
            while (time.time() - start) <= self.delay/1000:
                if msvcrt.kbhit():
                    current = SnakeGame.GetDirection()
                    
                    #진행방향과 반대 방향으로 조작할때 처리
                    if  current==SnakeGame.direction["RIGHT"] and ret ==SnakeGame.direction["LEFT"]:
                        current = SnakeGame.direction["NON_DIR"]
                    elif current==SnakeGame.direction["LEFT"] and ret ==SnakeGame.direction["RIGHT"]:
                        current = SnakeGame.direction["NON_DIR"]
                    elif current==SnakeGame.direction["UP"] and ret ==SnakeGame.direction["DOWN"]:
                        current = SnakeGame.direction["NON_DIR"]
                    elif current==SnakeGame.direction["DOWN"] and ret ==SnakeGame.direction["UP"]:
                        current = SnakeGame.direction["NON_DIR"]
                    else:
                        ret = current
                    if current == SnakeGame.direction["NON_DIR"]:
                        continue
                    #왼쪽으로 움직일때 처리
                    elif ret == SnakeGame.direction["LEFT"]:
                        #벽에 안 닿았을때 처리
                        #머리 정보 업데이트
                        if self.snake.head[1]-1>=0:
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["LEFT"]
                            self.snake.head[1] = self.snake.head[1]-1
                            #먹이를 먹어 길어질때 처리
                            if self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
                                self.snake.length = self.snake.length+1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["LEFT"]
                                i = random.randint(0, self.W-1)
                                j = random.randint(0, self.H-1)
                                #먹이 재생성
                                while self.board[j][i][SnakeGame.element["SPRITE"]]\
                                    != SnakeGame.sprite["EMPTY"]:
                                    i = random.randint(0, self.W-1)
                                    j = random.randint(0, self.H-1)
                                self.board[j][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]
                            #몸에 닿았을때 처리
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
                                self.snake.head[1] = self.snake.head[1]+1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                ret = SnakeGame.direction["NON_DIR"]
                                print("Game Over")
                                return 0
                            #꼬리 정보 업데이트
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["EMPTY"]:
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["LEFT"]
                                if self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["RIGHT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]+1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["LEFT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["UP"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["DOWN"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]+1
                        #벽에 닿았을때 처리
                        else:
                            print("Game Over")
                            return 0
                    #오른쪽으로 조작할때 처리
                    elif ret == SnakeGame.direction["RIGHT"]:
                        if self.snake.head[1]+1<self.W:
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]
                            self.snake.head[1] = self.snake.head[1]+1
                            if self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
                                self.snake.length = self.snake.length+1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]
                                i = random.randint(0, self.W-1)
                                j = random.randint(0, self.H-1)
                                while self.board[j][i][SnakeGame.element["SPRITE"]]\
                                    != SnakeGame.sprite["EMPTY"]:
                                    i = random.randint(0, self.W-1)
                                    j = random.randint(0, self.H-1)
                                self.board[j][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
                                self.snake.head[1] = self.snake.head[1]-1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                ret = SnakeGame.direction["NON_DIR"]
                                print("Game Over")
                                return 0
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["EMPTY"]:
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]
                                if self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["RIGHT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]+1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["LEFT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["UP"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["DOWN"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]+1
                        else:
                            print("Game Over")
                            return 0
                    #위로 조작할때 처리
                    elif ret == SnakeGame.direction["UP"]:
                        if self.snake.head[0]-1>=0:
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["UP"]
                            self.snake.head[0] = self.snake.head[0]-1
                            if self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
                                self.snake.length = self.snake.length+1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["UP"]
                                i = random.randint(0, self.W-1)
                                j = random.randint(0, self.H-1)
                                while self.board[j][i][SnakeGame.element["SPRITE"]]\
                                    != SnakeGame.sprite["EMPTY"]:
                                    i = random.randint(0, self.W-1)
                                    j = random.randint(0, self.H-1)
                                self.board[j][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
                                self.snake.head[0] = self.snake.head[0]+1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                ret = SnakeGame.direction["NON_DIR"]
                                print("Game Over")
                                return 0
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["EMPTY"]:
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["UP"]
                                if self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["RIGHT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]+1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["LEFT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["UP"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["DOWN"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]+1
                        else:
                            print("Game Over")
                            return 0
                    #아래로 조작할때 처리
                    elif ret == SnakeGame.direction["DOWN"]:
                        if self.snake.head[0]+1<self.H:
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
                            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["DOWN"]
                            self.snake.head[0] = self.snake.head[0]+1
                            if self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
                                self.snake.length = self.snake.length+1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["DOWN"]
                                i = random.randint(0, self.W-1)
                                j = random.randint(0, self.H-1)
                                while self.board[j][i][SnakeGame.element["SPRITE"]]\
                                    != SnakeGame.sprite["EMPTY"]:
                                    i = random.randint(0, self.W-1)
                                    j = random.randint(0, self.H-1)
                                self.board[j][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
                                self.snake.head[0] = self.snake.head[0]-1
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                ret = SnakeGame.direction["NON_DIR"]
                                print("Game Over")
                                return 0
                            elif self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["EMPTY"]:
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
                                self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["DOWN"]
                                if self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["RIGHT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]+1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["LEFT"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[1] = self.snake.tail[1]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["UP"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]-1
                                elif self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] == SnakeGame.direction["DOWN"]:
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                                    self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["NON_DIR"]
                                    self.snake.tail[0] = self.snake.tail[0]+1
                        else:
                            print("Game Over")
                            return 0
                    else:
                        continue
            self.DrawScene()
            print("Score: {}".format(self.snake.length - self.initLen))

if __name__ == '__main__' :
    game = SnakeGame(60, 24, 4, 300)
    game.GameLoop()
