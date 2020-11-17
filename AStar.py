import numpy as np
import time
from operator import attrgetter
from Node import Node


# Parse string to get inital state puzzle
file1 = open('input.txt', 'r')
Lines = file1.readlines()

puzzleNumber = 0
for line in Lines:
    arr = []
    for number in line.split():
        arr.append(int(number))


    for x in range(0,2):
        if x == 0:
            heuristic = "Hamming"
        if(x == 1):
            heuristic = "Permutation"

        #####------------WARNING---------------#####
        # For puzzles with dimensions other than 2x4,
        # Please change the initialState and the goalStates in the Node class to the dimensions desired
        initialState = Node(np.array([[arr[0], arr[1], arr[2], arr[3]], [arr[4], arr[5], arr[6], arr[7]]]), None, 0, 0, 0, heuristic)

        global goalState1
        global goalState2
        goalState1 = np.array([[1, 2, 3, 4], [5, 6, 7, 0]])
        goalState2 = np.array([[1, 3, 5, 7], [2, 4, 6, 0]])

        openList = [initialState]
        closedList = []
        # Create Output Files
        solutionFileName = str(puzzleNumber) + "_astar-h"+ str((x+1)) + "_solution.txt"
        searchFileName = str(puzzleNumber) + "_astar-h"+ str((x+1)) + "_search.txt"


        with open(searchFileName, mode='w+', newline='') as output_file:
            start = time.time()
            while True:
                output_file.write(str(openList[0].Fn) + " " + str(openList[0].weight) + " " + str(openList[0].Hn) + " " + openList[0].toString()+ "\n")
                # Check if first Node is the goal
                solutionFound = openList[0].isGoal(goalState1,goalState2)
                if solutionFound:
                    end = time.time()
                    print("Solution found, Total cost: ", openList[0].weight)
                    break
                if(time.time() - start) >= 60:
                    print("no solution")
                    break

                # Pop the visited node and add to closed list
                visitedNode = openList.pop(0)
                closedList.append(visitedNode)

                #Create successor nodes and check if they already exists
                newSuccessorList = visitedNode.createSuccessors("Hamming")
                for successorNode in newSuccessorList:
                    for openNode in openList:
                        if np.array_equal(successorNode.state, openNode.state) and successorNode.Fn < openNode.Fn:
                            openList.remove(openNode)
                    for closedNode in closedList:
                        if np.array_equal(successorNode.state, closedNode.state) and successorNode.Fn < closedNode.Fn:
                            closedList.remove(closedNode)
                    openList.append(successorNode)

                # Sort open list by weight
                openList.sort(key=attrgetter('Fn'))
        output_file.close()

        # Print solution to the output files
        if solutionFound:
            with open(solutionFileName, mode='w+', newline='') as output_file:
                output_file.write(openList[0].solutionToString())
                output_file.write(str(openList[0].weight) + " " + str(round(end-start, 3)))
                output_file.close()
        else:
            with open(searchFileName, mode='w+', newline='') as output_file:
                output_file.write("No solution")
                output_file.close()
            with open(solutionFileName, mode='w+', newline='') as output_file:
                output_file.write("No solution")
                output_file.close()

    puzzleNumber += 1
