from maze import Maze,Point, Line, Cell
from window import Window
import random



def main():
    win = Window(800, 600)
    maze = Maze(12,9, win)
    win.wait_for_close()
    

main()