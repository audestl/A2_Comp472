import numpy as np
from operator import attrgetter


class Node:
    # Class attribute
    weight = 0
    def __init__(self, state, old_Node, weight):
        self.state = state
        self.old_Node = old_Node
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

       #1-Create successor for regular move

        leftPos = (position[0], position[1]-1)
        rightPos = (position[0], position[1] + 1)
        bottomPos = (position[0] + 1, position[1])
        topPos = (position[0] - 1, position[1])

        successorList = []
        if leftPos[1] >= 0:
            leftState = np.copy(self.state)
            leftState[leftPos[0]][leftPos[1]], leftState[position[0]][position[1]] = leftState[position[0]][position[1]], leftState[leftPos[0]][leftPos[1]]
            leftNode = Node(leftState, self, self.weight + 1)
            successorList.append(leftNode)

        if rightPos[1] <= col-1:
            rightState = np.copy(self.state)
            rightState[rightPos[0]][rightPos[1]], rightState[position[0]][position[1]] = \
            rightState[position[0]][position[1]], rightState[rightPos[0]][rightPos[1]]
            rightNode = Node(rightState, self, self.weight + 1)
            successorList.append(rightNode)

        if bottomPos[0] <= row-1:
            botState = np.copy(self.state)
            botState[bottomPos[0]][bottomPos[1]], botState[position[0]][position[1]] = \
            botState[position[0]][position[1]], botState[bottomPos[0]][bottomPos[1]]
            bottomNode = Node(botState, self, self.weight + 1)
            successorList.append(bottomNode)

        if topPos[0] >= 0:
            topState = np.copy(self.state)
            topState[topPos[0]][topPos[1]], topState[position[0]][position[1]] = \
            topState[position[0]][position[1]], topState[topPos[0]][topPos[1]]
            topNode = Node(topState, self, self.weight + 1)
            successorList.append(topNode)

        if isCorner:
            # Create Wrapping moves
            if position[1] == col-1:
                wrapLeftState = np.copy(self.state)
                wrapLeftState[position[0]][0], wrapLeftState[position[0]][position[1]] = \
                    wrapLeftState[position[0]][position[1]], wrapLeftState[position[0]][0]
                wrapLeftNode = Node(wrapLeftState, self, self.weight + 2)
                alreadyExists = False
                for successorNode in successorList:
                    if np.array_equal(wrapLeftNode.state, successorNode.state):
                        alreadyExists = True
                if not alreadyExists:
                    successorList.append(wrapLeftNode)

            elif position[1] == 0:
                wrapRightState = np.copy(self.state)
                wrapRightState[position[0]][col-1], wrapRightState[position[0]][position[1]] = \
                    wrapRightState[position[0]][position[1]], wrapRightState[position[0]][col-1]
                wrapRightNode = Node(wrapRightState, self, self.weight + 2)
                alreadyExists = False
                for successorNode in successorList:
                    if np.array_equal(wrapRightNode.state, successorNode.state):
                        alreadyExists = True
                if not alreadyExists:
                    successorList.append(wrapRightNode)

            if position[0] == row-1:
                wrapTopState = np.copy(self.state)
                wrapTopState[0][position[1]], wrapTopState[position[0]][position[1]] = \
                    wrapTopState[position[0]][position[1]], wrapTopState[0][position[1]]
                wrapTopNode = Node(wrapTopState, self, self.weight + 2)
                alreadyExists = False
                for successorNode in successorList:
                    if np.array_equal(wrapTopNode.state, successorNode.state):
                        alreadyExists = True
                if not alreadyExists:
                    successorList.append(wrapTopNode)

            elif position[0] == 0:
                wrapBottomState = np.copy(self.state)
                wrapBottomState[row - 1][position[1]], wrapBottomState[position[0]][position[1]] = \
                    wrapBottomState[position[0]][position[1]], wrapBottomState[row -1 ][position[1]]
                wrapBottomNode = Node(wrapBottomState, self, self.weight + 2)
                alreadyExists = False
                for successorNode in successorList:
                    if np.array_equal(wrapBottomNode.state, successorNode.state):
                        alreadyExists = True
                if not alreadyExists:
                    successorList.append(wrapBottomNode)

            # Create Diagonal moves
            if position == (0, 0):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[row-1][col-1], oppositeCornerState[0][0] = \
                oppositeCornerState[0][0], oppositeCornerState[row-1][col-1]
                oppositeCornerNode = Node(oppositeCornerState, self, self.weight + 3)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[1][1], diagonalState[0][0] = \
                    diagonalState[0][0], diagonalState[1][1]
                diagonalNode = Node(diagonalState, self, self.weight + 3)
                successorList.append(diagonalNode)
            elif position == (0, col-1):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[row - 1][0], oppositeCornerState[0][col-1] = \
                    oppositeCornerState[0][col-1], oppositeCornerState[row - 1][0]
                oppositeCornerNode = Node(oppositeCornerState, self, self.weight + 3)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[1][col-2], diagonalState[0][col-1] = \
                    diagonalState[0][col-1], diagonalState[1][col-2]
                diagonalNode = Node(diagonalState, self, self.weight + 3)
                successorList.append(diagonalNode)
            elif position == (row-1, 0):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[0][col - 1], oppositeCornerState[row-1][0] = \
                    oppositeCornerState[row-1][0], oppositeCornerState[0][col - 1]
                oppositeCornerNode = Node(oppositeCornerState, self, self.weight + 3)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[row-2][1], diagonalState[row-1][0] = \
                    diagonalState[row-1][0], diagonalState[row-2][1]
                diagonalNode = Node(diagonalState, self, self.weight + 3)
                successorList.append(diagonalNode)
            elif position == (row-1, col-1):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[row - 1][col - 1], oppositeCornerState[0][0] = \
                    oppositeCornerState[0][0], oppositeCornerState[row - 1][col - 1]
                oppositeCornerNode = Node(oppositeCornerState, self, self.weight + 3)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[row-2][col-2], diagonalState[row-1][col-1] = \
                    diagonalState[row-1][col-1], diagonalState[row-2][col-2]
                diagonalNode = Node(diagonalState, self, self.weight + 3)
                successorList.append(diagonalNode)

        return successorList



# Parse string to get inital state puzzle
initialState = Node(np.array([[1, 6, 3, 4], [0, 2, 7, 5]]), None, 0)

openList = [initialState]
closedList = []

while True:
    # Check if first Node is the goal
    if openList[0].isGoal():
        print("Solution found, Total cost: ", openList[0].weight)
        break

    # Pop the visited node and add to closed list
    visitedNode = openList.pop(0)
    closedList.append(visitedNode)

    #Create successor
    newSuccessorList = visitedNode.createSuccessors()
    for successorNode in newSuccessorList:
        for openNode in openList:
            if np.array_equal(successorNode.state, openNode.state) and successorNode.weight < openNode.weight:
                openList.remove(openNode)
        alreadyExists = False
        for closedNode in closedList:
            if np.array_equal(successorNode.state, closedNode.state):
                alreadyExists = True
        if not alreadyExists:
            openList.append(successorNode)

    # Sort open list by weight
    openList.sort(key=attrgetter('weight'))



