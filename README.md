# A2_Comp472

The χ-Puzzle
In this assignment you will implement and analyse a variety of search algorithms to solve the χ-Puzzle.
1.1 Rules of the Puzzle
The χ-Puzzle is a type of sliding-puzzle played on a wrapping board. The rules of the χ-Puzzle are the following:
1. The puzzle is an 2 × 4 board with 8 tiles (7 numbered and 1 empty).
2. Regular moves: Regular horizontal and vertical moves of sliding-puzzles are allowed and have a cost of 1.
3. Wrapping moves: If the empty tile is at a corner position, then the numbered tile at the other end of the
same row can slide into it. These moves are more expensive than regular moves, and have a cost of 2.
4. Diagonal moves: If the empty tile is at a corner position, then the numbered tile diagonally adjacent to it
inside the board, as well as the numbered tile in the opposed corner can be moved into it. These moves
are more expensive than regular moves, and have a cost of 3.
5. The goal of the puzzle is to reach either one of the 2 goals below with the lowest cost.

 
