from tkinter import Tk, BOTH, Canvas


class Window:

    def __init__(self,width,height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="black", height=height, width=width)
        self.__canvas.pack()
        self.isRunning = False
       
        self.width = width
        self.height = height

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def GetWindoSize(self):
        return self.width,self.height

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def ClearCanvas(self):
        self.__canvas.delete("all")


    def drawLine(self, x1,x2,y1,y2, fillColor):
         self.__canvas.create_line(x1,x2,y1,y2, fill=fillColor, width=2)



    def wait_for_close(self):
        self.isRunning = True
        while self.isRunning:
            self.redraw()
        print("close window")

    def close(self):
        self.isRunning = False


