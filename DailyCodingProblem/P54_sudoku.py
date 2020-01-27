# This problem was asked by Dropbox.

# Sudoku is a puzzle where you're given a partially-filled 9 by 9 grid with digits.
# The objective is to fill the grid with the constraint that every row, column, and box
# (3 by 3 box) must contain all of the digits from 1 to 9.

# Implement an efficient sudoku solver.


import random

nums = set(range(1, 10))
puzzle = []
choices = []
stack = []
modified = []
n = 0

base = 3
side = base*base


def printSudoku():
    def expandLine(line):
        return line[0]+line[5:9].join([line[1:5]*(base-1)]*base)+line[9:13]
    line0 = expandLine("╔═══╤═══╦═══╗")
    line1 = expandLine("║ . │ . ║ . ║")
    line2 = expandLine("╟───┼───╫───╢")
    line3 = expandLine("╠═══╪═══╬═══╣")
    line4 = expandLine("╚═══╧═══╩═══╝")

    symbol = " 123456789*"
    nums = [[""]+[symbol[n] for n in row] for row in puzzle]
    
    print()
    print ("  " + "".join("  %d " % (n+1) for n in range(9)))
    print("  " + line0)
    symbol = "ABCDEFGHI"
    for r in range(side):
        print(symbol[r]+ " " + "".join(n+s for n, s in zip(nums[r], line1.split("."))))
        print("  " + [line2, line3, line4][((r+1) % side == 0)+((r+1) % base == 0)])
    print()


def createSudoku(values):
    # pattern for a baseline valid solution
    def pattern(r, c):
        return (base*(r%base) + r//base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base*base+1))

    # produce board using randomized baseline pattern
    global puzzle
    puzzle = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # remove some of the numbers
    squares = side*side
    for p in random.sample(range(squares),squares - values):
        puzzle[p//side][p%side] = 0




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
    symbol = "ABCDEFGHI"
    return "{}{}".format(symbol[i], j+1)

def cellPos(cell):
    i,j = cell
    return pos(i,j)

def nakedSingle(i,j):
    global n
    if modified[i][j] :
        used = []
        for x, y in connectedCells(i, j):
            used.append(puzzle[x][y])
        choices[i][j] = nums - set(used)
        modified[i][j] = False
    if len(choices[i][j]) == 1:
        puzzle[i][j] = list(choices[i][j])[0]
        n += 1
        touch(i, j)
        print("%s = %s : naked single" % (pos(i,j),puzzle[i][j]))
        #printSudoku()
        return True
    elif len(choices[i][j]) == 0:
        print("INVALID SUDOKU")
        print("%s no available choice" % pos(i,j))
        return False
    return True

def hiddenSingle(axis,cells,i,j):
    global n
    others = []
    for y, x in cells:
        if modified[y][x]:
            #Incomplete, we need to come back later
            push(i,j)
            return True
        if (y,x) != (i,j):
            others += list(choices[y][x])
    result = list(choices[i][j] - set(others) )
    if len(result) == 1 :
        r = list(result)[0]
        puzzle[i][j] = r
        n += 1
        touch(i, j)
        print("%s = %d : hidden single in the %s" % (pos(i,j), r, axis))
        #printSudoku()
        return True
    elif len(result) > 1 :
        printSudoku()
        print("INVALID SUDOKU")
        print("%s multiple hidden choices" % pos(i,j))
        return False
    return True

def nakedPair(axis,cells,i,j):
    global n
    candidates = []
    # Search for pairs
    for y,x in cells:
        if modified[y][x]: 
            #Incomplete, we need to come back later
            push(i,j)
            return True
        candidates.append(sorted(choices[y][x]))
    # Compare pairs
    for a in range(len(candidates)) :
        for b in range(a+1,len(candidates)) :

            if candidates[a] == candidates[b] and len(candidates[a])==2:
                for r in range(len(candidates)):
                    if len(candidates[r]) >0 and r!=a and r!=b :
                        y,x = cells[r]
                        count = len(choices[y][x] )
                        choices[y][x] = choices[y][x] - set(candidates[a])
                        if count != len(choices[y][x]) :
                            pushConnected(y,x)
                            print("%s reduced to %s : naked pair %s-%s in the %s" % (cellPos(cells[r]),choices[y][x],cellPos(cells[a]),cellPos(cells[b]),axis))
    return True

def nakedTrpl(axis,cells,i,j):
    global n
    candidates = []
    # Search for triple
    for y,x in cells:
        if modified[y][x]: 
            #Incomplete, we need to come back later
            push(i,j)
            return True
        candidates.append(sorted(choices[y][x]))
    # Compare triples
    for a in range(len(candidates)) :
        for b in range(a+1,len(candidates)) :
            for c in range(b+1,len(candidates)) :
                if candidates[a] == candidates[b] == candidates[c] and len(candidates[a])== 3 :
                    for r in range(len(candidates)):
                        if len(candidates[r]) >0 and r!=a and r!=b and r!=c :
                            y,x = cells[r]
                            count = len(choices[y][x])
                            choices[y][x] = choices[y][x] - set(candidates[a])
                            if count != len(choices[y][x]) :
                                pushConnected(y,x)
                                print("%s reduced to %s : naked triple %s-%s-%s in the %s" % (cellPos(cells[r]),choices[y][x],cellPos(cells[a]),cellPos(cells[b]),cellPos(cells[c]),axis))
    return True

def nakedQuad(axis,cells,i,j):
    global n
    candidates = []
    # Search for quad
    for y,x in cells:
        if modified[y][x]: 
            #Incomplete, we need to come back later
            push(i,j)
            return True
        candidates.append(sorted(choices[y][x]))
    # Compare quads
    for a in range(len(candidates)) :
        for b in range(a+1,len(candidates)) :
            for c in range(b+1,len(candidates)) :
                for d in range(c+1,len(candidates)) :
                    if candidates[a] == candidates[b] == candidates[c] == candidates[d] and len(candidates[a])== 4 :
                        for r in range(len(candidates)):
                            if len(candidates[r]) >0 and r!=a and r!=b and r!=c and r!=d:
                                y,x = cells[r]
                                count = len(choices[y][x])
                                choices[y][x] = choices[y][x] - set(candidates[a])
                                if count != len(choices[y][x]) :
                                    pushConnected(y,x)
                                    print("%s reduced to %s : naked quad %s-%s-%s-%s in the %s" % (cellPos(cells[r]),choices[y][x],cellPos(cells[a]),cellPos(cells[b]),cellPos(cells[c]),cellPos(cells[d]),axis))
    return True


def solveSudoku():
    global stack
    global n
    global choices
    global modified
    choices = []
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
            choicesLine.append({})
        choices.append(choicesLine)
        modified.append(modifiedLine)

    

    while len(stack)>0:
        i,j = stack.pop(0)
        row = horizontalCells(i,j)
        col = verticalCells(i,j)
        box = boxCells(i,j)
        
        # SIMPLE TECHNIQUES
        if not nakedSingle(i,j) : break
        if puzzle[i][j] != 0 : continue

        if not hiddenSingle("row",row,i,j) : break
        if puzzle[i][j] != 0 : continue
        if not hiddenSingle("column",col,i,j) : break
        if puzzle[i][j] != 0 : continue
        if not hiddenSingle("box",box,i,j) : break
        if puzzle[i][j] != 0 : continue

        # INTERMEDIATE TECHNIQUES
        nakedPair("row",row,i,j)
        nakedTrpl("row",row,i,j)
        nakedQuad("row",row,i,j)

        nakedPair("column",col,i,j)
        nakedTrpl("column",col,i,j)
        nakedQuad("column",col,i,j)

        nakedPair("box",box,i,j)
        nakedTrpl("box",box,i,j)
        nakedQuad("box",box,i,j)


        #   NAKED QUINT

        #   HIDDEN PAIR
        #   HIDDEN TRIPLE
        #   HIDDEN QUAD

        #   POINTING PAIR
        #   POINTING TRIPLE

    printSudoku()
    if n<81 : 
        print("I couldn't solve this sudoku with the techniques I know")
    else:
        print("SOLVED")
    print()
            







createSudoku(40)
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
createSudoku(50)
print(puzzle)
printSudoku()
solveSudoku()
