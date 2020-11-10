import numpy as np


class Node:
    # Class attribute
    def __init__(self, state, old_state, weight):
        self.state = state
        self.old_state = old_state
        self.weight = weight


    def isGoal(self):
        if np.array_equal(self.state, np.array([[1,2,3,4], [5,6,7,0]])) or np.array_equal(self.state, np.array([[1,3,5,7], [2,4,6,0]])):
            return True
        else: return False

    def createSuccessors(self):
        #Calculte position
        row = len(self.state)
        col = len(self.state[0])
        for x in range(0, row):
            for y in range(0, col):
                if self.state[x][y] == 0:
                    position = (x,y)
                    break

       #Detect if position is in a corner
        if position == (0,0) or position == (0,col-1) or position == (row-1,0) or position == (row-1,col-1):
            isCorner = True
        else: isCorner = False
        print(position)


# Parse string to get inital state puzzle
initialState = Node(np.array([[3, 0, 1, 4], [2, 6, 5, 7]]), None, 0)

openList = [initialState]
closedList = []

initialState.createSuccessors()

#while True:
