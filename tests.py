import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def testMazeCells(self):
        numRows = 12
        numCols = 10
        m1 = Maze(numRows, numCols)
        self.assertEqual(
            len(m1.maze),
            numCols,
        )
        self.assertEqual(
            len(m1.maze[0]),
            numRows,
        )


if __name__ == "__main__":
    unittest.main()