import numpy as np
import time
from operator import attrgetter
from Node import Node, goalState1, goalState2

# Parse string to get inital state puzzle
file1 = open('input.txt', 'r')
Lines = file1.readlines()

TotalSolutionLength = 0
TotalSearchLength = 0
TotalFailures = 0
TotalExecutionTime = 0
TotalCost = 0
with open("uniform_analysis.txt", mode='w+', newline='') as output_file:
    for line in Lines:
        arr = []
        for number in line.split():
            arr.append(int(number))


        #####------------WARNING---------------#####
        #For puzzles with dimensions other than 2x4,
        #Please change the initialState and the goalStates to the dimensions desired
        initialState = Node(np.array([[arr[0], arr[1], arr[2], arr[3]], [arr[4], arr[5], arr[6], arr[7]]]), None, 0, 0, 0, 0)

        openList = [initialState]
        closedList = []
        # Create Output Files
        # solutionFileName = str(puzzleNumber) + "_ucs_solution.txt"
        # searchFileName = str(puzzleNumber) + "_ucs_search.txt"

        SearchLength = 0
        start = time.time()
        while True:
            SearchLength += 1
            # output_file.write("0 " + str(openList[0].weight) + " 0 " + openList[0].toString()+ "\n")
            # Check if first Node is the goal
            solutionFound = openList[0].isGoal(goalState1,goalState2)
            if solutionFound:
                end = time.time()
                TotalSolutionLength += openList[0].countSolutionLength()
                TotalSearchLength += SearchLength
                TotalExecutionTime += (end - start)
                TotalCost += openList[0].weight
                print("Solution found, Total cost: ", openList[0].weight)
                break
            if(time.time() - start) >= 60:
                TotalFailures += 1
                TotalSearchLength += SearchLength
                TotalExecutionTime += 60
                print("no solution")
                break

            # Pop the visited node and add to closed list
            visitedNode = openList.pop(0)
            closedList.append(visitedNode)

            #Create successor nodes and check if they already exists
            newSuccessorList = visitedNode.createSuccessors(0)
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

        # Print solution to the output files
        if solutionFound:
            output_file.write("Solution Length: " + str(openList[0].countSolutionLength())
                              + ", Search Length: " + str(SearchLength)
                              + ", Cost: " + str(openList[0].weight)
                              + ", Execution Time: " + str(round(end - start, 3)) + "\n")
        else:
            output_file.write("No solution\n")
    output_file.write("\nTotal Solution Length: " + str(TotalSolutionLength)
                      + ", Average Solution Length: " + str(round(TotalSolutionLength / (len(Lines) - TotalFailures), 2)) + "\n")
    output_file.write("Total Search Length: " + str(TotalSearchLength)
                      + ", Average Search Length: " + str(round(TotalSearchLength / len(Lines), 2)) + "\n")
    output_file.write("Total Cost: " + str(TotalCost)
                      + ", Average Cost: " + str(round(TotalCost / (len(Lines) - TotalFailures), 2)) + "\n")
    output_file.write("Total Execution Time: " + str(round(TotalExecutionTime, 3))
                      + ", Average Execution Time: " + str(round(TotalExecutionTime / len(Lines), 3)) + "\n")