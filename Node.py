import math

import numpy as np
from operator import attrgetter

#CHANGE THESE IF YOUR DIMENSION CHANGED
global goalState1
global goalState2
goalState1 = np.array([[1,2,3,4], [5,6,7,0]])
goalState2 = np.array([[1,3,5,7], [2,4,6,0]])

class Node:
    # Class attribute
    weight = 0
    # Constructor that changes which heuristic it uses
    def __init__(self, state, old_Node, tileMoved, moveCost, Gn, heuristic):
        self.state = state
        self.old_Node = old_Node
        self.tileMoved = tileMoved
        self.moveCost = moveCost
        self.weight = Gn
        if isinstance(heuristic,int):
            self.Hn = heuristic
        elif heuristic == "Hamming":
            self.Hn = self.computeHammingDistance()
        elif heuristic == "Permutation":
            self.Hn = self.computeManhattan()
        self.Fn = self.weight + self.Hn

    def computeHammingDistance(self):
        hammingTotal1 = 0
        hammingTotal2 = 0
        for row in self.state:
            for number in row:
                actualPosition = np.argwhere(self.state == number)[0]
                goalPosition1 = np.argwhere(goalState1 == number)[0]
                goalPosition2 = np.argwhere(goalState2 == number)[0]
                if not np.array_equal(actualPosition, goalPosition1):
                    hammingTotal1 += 1
                if not np.array_equal(actualPosition, goalPosition2):
                    hammingTotal2 += 1

        return min(hammingTotal1,hammingTotal2)

    def computeManhattan(self):
        manhattanTotal1 = 0
        manhattanTotal2 = 0
        for row in self.state:
            for number in row:
                actualPosition = np.argwhere(self.state == number)[0]
                goalPosition1 = np.argwhere(goalState1 == number)[0]
                goalPosition2 = np.argwhere(goalState2 == number)[0]
                if not np.array_equal(actualPosition, goalPosition1):
                    manhattanTotal1 += ((abs(actualPosition[0] - goalPosition1[0]) + abs(
                        actualPosition[1] - goalPosition1[1])) / 2)
                if not np.array_equal(actualPosition, goalPosition2):
                    manhattanTotal2 += ((abs(actualPosition[0] - goalPosition2[0]) + abs(
                        actualPosition[1] - goalPosition2[1])) / 2)

        return math.floor(min(manhattanTotal1, manhattanTotal2))

    #Returns a string that traces back the solution from the goal state
    def solutionToString(self):
        str1 = ""
        if self.old_Node != None:
            str1 += self.old_Node.solutionToString()
        str1 += str(self.tileMoved) + " " + str(self.moveCost) + " " + self.toString() + "\n"
        return str1

    def isGoal(self, goal1, goal2):
        if np.array_equal(self.state, goal1) or np.array_equal(self.state, goal2):
            return True
        else: return False

    def toString(self):
        str1 = ""
        for row in self.state:
            for number in row:
                str1 += str(number) + " "
        return str1

    def createSuccessors(self, heuristic):

        #Calculate position of empty tile
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

        #Positions of the tiles to be switched
        leftPos = (position[0], position[1]-1)
        rightPos = (position[0], position[1] + 1)
        bottomPos = (position[0] + 1, position[1])
        topPos = (position[0] - 1, position[1])

        successorList = []

        #In each if block statement, a new puzzle state array is created by switching the empty tile and the target tile
        #A new Node object is created with that puzzle state and the cost of the move
        #This new successor node is then added to a list of all created successors
        if leftPos[1] >= 0:
            leftState = np.copy(self.state)
            leftState[leftPos[0]][leftPos[1]], leftState[position[0]][position[1]] = leftState[position[0]][position[1]], leftState[leftPos[0]][leftPos[1]]
            leftNode = Node(leftState, self, leftState[position[0]][position[1]], 1, self.weight + 1, heuristic)
            successorList.append(leftNode)

        if rightPos[1] <= col-1:
            rightState = np.copy(self.state)
            rightState[rightPos[0]][rightPos[1]], rightState[position[0]][position[1]] = \
            rightState[position[0]][position[1]], rightState[rightPos[0]][rightPos[1]]
            rightNode = Node(rightState, self,  rightState[position[0]][position[1]], 1, self.weight + 1, heuristic)

            successorList.append(rightNode)

        if bottomPos[0] <= row-1:
            botState = np.copy(self.state)
            botState[bottomPos[0]][bottomPos[1]], botState[position[0]][position[1]] = \
            botState[position[0]][position[1]], botState[bottomPos[0]][bottomPos[1]]
            bottomNode = Node(botState, self,  botState[position[0]][position[1]], 1, self.weight + 1, heuristic)
            successorList.append(bottomNode)

        if topPos[0] >= 0:
            topState = np.copy(self.state)
            topState[topPos[0]][topPos[1]], topState[position[0]][position[1]] = \
            topState[position[0]][position[1]], topState[topPos[0]][topPos[1]]
            topNode = Node(topState, self,  topState[position[0]][position[1]], 1, self.weight + 1, heuristic)
            successorList.append(topNode)

        if isCorner:
            #2-Create Wrapping moves, horizontal and vertical
            if position[1] == col-1:
                wrapLeftState = np.copy(self.state)
                wrapLeftState[position[0]][0], wrapLeftState[position[0]][position[1]] = \
                    wrapLeftState[position[0]][position[1]], wrapLeftState[position[0]][0]
                wrapLeftNode = Node(wrapLeftState, self, wrapLeftState[position[0]][position[1]], 2, self.weight + 2, heuristic)
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
                wrapRightNode = Node(wrapRightState, self, wrapRightState[position[0]][position[1]], 2, self.weight + 2, heuristic)
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
                wrapTopNode = Node(wrapTopState, self, wrapTopState[position[0]][position[1]], 2, self.weight + 2, heuristic)
                alreadyExists = False
                for successorNode in successorList:
                    if np.array_equal(wrapTopNode.state, successorNode.state):
                        alreadyExists = True
                if not alreadyExists:
                    successorList.append(wrapTopNode)

            elif position[0] == 0:
                wrapBottomState = np.copy(self.state)
                wrapBottomState[row - 1][position[1]], wrapBottomState[position[0]][position[1]] = \
                    wrapBottomState[position[0]][position[1]], wrapBottomState[row -1][position[1]]
                wrapBottomNode = Node(wrapBottomState, self, wrapBottomState[position[0]][position[1]], 2, self.weight + 2, heuristic)
                alreadyExists = False
                for successorNode in successorList:
                    if np.array_equal(wrapBottomNode.state, successorNode.state):
                        alreadyExists = True
                if not alreadyExists:
                    successorList.append(wrapBottomNode)

            #3-Create Diagonal moves

            #Top left corner
            if position == (0, 0):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[row-1][col-1], oppositeCornerState[0][0] = \
                oppositeCornerState[0][0], oppositeCornerState[row-1][col-1]
                oppositeCornerNode = Node(oppositeCornerState, self, oppositeCornerState[0][0], 3, self.weight + 3, heuristic)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[1][1], diagonalState[0][0] = \
                    diagonalState[0][0], diagonalState[1][1]
                diagonalNode = Node(diagonalState, self, diagonalState[0][0], 3, self.weight + 3, 0)
                successorList.append(diagonalNode)

            #Top Right Corner
            elif position == (0, col-1):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[row - 1][0], oppositeCornerState[0][col-1] = \
                    oppositeCornerState[0][col-1], oppositeCornerState[row - 1][0]
                oppositeCornerNode = Node(oppositeCornerState, self, oppositeCornerState[0][col-1], 3, self.weight + 3, heuristic)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[1][col-2], diagonalState[0][col-1] = \
                    diagonalState[0][col-1], diagonalState[1][col-2]
                diagonalNode = Node(diagonalState, self, diagonalState[0][col-1], 3, self.weight + 3, 0)
                successorList.append(diagonalNode)

            #Bottom Left Corner
            elif position == (row-1, 0):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[0][col - 1], oppositeCornerState[row-1][0] = \
                    oppositeCornerState[row-1][0], oppositeCornerState[0][col - 1]
                oppositeCornerNode = Node(oppositeCornerState, self, oppositeCornerState[row-1][0], 3, self.weight + 3, heuristic)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[row-2][1], diagonalState[row-1][0] = \
                    diagonalState[row-1][0], diagonalState[row-2][1]
                diagonalNode = Node(diagonalState, self, diagonalState[row-1][0], 3, self.weight + 3, heuristic)
                successorList.append(diagonalNode)

            #Bottom Right Corner
            elif position == (row-1, col-1):
                oppositeCornerState = np.copy(self.state)
                oppositeCornerState[0][0], oppositeCornerState[row - 1][col - 1] = \
                    oppositeCornerState[row - 1][col - 1], oppositeCornerState[0][0]
                oppositeCornerNode = Node(oppositeCornerState, self, oppositeCornerState[row - 1][col - 1], 3, self.weight + 3, heuristic)
                successorList.append(oppositeCornerNode)

                diagonalState = np.copy(self.state)
                diagonalState[row-2][col-2], diagonalState[row-1][col-1] = \
                    diagonalState[row-1][col-1], diagonalState[row-2][col-2]
                diagonalNode = Node(diagonalState, self, diagonalState[row-1][col-1], 3, self.weight + 3, heuristic)
                successorList.append(diagonalNode)

        return successorList