import numpy as np
from operator import attrgetter


class Node:
    # Class attribute
    weight = 0
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

       #1-Create successor for first move

        leftPos = (position[0], position[1]-1)
        rightPos = (position[0], position[1] + 1)
        bottomPos = (position[0] + 1, position[1])
        topPos = (position[0] - 1, position[1])

        # initialState.state[0][0], initialState.state[pos[0]][pos[1]] = initialState.state[pos[0]][pos[1]], initialState.state[0][0]
        # leftNode = Node()

        if leftPos[1]>=0:
            tempState = np.array.copy(self.state)
            tempState.state[leftPos[0]][leftPos[1]], tempState.state[position[0]][position[1]] = tempState.state[position[0]][position[1]],tempState.state[leftPos[0]][leftPos[1]]
            leftNode = Node()
        if rightPos[1] <= col:
            #
        if bottomPos[0] <=row:
            #
        if topPos[0] >= 0:
            #








        #2 Add successors to openList


# Parse string to get inital state puzzle
initialState = Node(np.array([[3, 0, 1, 4], [2, 6, 5, 7]]), None, 0)

openList = [initialState, initialState1, initialState2]
closedList = []

initialState.createSuccessors()

#while True:
#Sort open list by weight
openList.sort(key=attrgetter('weight'))

#Create successor
openList[0].createSuccessors()

#Pop the visited node and add to closed list

#Check if first Node is the goal
if openList[0].isGoal():
    print("Solution found")

