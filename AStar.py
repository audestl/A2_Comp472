import numpy as np
import time
from operator import attrgetter
from Node import Node, goalState1, goalState2


# Parse string to get inital state puzzle
file1 = open('input.txt', 'r')
Lines = file1.readlines()

TotalSolutionLength = 0
TotalSearchLengthWithFailure = 0
TotalSearchLengthWithoutFailure = 0
TotalFailures = 0
TotalExecutionTimeWithFailure = 0
TotalExecutionTimeWithoutFailure = 0
TotalCost = 0
with open("astar-h2_analysis.txt", mode='w+', newline='') as output_file:
    for line in Lines:
        arr = []
        for number in line.split():
            arr.append(int(number))


        for x in range(2,3):
            if x == 0:
                heuristic = "H0"
            elif x == 1:
                heuristic = "Hamming"
            elif (x == 2):
                heuristic = "Manhattan"

            #####------------WARNING---------------#####
            # For puzzles with dimensions other than 2x4,
            # Please change the initialState and the goalStates in the Node class to the dimensions desired
            initialState = Node(np.array([[arr[0], arr[1], arr[2], arr[3]], [arr[4], arr[5], arr[6], arr[7]]]), None, 0, 0, 0, heuristic)

            openList = [initialState]
            closedList = []
            # Create Output Files
            # solutionFileName = str(puzzleNumber) + "_astar-h"+ str(x) + "_solution.txt"
            # searchFileName = str(puzzleNumber) + "_astar-h"+ str(x) + "_search.txt"

            SearchLength = 0
            start = time.time()
            while True:
                SearchLength += 1
                # Check if first Node is the goal
                solutionFound = openList[0].isGoal(goalState1,goalState2)
                if solutionFound:
                    end = time.time()
                    TotalSolutionLength += openList[0].countSolutionLength()

                    TotalSearchLengthWithFailure += SearchLength
                    TotalExecutionTimeWithFailure += (end - start)

                    TotalSearchLengthWithoutFailure += SearchLength
                    TotalExecutionTimeWithoutFailure += (end - start)

                    TotalCost += openList[0].weight
                    print("Solution found, Total cost: ", openList[0].weight)
                    break
                if(time.time() - start) >= 60:
                    TotalFailures += 1
                    TotalSearchLengthWithFailure += SearchLength
                    TotalExecutionTimeWithFailure += 60
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
    output_file.write("Total Search Length (Failures Included): " + str(TotalSearchLengthWithFailure)
                      + ", Average Search Length (Failures Included): " + str(round(TotalSearchLengthWithFailure / len(Lines), 2)) + "\n")
    output_file.write("Total Search Length (Failures Excluded): " + str(TotalSearchLengthWithoutFailure)
                      + ", Average Search Length (Failures Excluded): " + str(round(TotalSearchLengthWithoutFailure / (len(Lines) - TotalFailures), 2)) + "\n")
    output_file.write("Total Failure: " + str(TotalFailures)
                      + ", Average Failure: " + str(round(TotalFailures / len(Lines), 3)) + "\n")
    output_file.write("Total Cost: " + str(TotalCost)
                      + ", Average Cost: " + str(round(TotalCost / (len(Lines) - TotalFailures), 2)) + "\n")
    output_file.write("Total Execution Time (Failure Included): " + str(round(TotalExecutionTimeWithFailure, 3))
                      + ", Average Execution Time (Failure Included): " + str(round(TotalExecutionTimeWithFailure / len(Lines), 3)) + "\n")
    output_file.write("Total Execution Time (Failure Excluded): " + str(round(TotalExecutionTimeWithoutFailure, 3))
                      + ", Average Execution Time (Failure Excluded): " + str(round(TotalExecutionTimeWithoutFailure / (len(Lines) - TotalFailures), 3)) + "\n")


