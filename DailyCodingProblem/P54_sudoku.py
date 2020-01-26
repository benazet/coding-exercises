# This problem was asked by Dropbox.

# Sudoku is a puzzle where you're given a partially-filled 9 by 9 grid with digits.
# The objective is to fill the grid with the constraint that every row, column, and box
# (3 by 3 subgrid) must contain all of the digits from 1 to 9.

# Implement an efficient sudoku solver.

nums = set(range(1,10))

import random

def printSudoku(puzzle,lin=9,col=9):
    for i in range(9):
        line = " "
        if i % 3 == 0 : 
            print()
        for j in range(9):
            if j % 3 == 0 :
                line += "  "
            if puzzle[i][j] == 0 :
                if i == lin and j == col :
                    line += " *"
                else :
                    line += " ."
            else:
                line += " %d" % puzzle[i][j] 
        print(line)
    print()

def connectedCells(i,j):
    # return a list of cells connected to the (i,j) cell
    cells = []
    for k in range(9):
        if k != j :
            cells.append((i,k))
        if k != i :
            cells.append((k,j))
    lin = i//3*3
    col = j//3*3
    for y in range(lin,lin+3):
        for x in range(col,col+3):
            if y!=i or x!=j:
                cells.append((y,x))
    return cells

def possibleValues(puzzle,i,j):
    used_nums = []
    for x,y in connectedCells(i,j):
        used_nums.append(puzzle[x][y])
    return nums - set(used_nums)

def exclusiveValues(choices,i,j):
    others = []
    for x,y in connectedCells(i,j):
        others += list(choices[x][y])
    return choices[i][j] - set(others)

def CreateSudoku(n):
    puzzle = []
    for _ in range(9):
        puzzle.append([0]*9)


    while n > 0 :
        i = random.randint(0,8)
        j = random.randint(0,8)
        if puzzle[i][j] == 0:
            choices = possibleValues(puzzle,i,j)
            if len(choices)>0 :
                puzzle[i][j] = random.sample(choices,1)[0]
                n-=1
            else :
                printSudoku(puzzle,i,j)
                print("unsolvable puzzle at %d,%d" % (i,j))
                return puzzle
                
    return puzzle


def solveSudoku(puzzle):
    # Create a 2D table of dicts that will contain the possible choices for that cell
    choices = []
    changed = []
    for _ in range(9):
        line = []
        for _ in range(9):
            line.append({})
            changed.append([False]*9)
        choices.append(line)

    n = 0 # Number of filled values
    # Initial possible values
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0 :
                choices[i][j] = possibleValues(puzzle,i,j) 
                if len(choices[i][j]) == 1:
                    # printSudoku(puzzle,i,j)
                    print("The value at %d,%d is %d" % (i,j,list(choices[i][j])[0]))
                elif len(choices[i][j]) == 0:
                    # printSudoku(puzzle,i,j)
                    print("Error, no choice at %d,%d" % (i,j)) 
                    return             
            else:
                n += 1

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0 :
                e = exclusiveValues(choices,i,j)
                if len(e) == 1 :
                    # printSudoku(puzzle,i,j)
                    print("The value at %d,%d is %d" % (i,j,list(e)[0]))
                elif len(e) > 1 :
                    # printSudoku(puzzle,i,j)
                    print("Error, multiple exclusive choices at %d,%d :" %(i,j))
                    print(e)
            else:
                n += 1




    

puzzle = CreateSudoku(40)
printSudoku(puzzle)
solveSudoku(puzzle)