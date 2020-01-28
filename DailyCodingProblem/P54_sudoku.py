# This problem was asked by Dropbox.

# Sudoku is a puzzle where you're given a partially-filled 9 by 9 grid with digits.
# The objective is to fill the grid with the constraint that every row, column, and box
# (3 by 3 box) must contain all of the digits from 1 to 9.

# Implement an efficient sudoku solver.


import random
import os
import copy

clear = lambda : os.system('clear')

nums = set(range(1, 10))
puzzle = []
candidates = []
stack = []
modified = []
n = 0

debug = False
s = []

tuples = ["", "SINGLE", "DOUBLE", "TRIPLE", "QUADRUPLE", "QUINTUPLE"]
symbol = " 123456789*"
letters = "ABCDEFGHI"

def printCandidates():
    def expandLine(line):
        return line[0]+line[9:17].join([line[1:9]*(2)]*3)+line[17:25]
    line0 = expandLine("╔═══════╤═══════╦═══════╗")
    line1 = expandLine("║   .   │   .   ║   .   ║")
    line2 = expandLine("╟───────┼───────╫───────╢")
    line3 = expandLine("╠═══════╪═══════╬═══════╣")
    line4 = expandLine("╚═══════╧═══════╩═══════╝")
    
    val = [[[f'{i+1}' if i+1 in cell else ' ' for i in range(9)] for cell in row] for row in candidates]
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] > 0 :
                val[i][j] = ['┌','─','┐' ,'│',f"{puzzle[i][j]}",'│' ,'└','─','┘' ]
                
    print ("      " + "       ".join("%d" % (n+1) for n in range(9)))
    print("  " + line0)
    for i in range(9):
        for l in range(3):
            print(f"{letters[i] if l==1 else ' '} ║ " + " ║ ".join(" │ ".join(" ".join(val[i][j+k*3][c+l*3]  for c in range(3)) for j in range(3)) for k in range(3)) + f" ║ {letters[i] if l==1 else ' '} ")
        print("  " + [line2, line3, line4][((i+1) % 9 == 0)+((i+1) % 3 == 0)])
    print ("      " + "       ".join("%d" % (n+1) for n in range(9)))

    print()

def simpleSudoku(sudoku = False):
    if not sudoku : sudoku = puzzle
    val = [[symbol[n] for n in row] for row in sudoku]
    for i in range(9):
        print(f"{letters[i]}  " + " │ ".join(" ".join(f"{val[i][j+k*3]}" for j in range(3)) for k in range(3)))
        if i==2 or i == 5: print("   ──────┼───────┼──────")
    print()
    print("   " + "   ".join(" ".join(f"{j+1+k*3}" for j in range(3)) for k in range(3)))
    print()


def printSudoku(sudoku = False):
    if not sudoku : sudoku = puzzle
    def expandLine(line):
        return line[0]+line[5:9].join([line[1:5]*(3-1)]*3)+line[9:13]
    line0 = expandLine("╔═══╤═══╦═══╗")
    line1 = expandLine("║ . │ . ║ . ║")
    line2 = expandLine("╟───┼───╫───╢")
    line3 = expandLine("╠═══╪═══╬═══╣")
    line4 = expandLine("╚═══╧═══╩═══╝")
    
    val = [[""]+[symbol[n] for n in row] for row in sudoku]
    print()
    print("  " + line0)
    for r in range(9):
        print(letters[r]+ " " + "".join(n+s for n, s in zip(val[r], line1.split("."))))
        print("  " + [line2, line3, line4][((r+1) % 9 == 0)+((r+1) % 3 == 0)])
    print ("  " + "".join("  %d " % (n+1) for n in range(9)))
    print()


def createSudoku(values):
    # pattern for a baseline valid solution
    def pattern(r, c):
        return (3*(r%3) + r//3 + c) % 9

    # randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(3)
    rows = [g*3 + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*3 + c for g in shuffle(rBase) for c in shuffle(rBase)]
    vals = shuffle(range(1, 3*3+1))

    # produce board using randomized baseline pattern
    global puzzle
    puzzle = [[vals[pattern(r, c)] for c in cols] for r in rows]

    
    print("The solution:")
    for row in puzzle : print (row)

    # remove some of the numbers
    squares = 9*9
    for p in random.sample(range(squares),squares - values):
        puzzle[p//9][p%9] = 0




def horizontalCells(i, j):
    return [(i,k) for k in range(9)]

def verticalCells(i, j):
    return [(k,j) for k in range(9)]

def boxCells(i, j):
    return [(y,x) for y in range(i//3*3, i//3*3+3)  for x in range(j//3*3, j//3*3+3)]

def connectedCells(i, j):
    # return a list of cells connected to the (i,j) cell
    return horizontalCells(i,j) + verticalCells(i,j) + boxCells(i,j)

def touch(i, j):
    for y, x in connectedCells(i, j):
        if puzzle[y][x] == 0:
            if (y,x) != (i,j):
                push(y,x)
                modified[y][x] = True

def pushConnected(i,j):
    for y, x in connectedCells(i, j):
        if puzzle[y][x] == 0:
            if (y,x) != (i,j):
                push(y,x)
    pushTop(i,j)

def push(i,j):
    if not (i,j) in stack :
        stack.append((i,j))

def pushTop(i,j):
    if (i,j) in stack :
        stack.remove((i,j))
    stack.insert(0,(i,j))

def pos(i,j):
    return f"{letters[i]}{j+1}"

def cellPos(cell):
    i,j = cell
    return pos(i,j)

def solveCell(i,j,value):
    global n
    puzzle[i][j]=value
    candidates[i][j] = []
    n += 1
    touch(i, j)
    if (i,j) in stack :
        stack.remove((i,j))
    return value

def nakedSingle(i,j):
    if modified[i][j] :
        used = []
        for x, y in connectedCells(i, j):
            used.append(puzzle[x][y])
        candidates[i][j] = sorted(nums - set(used))
        modified[i][j] = False
    if len(candidates[i][j]) == 1:
        r = solveCell(i,j,candidates[i][j][0])
        print(f"NAKED SINGLE : {r} is the only candidate for {pos(i,j)}")
        print(f" ->  {pos(i,j)} = {r}")
        if debug : printCandidates()
        return True
    elif len(candidates[i][j]) == 0:
        printCandidates()
        print("ERROR")
        print(f"{pos(i,j)} : no available choice")
        return False
    return True

def hiddenSingle(group,cells,i,j):
    global n
    others = set()
    for y, x in cells:
        if modified[y][x]:
            #Incomplete, we need to come back later
            push(i,j)
            return True
        if (y,x) != (i,j):
            others.update(candidates[y][x])
    result = set(candidates[i][j]) - others
    if len(result) == 1 :
        r = solveCell(i,j,list(result)[0])
        print(f"HIDDEN SINGLE : {pos(i,j)} is the only possibility for {r} in the {group}") 
        print(f" ->  {pos(i,j)} = {r}") 
        if debug : printCandidates()
        return True
    elif len(result) > 1 :
        printCandidates()
        print("ERROR")
        print(f"{pos(i,j)} : multiple hidden candidates")
        return False
    return True

def hiddenGroups(group,cells,i,j):
    global n
    positions = [[] for r in range(10)]      # contains the position index of the cells that contain the value (from 1 to 9)
    # Get all candidates for the group
    for p, cell in enumerate(cells):
        y,x = cell
        if modified[y][x]:
            #Incomplete, we need to come back later
            push(i,j)
            return True
        for c in candidates[y][x]:
            positions[c].append(p) 
    # Search hidden pairs
    for a in range(1,10):
        if len(positions[a]) > 1:
            pairs = [a]
            for b in range(a+1,10):
                if positions[a] == positions[b]:
                    pairs.append(b)
            if len(pairs) == len(positions[a]):
                # Since the candidate values only occur in these cells, all other candidates can be removed from these cells.
                for r in positions[a]:
                    y,x = cells[r]
                    previous = candidates[y][x]
                    candidates[y][x] = pairs[:]
                    if len(previous) != len(candidates[y][x]) :
                        position = cellPos(cell)
                        pushConnected(y,x)
                        position = "[" + ", ".join(cellPos(cells[c]) for c in positions[a]) + "]"
                        print(f"HIDDEN {tuples[len(pairs)]} {position} in the {group}, only these cells contain {set(pairs)}, all other candidates can be removed")
                        print(f" ->  {cellPos(cells[r])} reduced from {previous} to {candidates[y][x]}")
                        if debug : printCandidates()

def nakedGroups(group,cells,i,j):
    global n
    myCandidates = []                         # contains the candidates of each cell of the group (from 0 to 8)
    # Get all candidates for the group
    for y,x in cells:
        if modified[y][x]: 
            #Incomplete, we need to come back later
            push(i,j)
            return True
        myCandidates.append(candidates[y][x])
    # Search pairs
    for a in range(9) :
        if len(myCandidates[a]) > 1 :
            pairs = [a]
            for b in range(a+1,9) :
                if myCandidates[a] == myCandidates[b] : 
                    pairs.append(b)
            if len(pairs) == len(myCandidates[a]):
                # Since these values are the only candidates for those cells, the values can be removed from all other unsolved cells in the group.
                for r in range(9):
                    if len(myCandidates[r]) >0 and not r in pairs :
                        y,x = cells[r]
                        previous = candidates[y][x]
                        candidates[y][x] = sorted(set(candidates[y][x]) - set(myCandidates[a]))
                        if len(previous) != len(candidates[y][x]) :
                            pushConnected(y,x)
                            position = "[" + ", ".join(cellPos(cells[c]) for c in pairs) + "]"
                            print(f"NAKED {tuples[len(pairs)]} {position} in the {group}, {myCandidates[a]} are the only candidates for these cells, they are not in the rest of the {group}")
                            print(f" ->  {cellPos(cells[r])} reduced from {previous} to {candidates[y][x]}")
                            if debug : printCandidates()
    return True

def pointingPair(group,cells,outputGroup,outputCells,i,j):
    #If a pair of empty cells within a box in the same row or column share a given candidate then that candidate can be removed from the candidate list of all other cells in the row or column if it is not a candidate of any of the other cells in the box.        
    global n
    intersection = [0 for r in range(10)]     # contains the position index of the cells that contain the value (from 1 to 9)
    positions = [[] for r in range(10)]      # contains the position index of the cells that contain the value (from 1 to 9)
    # Check if output group is complete
    for y,x in outputCells:
        if modified[y][x]:
            #Incomplete, we need to come back later
            push(i,j)
            return True
    # Get all candidates for the box
    for p,cell in enumerate(cells):
        y,x = cell
        if modified[y][x]:
            #Incomplete, we need to come back later
            push(i,j)
            return True
        for c in candidates[y][x]:
            # Check if the cell is in the output row or col
            if cell in outputCells:
                intersection[c] += 1
            positions[c].append(p) 
    for a in range(1,10):
        if intersection[a] == len(positions[a]) > 1:
            #this value is only in the output group
            for cell in outputCells:
                if not cell in cells:
                    y,x = cell
                    previous = str(candidates[y][x])
                    if a in candidates[y][x] :
                        candidates[y][x].remove(a)
                        pushConnected(y,x)
                        position = "[" + ", ".join(cellPos(cells[c]) for c in positions[a]) + "]"
                        print(f"POINTING {tuples[len(positions[a])]} : {position} is the only possibility for {a} in the {group}. As these cells are also in the same {outputGroup}, {a} is not in the rest of the {outputGroup}")
                        print(f" ->  {cellPos(cell)} reduced from {previous} to {candidates[y][x]}")
                        if debug : printCandidates()

def XWing():
    #printCandidates()
    for n in range(1,10):
        column = [[] for _ in range(9)] #position of n in each column
        row =    [[] for _ in range(9)] #position of n in each row
        for i in range(9):
            for j in range(9):
                if n in candidates[i][j]:
                    column[j].append(i)
                    row[i].append(j)
        for a in range(9):
            if len(column[a])>1:
                columnPair = [a]
                for b in range(a+1,9):
                    if column[a] == column[b] :
                        columnPair.append(b)
                if len(columnPair) == len(column[a]):
                    for r in column[a]:
                        for c in range(9):
                            if not c in columnPair:
                                previous = str(candidates[r][c])
                                if n in candidates[r][c]:
                                    candidates[r][c].remove(n)
                                    pushConnected(r,c)
                                    rowNames = " & ".join(letters[r] for r in column[a])
                                    colNames = " & ".join(f"{c+1}" for c in columnPair)
                                    print(f"X-WING : Columns {colNames} have their only {n} in rows {rowNames}, {n} is not in the rest of these rows")
                                    print(f" ->  {pos(r,c)} reduced from {previous} to {candidates[r][c]}")
                                    if debug : printCandidates()
                                    

            if len(row[a])>1:
                rowPair = [a]
                for b in range(a+1,9):
                    if row[a] == row[b] :
                        rowPair.append(b)
                if len(rowPair) == len(row[a]):
                    for r in range(9):
                        for c in row[a]:
                            if not r in rowPair:
                                previous = str(candidates[r][c])
                                if n in candidates[r][c]:
                                    candidates[r][c].remove(n)
                                    pushConnected(r,c)
                                    colNames = " & ".join(f"{c+1}" for c in row[a])
                                    rowNames = " & ".join(letters[r] for r in rowPair)
                                    print(f"X-WING : Rows {rowNames} have their only {n} in columns {colNames}, {n} is not in the rest of these columns")
                                    print(f" ->  {pos(r,c)} reduced from {previous} to {candidates[r][c]}")
                                    if debug : printCandidates()
    


    




def solveSudoku():
    global stack
    global n
    global candidates
    global modified
    candidates = []
    modified = []
    for i in range(9):
        choicesLine = []
        modifiedLine = []
        for j in range(9):
            if puzzle[i][j] == 0:    
                modifiedLine.append(True)
                push(i,j)
            else:
                modifiedLine.append(False)
                n += 1
            choicesLine.append([])
        candidates.append(choicesLine)
        modified.append(modifiedLine)

    

    while len(stack)>0:
        i,j = stack.pop(0)
        row = horizontalCells(i,j)
        col = verticalCells(i,j)
        box = boxCells(i,j)
        
        # SIMPLE TECHNIQUES
        # the result of those techniques can be :
        #  False = an error has occured, the SUDOKU is invalid
        #  True  = no error
        # If the cell has changed, then no need to continue testing this cell 

        if not nakedSingle(i,j) : break
        if puzzle[i][j] != 0 : continue
        if not hiddenSingle("box",box,i,j) : break
        if puzzle[i][j] != 0 : continue
        if not hiddenSingle("row",row,i,j) : break
        if puzzle[i][j] != 0 : continue
        if not hiddenSingle("column",col,i,j) : break
        if puzzle[i][j] != 0 : continue

        # INTERMEDIATE TECHNIQUES
        nakedGroups("box",box,i,j)
        nakedGroups("row",row,i,j)
        nakedGroups("column",col,i,j)

        hiddenGroups("box",box,i,j)
        hiddenGroups("row",row,i,j)
        hiddenGroups("column",col,i,j)

        pointingPair("box",box,"row",row,i,j)
        pointingPair("box",box,"column",col,i,j)
        pointingPair("row",row,"box",box,i,j)
        pointingPair("column",col,"box",box,i,j)

        # ADVANCED TECHNIQUES
        # Only if the stack is empty because :
        # 1. Those are costly routines
        # 2. They need the candidates for every cells

        if len(stack)==0 :
            XWing()

        
        # XYWing
        # Swordfish
        # Jellyfish
        # Squirmbag
        # Burma

    #printSudoku()
    printCandidates()
    if n<81 : 
        print("I couldn't solve this sudoku with the techniques I know")
    else:
        print("SOLVED !")
    print()
            
def initBruteSolve(sudoku):
    n = 0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0 :
                n +=1
    bruteSolve(sudoku,n)

    print(len(s))

def bruteSolve(sudoku,n):
    global s
    if n == 81 :
        if not sudoku in s :
            s.append(sudoku)
            print (f"Solution : {len(s)}")
            simpleSudoku(sudoku)
    else:
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0 :
                    #simpleSudoku(sudoku)
                    used = []
                    for x, y in connectedCells(i, j):
                        used.append(sudoku[x][y])
                    candidates = sorted(nums - set(used))
                    if len(candidates) == 0 :
                        return
                    for candidate in candidates:
                        newSudoku = copy.deepcopy(sudoku)
                        newSudoku[i][j] = candidate
                        bruteSolve(newSudoku,n+1) 








# clear()
# empty
puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]
#hard #3539 on https://www.sudoku-solutions.com
puzzle = [[0, 0, 2, 9, 0, 1, 0, 0, 0],\
          [0, 0, 0, 0, 0, 0, 5, 3, 0],\
          [0, 1, 0, 0, 0, 3, 4, 2, 0],\
          [0, 6, 0, 0, 0, 7, 1, 0, 0],\
          [2, 7, 0, 0, 8, 0, 0, 4, 3],\
          [0, 0, 3, 5, 0, 0, 0, 6, 0],\
          [0, 2, 6, 7, 0, 0, 0, 8, 0],\
          [0, 3, 4, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 3, 0, 2, 7, 0, 0]]
# the same twisted
puzzle = [[0, 0, 0, 0, 2, 0, 0, 0, 0],\
          [0, 0, 1, 6, 7, 0, 2, 3, 0],\
          [2, 0, 0, 0, 0, 3, 6, 4, 0],\
          [9, 0, 0, 0, 0, 5, 7, 0, 3],\
          [0, 0, 0, 0, 8, 0, 0, 0, 0],\
          [1, 0, 3, 7, 0, 0, 0, 0, 2],\
          [0, 5, 4, 1, 0, 0, 0, 0, 7],\
          [0, 3, 2, 0, 4, 6, 8, 0, 0],\
          [0, 0, 0, 0, 3, 0, 0, 0, 0]]
#medium 1925 on https://www.sudoku-solutions.com
puzzle = [[0, 2, 0, 0, 8, 9, 7, 0, 3],\
          [0, 0, 0, 0, 1, 5, 0, 0, 8],\
          [9, 0, 0, 0, 0, 0, 0, 0, 0],\
          [0, 9, 0, 0, 0, 0, 3, 0, 0],\
          [3, 0, 7, 0, 0, 0, 2, 0, 1],\
          [0, 0, 4, 0, 0, 0, 0, 6, 0],\
          [0, 0, 0, 0, 0, 0, 0, 0, 6],\
          [8, 0, 0, 4, 7, 0, 0, 0, 0],\
          [5, 0, 1, 9, 3, 0, 0, 8, 0]]
# nakedPair
puzzle = [[1, 0, 4, 0, 9, 0, 0, 6, 8],\
          [9, 5, 6, 0, 1, 8, 0, 3, 4],\
          [0, 0, 8, 4, 0, 6, 9, 5, 1],\
          [5, 1, 0, 0, 0, 0, 0, 8, 6],\
          [8, 0, 0, 6, 0, 0, 0, 1, 2],\
          [6, 4, 0, 0, 8, 0, 0, 9, 7],\
          [7, 8, 1, 9, 2, 3, 6, 4, 5],\
          [4, 9, 5, 0, 6, 0, 8, 2, 3],\
          [0, 6, 0, 8, 5, 4, 1, 7, 9]]
createSudoku(73)
debug = False
print(f"puzzle = {puzzle}")
printSudoku()
solveSudoku()
#initBruteSolve(puzzle)
