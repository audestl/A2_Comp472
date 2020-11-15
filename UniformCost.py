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

    initialState = Node(np.array([[arr[0], arr[1], arr[2], arr[3]], [arr[4], arr[5], arr[6], arr[7]]]), None, 0, 0, 0, 0)

    openList = [initialState]
    closedList = []
    # Create Output Files
    solutionFileName = str(puzzleNumber) + "_ucs_solution.txt"
    searchFileName = str(puzzleNumber) + "_ucs_search.txt"

    with open(searchFileName, mode='w+', newline='') as output_file:
        start = time.time()
        while True:
            output_file.write("0 " + str(openList[0].weight) + " 0 " + openList[0].toString()+ "\n")
            # Check if first Node is the goal
            solutionFound = openList[0].isGoal()
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
            newSuccessorList = visitedNode.createSuccessors(True)
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