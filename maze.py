from window import Window
import time
import random


class Maze:
    def __init__(self, rows,cols, win = None):
        self.size = 50
        self.win = win
        self.rowLen = rows
        self.colLen = cols

        self.isAnimate = True
        self.timePath = 0.1
        self.timeMap = 0.01

        self.maxNeighborCount = 2


        self.safetyNet = 0 #debug

        self.maze = [[None for _ in range(rows)] for _ in range(cols)]
        #print(self.maze)
        self.ramdomRoute = [(1,0),(-1,0),(0,1),(0,-1)]


        print(f"length; x: {len(self.maze[0])} y: {len(self.maze)}") #debug

        self.createCells()

        self.allPos = self.GetAllPos()
        self.RamdomNise(self.allPos)


        
        self.CreateMazePath()

        self.CavasReset()
        self.breakIntranceOutrance()
        self.ResetVisited()

        #self.breakWalls(4,3,4,2) # debug
        #self.drawcell(4,3)


        #self.maze[self.colLen //2][self.rowLen //2].isVisited = True #debug
        #self.RecurseRamdomMaze(self.rowLen //2, self.colLen //2)

        if(self.win != None):
            self.drawMaze()

        print(self.Solve())


    def createCells(self):
        if(self.win != None):
            (x,y) = self.win.GetWindoSize() 
        else:
            x = 800
            y = 600

        x = x/2 - self.rowLen//2 * self.size 
        y = y/2 - self.colLen//2 * self.size 


        if self.rowLen % 2 == 0:
            x += self.size/2
        if self.colLen % 2 == 0:
            y += self.size/2

        #print(f"x: {x} y: {y}")

        for col in range(self.colLen):
            curX = x
            for row in range(self.rowLen):
                self.maze[col][row] = Cell(curX,y,self.size,self.win)
                curX += self.size
            y += self.size


    #self.ramdomRoute[(1,0),(-1,0),(0,1),(0,-1)] #todo
    def Solve(self):
        self.maze[0][0].isVisited = True
        return self.Solver(0,0)

    #self.ramdomRoute[(1,0),(-1,0),(0,1),(0,-1)] #todo
    def Solver(self, x, y):
            
            print(f"here: {y}/{x}")
            if self.isOutOfBound(x,y):
                return False
            self.drawcellDebug(x,y,0.3)

            i = 0
            cur = self.maze[y][x]
            walls = [cur.hasDownWall, cur.hasUpWall,cur.hasRightWall,cur.hasLeftWall]

            while i < 4:
                b,a = self.ramdomRoute[i] 
                a +=x
                b +=y
                if self.isOutOfBound(a,b) or self.maze[b][a].isVisited:
                    i +=1
                    continue   


                if walls[i]: 
                    i+=1
                    continue
                self.maze[b][a].isVisited = True
                self.maze[y][x].drawToCell(self.maze[b][a])
                if(b == len(self.maze) and a == len(self.maze[0])): return True
                if not (self.Solver(a,b)):
                    self.maze[y][x].drawToCell(self.maze[b][a], True)
                i+=1

            return False
    

    def CreateMazePath(self):
        i = 0
        pathMax = 3

        
        while i < len(self.allPos):
            (x,y) = self.allPos[i]
            if self.maze[y][x].isVisited and self.calcNeighbors(x,y) > self.maxNeighborCount: 
                i+=1
                continue
            #for cell in self.allPos:
            self.maze[y][x].isVisited = True
           
            self.RecurseRamdomMaze(x,y)

            i+=1

    
        
    def RecurseRamdomMaze(self, x, y, prev = random.randint(0,3)):
        #self.safetyNet +=1        #debug
        #if(self.safetyNet > 1000):
           # print("stuck in recusion")
            #return

        num = self.RamdomMove(prev)
        prev = num
        a,b = self.ramdomRoute[num] 
        a +=x
        b+= y

        if self.isOutOfBound(a,b):
            return

        if self.maze[b][a].isVisited:
            if self.calcNeighbors(a,b) < self.maxNeighborCount: 
                self.breakWalls(a,b,x,y)
            #self.drawcell(x,y)    #debug 
            return
        else:
            self.maze[y][x].isVisited = True
       
        self.breakWalls(a,b,x,y)
        #self.drawcell(x,y,self.timePath) #debug

        self.RecurseRamdomMaze(a,b,prev)



    def breakWalls(self,a,b,x,y):
        if a == x:
            if b > y:
                self.maze[b][a].hasUpWall = False;
                self.maze[y][x].hasDownWall = False;
            else:
                self.maze[y][x].hasUpWall = False;
                self.maze[b][a].hasDownWall = False;
        else:
            if a < x:
                self.maze[b][a].hasRightWall = False;
                self.maze[y][x].hasLeftWall = False;
            else:
                self.maze[y][x].hasRightWall = False;
                self.maze[b][a].hasLeftWall = False;


    def calcNeighbors(self, x,y):
        count = 0
        cell = self.maze[y][x]
        if cell.hasLeftWall:
            count += 1
        if cell.hasRightWall:
            count += 1
        if cell.hasUpWall:
            count += 1
        if cell.hasDownWall:
            count += 1

        return 4 - count

    def isOutOfBound(self,x,y):
        return x < 0 or y < 0 or x >= len(self.maze[0]) or y >= len(self.maze)
        
    
    def animate(self,sec):
        self.win.redraw()
        time.sleep(sec)
        
    def breakIntranceOutrance(self):
        self.maze[0][0].hasLeftWall = False
        self.maze[len(self.maze)-1][len(self.maze[0])-1].hasRightWall = False
        #self.drawcell(0,0) #debug
        #self.drawcell(len(self.maze[0])-1,len(self.maze)-1)



    def drawcell(self, x, y, sec = 0):
        if not self.win:
            return
        self.maze[y][x].draw()
        if self.isAnimate:
            self.animate(sec)


    def drawcellDebug(self, x, y, sec = 0): #debug
        if not self.win:
            return
        self.maze[y][x].drawDebug()
        if self.isAnimate:
            self.animate(sec)
    
    
    def RamdomMove(self, prev): # making sure we dont go back
        match prev:
            case 0:
                prev = 1
            case 1:
                prev = 0
            case 2:
                prev = 3
            case 3:
                prev = 2

        num = random.randint(0,3)
        return num if num != prev else 3

    def RamdomNise(self,list):
        lenght = len(list) -1
        i = lenght

        while(i > 0):
            r = random.randint(0,i -1)
            (list[i] , list[r]) = (list[r] , list[i])
            i -= 1

    def GetAllPos(self):
        list = [(None,None)]  * self.colLen * self.rowLen
        x = 0
        for i in range(self.colLen):
            for j in range(self.rowLen):
                list[x] = (j,i)
                x +=1
        return list
    
    def drawMaze(self):
        for col in range(self.colLen):
            for row in range(self.rowLen):
                self.drawcell(row,col,self.timeMap)

    def ResetVisited(self):
        i = 0

        while i < len(self.allPos):
            (x,y) = self.allPos[i]
            self.maze[y][x].isVisited = False
            i+=1

    def CavasReset(self):
        self.win.ClearCanvas()

class Cell:
    def __init__(self, x, y,size, window):
        self.hasLeftWall = True
        self.hasRightWall = True
        self.hasUpWall = True
        self.hasDownWall = True

        self.isVisited = False

        self.win = window
        self.color = "white"
        self.colorD = "yellow"

        self.core = Point(x,y)

        leftUp = Point(x - size/2, y - size/2)
        rightUp = Point(x + size/2, y - size/2)
        leftDown = Point(x - size/2, y + size/2)
        rightDown = Point(x + size/2, y + size/2)

        self.LeftWall = Line(leftUp,leftDown)
        self.RightWall = Line(rightUp, rightDown)
        self.UpWall = Line(leftUp, rightUp)
        self.DownWall = Line(leftDown, rightDown) 


    def draw(self):
        if self.hasLeftWall:
            self.LeftWall.draw(self.win,self.color)
        if self.hasRightWall:
            self.RightWall.draw(self.win,self.color)
        if self.hasUpWall:
            self.UpWall.draw(self.win,self.color)
        if self.hasDownWall:
            self.DownWall.draw(self.win,self.color)

    def drawDebug(self):
        if self.hasLeftWall:
            self.LeftWall.draw(self.win,self.colorD)
        if self.hasRightWall:
            self.RightWall.draw(self.win,self.colorD)
        if self.hasUpWall:
            self.UpWall.draw(self.win,self.colorD)
        if self.hasDownWall:
            self.DownWall.draw(self.win,self.colorD)


    def drawToCell(self, celx, undo=False):
        if(undo):
            Line(self.core,celx.core).draw(self.win, "gray")
        else:
            Line(self.core,celx.core).draw(self.win, "red")



class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class Line:
    def __init__(self, x , y):
        self.pointX = x
        self.pointY = y

    def draw(self, win, fill_color):
        win.drawLine(self.pointX.x,self.pointX.y,self.pointY.x,self.pointY.y, fill_color)
        
