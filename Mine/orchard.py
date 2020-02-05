import random

# global variables
tree      = []
number    = 0
_flag      = []
flags     = 0
_apples    = []
_clear     = []
width     = 0
height    = 0
cleared   = 0
stack     = []
neighbour = []
linked    = []
verbose   = False
seed      = 0

ClearingTechnique   = 1
LumberjackTechnique = 0
ForresterTechnique  = 0
TwinsTechnique      = 0
TripletsTechnique   = 0
DragonsTechnique    = 0
BruteForceTechnique = 0

def createOrchard(h, w, n=-1, r=-1, c=-1):
    global width
    global height
    global number
    global tree
    global _flag
    global _apples
    global _clear
    global neighbour
    global linked

    width = w
    height = h

    tree      = [[False for _ in range(width)] for _ in range(height)]
    _flag      = [[False for _ in range(width)] for _ in range(height)]
    _clear     = [[False for _ in range(width)] for _ in range(height)]
    _apples   = [[-1    for _ in range(width)] for _ in range(height)]
    neighbour = [[[]    for _ in range(width)] for _ in range(height)]
    linked    = [[[]    for _ in range(width)] for _ in range(height)]

    if n == -1:
        n = width * height / 3
    n = min(n, width*height-1)
    number = n

    while n > 0:
        x = random.randrange(width)
        y = random.randrange(height)
        if not tree[y][x]:
            # if r == -1 or c == -1 or y != r or x != c:
            if r == -1 or c == -1 or abs(y-r) > 1 or abs(x-c) > 1:
                tree[y][x] = True
                n -= 1


def printOrchard(cheat=False):
    global seed
    global number
    printCells(0,height,0,width,cheat)
    print(f"   🌲  {width * height - cleared - flags} unchecked trees",end = '')
    print(f" / 🎄  {number - flags} apple trees",end = '')
    print(f" / 🍏  {flags} flags",end = '')
    print(f" / seed = {seed}")
    print()
    print(f"Techniques used :")
    print(f"   {'Clearing':<12}{ClearingTechnique:>3}")
    print(f"   {'Lumberjack':<12}{LumberjackTechnique:>3}")
    print(f"   {'Forrester':<12}{ForresterTechnique:>3}")
    print(f"   {'Twins':<12}{TwinsTechnique:>3}")
    print(f"   {'Triplets':<12}{TripletsTechnique:>3}")
    print(f"   {'Dragons':<12}{DragonsTechnique:>3}")
    print(f"   {'Brute Force':<12}{BruteForceTechnique:>3}")
    print()
def printGroup(group,cheat=False):
    
    neighbours = [n for c in group for n in neighbourCells(c) ]
    rMin = min(r for r,c in neighbours)
    rMax = max(r for r,c in neighbours)+1
    cMin = min(c for r,c in neighbours)
    cMax = max(c for r,c in neighbours)+1
    
    printCells(rMin,rMax,cMin,cMax,cheat)
    
def printCells(rMin,rMax,cMin,cMax,cheat):
    def expandLine(line):
        return [line[4],line[0]][cMin==0] + "".join(line[1:5] for _ in range(cMax- cMin-1)) + [line[1:5],line[5:9]][cMax==width] 
    line0 = expandLine("┌───┬───┐")
    line1 = expandLine("│ . │ . │")
    line2 = expandLine("├───┼───┤")
    line3 = expandLine("└───┴───┘")

    symbol = " 12345678🌲"  # ▉
    val = []
    for r in range(height):
        row = [""]
        for c in range(cMin,cMax):
            cell = symbol[_apples[r][c]]
            if cheat:
                if tree[r][c]:
                    cell = "🎄" #🌳"  # 
            if _flag[r][c]:
                if tree[r][c] or not cheat:
                    cell =  "🍏"  # ⚑
                else:
                    cell =  "🍎"  # ⚐
                    
            row += cell
        val.append(row)

    print()
    print("    " + " ".join(f"{c+1:^3}" for c in range(cMin,cMax)))
    print("   " + [line2, line0][rMin==0])
    for r in range(rMin,rMax):
        print(f"{letter(r):^3}", end='')
        print("".join(a+b for a, b in zip(val[r], line1.split("."))), end='')
        print(f"{letter(r):^3}") 
        print("   " + [line2, line3][r==height-1])
    print("    " + " ".join(f"{c+1:^3}" for c in range(cMin,cMax)))
    print()

def positions(group):
    return ' '.join(position(cell) for cell in group)

def position(cell):
    r, c = cell
    return f"{letter(r)}{c+1}"

def letter(r):
    if height <= 26:
        result = chr(r+65)
    else:
        result = chr(r//26+65) + chr(r % 26+65)
    return result


def apples(cell):
    r, c = cell
    if _apples[r][c] == -1 :
        _apples[r][c] = 0
        for i, j in neighbourCells(cell):
            if tree[i][j]:
                _apples[r][c] += 1
                
    return _apples[r][c]

def clear(cell):
    r,c = cell
    return _clear[r][c]

def flag(cell):
    r,c = cell
    return _flag[r][c]

def neighbourCells(cell):
    r, c = cell
    if neighbour[r][c] == []:
        cells = []
        for i in range(max(r-1, 0), min(r+2, height)):
            for j in range(max(c-1, 0), min(c+2, width)):
                if i != r or j != c:
                    cells.append((i, j))
        neighbour[r][c] = cells

    return neighbour[r][c]

def borders():
    borderCells = []
    for r in range(height):
        for c in range(width):
            cell = (r,c)
            if not clear(cell) and not flag(cell):
                border = [c for c in neighbourCells(cell) if clear(c)]
                borderCells += border
    return sorted(set(borderCells))

def linkedCells(cell):
    r, c = cell
    if linked[r][c] == []:
        cells = []
        for i in range(max(r-2, 0), min(r+3, height)):
            for j in range(max(c-2, 0), min(c+3, width)):
                if i != r or j != c:
                    cells.append((i, j))
        linked[r][c] = cells

    return linked[r][c]

def countUnclear(cells):
    count = 0
    for cell in cells:
        if not clear(cell):
            count += 1
    return count

def countFlag(cells):
    count = 0
    for r, c in cells:
        if _flag[r][c]:
            count += 1
    return count

def checkNeighbours(cell):
    for neighbour in neighbourCells(cell):
        checkCell(neighbour)

def neighbourChecked(cell):
    for neighbour in neighbourCells(cell):
        if neighbour in stack :
            return False
    return True



def checkCell(cell):
    if not cell in stack and clear(cell):
        stack.append(cell)

def cutNeighbours(cell):
    result = []
    for neighbour in neighbourCells(cell):
        if cutTree(neighbour):
            result.append(neighbour)
    return result

def cutTree(cell):
    global cleared
    r, c = cell
    if not flag(cell) and not clear(cell):
        # if cell in stack:
        #     stack.remove(cell)
        #     print(f"{position(cell)}\tThe cell was in the stack, is that normal ?")
        #     return False
        if tree[r][c]:
            printOrchard(True)
            print(f"OUCH - I just cut an apple tree at {position(cell)}")
            exit()
        else:
            cleared += 1
            _clear[r][c] = True
            checkNeighbours(cell)
            checkCell(cell)
            return True

def markTree(cell):
    global flags
    r, c = cell
    _flag[r][c] = True
    flags += 1
    checkNeighbours((r, c))
    if not tree[r][c]:
        print(f"{position(cell)}\tThat tree is not an apple tree !")
        printGroup(neighbourCells(cell),True)


def beginnerTechniques(cell):
    global ClearingTechnique
    global LumberjackTechnique
    global ForresterTechnique
    
    n = neighbourCells(cell)
    u = countUnclear(n)
    f = countFlag(n)
    a = apples(cell)

    if a == 0:
        result = cutNeighbours(cell)
        if result != []:
            if verbose:
                print(f"{position(cell)}\tCLEARING : no apple, cutting off {positions(result)}")
            ClearingTechnique += 1
            return 

    if a - f == 0:
        result = cutNeighbours(cell)
        if result != []:
            if verbose:
                print(f"{position(cell)}\tLUMBERJACK : all apple trees marked, cutting off {positions(result)}")
            LumberjackTechnique +=1
            return 

    if a == u > 0:
        for c in n:
            if not clear(c) and not flag(c):
                if verbose:
                    print(
                        f"{position(cell)}\tFORRESTER : as many apples as trees, marking {position(c)}")
                ForresterTechnique += 1
                markTree(c)
                return



def minApples(group, cell):
    # Assuming all cells in group are not clear and not flag
    n = neighbourCells(cell)
    u = [c for c in n if not clear(c) and not flag(c)]
    x = set(u) - set(group)
    
    a = apples(cell)
    f = countFlag(n)
    
    return max(0, a - f - len(x))

def maxApples(group, cell):
    # Assuming all cells in group are not clear and not flag
    n = neighbourCells(cell)
    
    a = apples(cell)
    f = countFlag(n)
    
    return min(len(group),a - f)
  
def Twins(A):
    global TwinsTechnique
    listA = borders()
    for A in listA:
        nA = neighbourCells(A)
        unA = [c for c in nA if not clear(c) and not flag(c)]
        listB = [c for c in linkedCells(A) if clear(c) and apples(c) > 0 and not c in stack]
        for B in listB:
            nB = neighbourCells(B)
            unB = [c for c in nB if not clear(c) and not flag(c)]
            nAiB = set(unA) & set(unB) 
            if nAiB :
                a = apples(A)
                f = countFlag(nA)
                minB = minApples(nAiB,B)
                maxB = maxApples(nAiB,B)
                xA = [c for c in unA if not c in nAiB]
                if len(xA) > 0 :
                    if a - f - minB == 0:
                        TwinsTechnique +=1
                        printGroup([A,B])
                        print(f"LUMBERJACK TWINS")
                        print(f"  {position(A)} and {position(B)} share {len(nAiB)} neighbours {positions(nAiB)}")
                        print(f"  {position(B)} has minimum {minB} apple trees in the shared neighbours")
                        print(f"  {position(A)} has no remaining apple trees in {positions(xA)}")
                        if len(xA):print(f"> Cutting off {positions(xA)}")
                        print()
                        for c in xA: cutTree(c)
                        
                
                    if a - f - maxB == len(xA):
                        TwinsTechnique +=1
                        printGroup([A,B])
                        print(f"FORRESTER TWINS")
                        print(f"  {position(A)} and {position(B)} share {len(nAiB)} neighbours {positions(nAiB)}")
                        print(f"  {position(B)} has maximum {maxB} apple trees in the shared neighbours")
                        print(f"  {position(A)} has {a-f-maxB} remaining apple trees in {len(xA)} trees {positions(xA)}")
                        if len(xA):print(f"> Marking {positions(xA)}")
                        print()
                        for c in xA: markTree(c)
                        
            

    
def Triplets(A):
    global TripletsTechnique
    listA = borders()
    for A in listA:
        unA = [c for c in neighbourCells(A) if not clear(c) and not flag(c)]
        listB = [c for c in linkedCells(A) if clear(c) and apples(c) > 0 and not c in stack]
        for B in listB:
            nB = neighbourCells(B)
            unB = [c for c in nB if not clear(c) and not flag(c)]
            nAiB = set(unA) & set(unB) 
            if nAiB :
                listC = [c for c in linkedCells(B) if clear(c) and apples(c) >0 and not c in stack and c != A ]    
                for C in listC:
                    unC = [c for c in neighbourCells(C) if not clear(c) and not flag(c)]
                    nBiC = set(unB) & set(unC) 
                    if nBiC and not nBiC & nAiB :
                        xB = [c for c in unB if not c in nAiB and not c in nBiC]
                        if len(xB)>0:    
                            a = apples(B)
                            f = countFlag(nB)
                            minA = minApples(nAiB,A)
                            minC = minApples(nBiC,C) 
                            if a - f - minA - minC == 0 :
                                TripletsTechnique +=1
                                printGroup([A,B,C])
                                print(f"LUMBERJACK TRIPLETS")
                                print(f"  {position(B)} shares {len(nAiB)} neighbours with {position(A)} and {len(nBiC)} with {position(C)}")
                                print(f"   - {position(A)} has minimum {minA} apple trees in the shared neighbours {positions(nAiB)}")
                                print(f"   - {position(C)} has minimum {minC} apple trees in the shared neighbours {positions(nBiC)}")
                                print(f"> Cutting off {positions(xB)}")
                                print()
                                for c in xB: cutTree(c)
                                
                            
                            maxA = maxApples(nAiB,A)
                            maxC = maxApples(nBiC,C)
                            if a - f - maxA - maxC == len(xB):
                                TripletsTechnique +=1
                                printGroup([A,B,C])
                                print(f"FORRESTER TRIPLETS")
                                print(f"  {position(B)} shares neighbours with {position(A)} and {position(C)}")
                                print(f"   - {position(A)} has maximum {maxA} apple trees in the shared neighbours {positions(nAiB)}")
                                print(f"   - {position(C)} has maximum {maxC} apple trees in the shared neighbours {positions(nBiC)}")
                                print(f"> Marking {positions(xB)}")
                                print()
                                for c in xB: markTree(c)
                                
                                
            
    


def getDragons():
    # We call 'dragons' the groups of intersecting group of uncut trees adjacent to a cleared cell
    # A. We determinate the dragons
    # B. We count min number of apple trees in each dragon, and add them
    #    If this sum equals the number of remaining apple trees, then
    #    every cell that is not in a dragon can be cleared
    # C. We count the max number of apple trees in each dragon, and add them
    #    If this number + the number of other remaining trees equals the 
    #    number of remaining apple trees, then all other remaining trees are apple trees

    # The term 'dragon' comes from the game of Go

    groups = []
    inDragon = [[False for _ in range(width)] for _ in range(height)]
    nGroups  = [[0     for _ in range(width)] for _ in range(height)]
    applesInGroup = []

    # A DETERMINE THE DRAGONS
    # Collect groups
    for cell in borders():
        n = neighbourCells(cell)
        f = countFlag(n)
        group = [cellB for cellB in n if not clear(cellB) and not flag(cellB)]
        if group != []:
            if not group in groups:
                groups.append(group)
                applesInGroup.append(apples(cell) - f)
                for i, j in group:
                    inDragon[i][j] = True
                    nGroups[i][j] += 1
            else:
                # If that group already exists, as the stack is empty, all cells pointing to that group should have the same remaining number of apples
                # if applesInGroup[groups.index(group)] != apples((r,c)) - f:
                #     print(
                #         f"Something went terribly wrong. That number i just saw is very bad news")
                pass

    # Find dragons : Group groups if they intersect.
    dragonNumber = [i for i in range(len(groups))]
    for i in range(len(groups)):
        for j in range(len(groups)):
            if i != j:
                if set(groups[i]) & set(groups[j]):
                    dragonNumber[j] = dragonNumber[i]
    dragons = []
    for i in range(len(groups)):
        dragon = []
        for j in range(len(groups)):
            if dragonNumber[j] == i:
                dragon.append(groups[j])
        if len(dragon) > 0:
            dragons.append(dragon)
    return dragons, groups, applesInGroup, nGroups, inDragon

def Dragons():
    dragons, groups, applesInGroup, nGroups, inDragon = getDragons()
    # B COUNT THE MIN NUMBER OF APPLE TREES
    # To determine the minimum number of apple trees, populate first the cells that intersect the most groups
    
    hypFlag = [[False for _ in range(width)] for _ in range(height)]
    hypClear = [[False for _ in range(width)] for _ in range(height)]

    minAppleTrees = [0 for _ in range(len(dragons))]
    totalMin = 0
    index = 0
    for dragon in dragons:
        if len(dragon) == 1:
            minAppleTrees[index] = applesInGroup[groups.index(dragon[0])]
        else:
            for group in dragon:
                n = applesInGroup[groups.index(group)]
                for r, c in group:
                    if hypFlag[r][c]:
                        n -= 1

                while n > 0:
                    max = 0
                    for r, c in group:
                        if nGroups[r][c] > max and not hypFlag[r][c] and not hypClear[r][c]:
                            max = nGroups[r][c]
                            bestr, bestc = r, c
                    hypFlag[bestr][bestc] = True
                    minAppleTrees[index] += 1
                    n -= 1

                for r, c in group:
                    if not hypFlag[r][c] and not hypClear[r][c]:
                        hypClear[r][c] = True

        totalMin += minAppleTrees[index]
        index+=1
    
    # Compare
    global number
    global flags
    if totalMin == number - flags:
        # Clear all cells not in a dragon
        cutTrees = []
        border = []
        for r in range(height):
            for c in range(width):
                cell = (r,c)
                if not clear(cell) and not flag(cell):
                    if not inDragon[r][c] :
                        cutTrees.append(cell)
                    else : 
                        border.append(cell)
        
        if len(cutTrees)>0 :
            print()
            printGroup([c for dragon in dragons for group in dragon for c in group])
            print(f"LUMBERJACK DRAGONS")
            print(f"  {number - flags} apple trees remaining in the orchard, and minimum {totalMin} in the following groups :")
            index = 0
            for dragon in dragons:
                cells = sorted(set([cell for group in dragon for cell in group]))
                print(f"   - minimum {minAppleTrees[index]} in group {positions(cells)}")
                index +=1
            print(f"> Cutting off all other remaining trees : {positions(cutTrees)}")
            print()
            
            for cell in cutTrees:
                cutTree(cell)
            global DragonsTechnique
            DragonsTechnique += 1
   
        
        
        
    # B COUNT THE MAX NUMBER OF APPLE TREES
    # To determine the minimum number of apple trees, populate first the cells that intersect the most groups
    
    hypFlag  = [[False for _ in range(width)] for _ in range(height)]
    hypClear = [[False for _ in range(width)] for _ in range(height)]

    maxAppleTrees = [0 for _ in range(len(dragons))]
    totalMax = 0
    index = 0
    for dragon in dragons:
        if len(dragon) == 1:
            maxAppleTrees[index] = applesInGroup[groups.index(dragon[0])]
        else:
            for group in dragon:
                n = applesInGroup[groups.index(group)]
                for r, c in group:
                    if hypFlag[r][c]:
                        n -= 1

                while n > 0:
                    min = 8
                    for r, c in group:
                        if nGroups[r][c] < min and not hypFlag[r][c] and not hypClear[r][c]:
                            min = nGroups[r][c]
                            bestr, bestc = r, c
                    hypFlag[bestr][bestc] = True
                    maxAppleTrees[index] += 1
                    n -= 1

                for r, c in group:
                    if not hypFlag[r][c] and not hypClear[r][c]:
                        hypClear[r][c] = True

        totalMax += maxAppleTrees[index]
        index+=1
    
    # Compare
    others = []
    for r in range(height):
        for c in range(width):
            cell = (r,c)
            if not clear(cell) and not flag(cell) and not inDragon[r][c] :
                others.append(cell)

    if number - flags - totalMax == len(others):
        # Flag all cells not in a dragon   
        if len(others)>0 :
            print()
            printGroup([c for dragon in dragons for group in dragon for c in group])
            print(f"FORRESTER DRAGONS")
            print(f"  {number - flags} apple trees remaining in the orchard, and maximum {totalMax} in the following groups :")
            index = 0
            for dragon in dragons:
                cells = sorted(set([cell for group in dragon for cell in group]))
                print(f"   - maximum {maxAppleTrees[index]} in group {positions(cells)}")
                index +=1
            if len(others) == 1:
                print(f"> Marking the other remaining tree : {positions(others)}")
            else:
                print(f"> Marking the {len(others)} other remaining trees : {positions(others)}")
            print()
            
            for cell in others:
                markTree(cell)
            DragonsTechnique += 1
       

combinations = []
cellIndex = []

def DragonsBruteForce():
    dragons, groups, applesInGroup, nGroups, inDragon = getDragons()
    global combinations
    global cellIndex
    totalMin = 0
    totalMax = 0
    minApples = [0 for _ in range(len(dragons))]
    maxApples = [0 for _ in range(len(dragons))]
    totalMinCells = []
    totalMaxCells = []
    for index,dragon in enumerate(dragons):
        if len(dragon) == 1:
            minApples[index] = applesInGroup[groups.index(dragon[0])]
            maxApples[index] = applesInGroup[groups.index(dragon[0])]
            minCells = []
            maxCells = []
        else:
            cellIndex = sorted(set([cell for group in dragon for cell in group]))
            combFlag = [False for _ in range(len(cellIndex))]
            combClear = [False for _ in range(len(cellIndex))]
            combinations = []
            applesInDragon = [applesInGroup[groups.index(group)] for group in dragon]
            recurseFindCombinations(dragon,applesInDragon, combFlag, combClear )
            
            l = len(cellIndex)
            maxApples[index] = 0
            minApples[index] = l
            xor = [0 for _ in range(l)]
            for combination in combinations:
                n = 0
                for i in range(l):
                    if combination[i]:
                        n += 1
                        xor[i] += 1
                
                if n == maxApples[index]:
                    maxCells = []
                if n > maxApples[index]:
                    maxApples[index] = n
                    maxCells = []
                    for cell,b in zip(cellIndex,combination):
                        if b:
                            maxCells.append(cell)
            
                if n == minApples[index]:
                    minCells = []
                elif n < minApples[index]:
                    minApples[index] = n
                    minCells = []
                    for cell,b in zip(cellIndex,combination):
                        if b:
                            minCells.append(cell)

            for x,b,cell in zip(xor,combinations[0],cellIndex):
                if x == l:
                    if b:
                        print(f"Brute Force Dragon says to mark {position(cell)}")
                    else:
                        print(f"Brute Force Dragon says to cut {position(cell)}")
                        
        totalMin += minApples[index]
        totalMax += maxApples[index]
        totalMaxCells += maxCells
        totalMinCells += minCells
    
        
    others = []
    for r in range(height):
        for c in range(width):
            cell = (r,c)
            if not clear(cell) and not flag(cell) and not inDragon[r][c] :
                others.append(cell)
                
    global BruteForceTechnique
    global number
    global flags
    if totalMin == number - flags:
        if totalMinCells != []:
            print()
            printGroup([c for dragon in dragons for group in dragon for c in group])
            print(f"BRUTEFORCE DRAGONS")
            print(f"  Every combination has been tested in the following groups :")
            for index,dragon in enumerate(dragons):
                cells = sorted(set([cell for group in dragon for cell in group]))
                m = minApples[index]
                M = maxApples[index]
                if m == M:
                    print(f"   - Dragon {positions(cells)} has {m} apple trees")
                else:
                    print(f"   - Dragon {positions(cells)} has {m} to {M} apple trees")
            print(f"  There is only one combination that uses the minimum possible number of apple trees, ie {totalMin}")
            print(f"  There are {number - flags} remaining apple trees")
            print(f"> Marking {positions(totalMinCells)}")
            print()
       
            for cell in totalMinCells:
                markTree(cell)
            BruteForceTechnique += 1
       
        
          
    if number - flags - totalMax == len(others):
        if totalMaxCells != []:
            print()
            printGroup([c for dragon in dragons for group in dragon for c in group])
            print(f"BRUTEFORCE DRAGONS")
            print(f"  Every combination has been tested in the following groups :")
            for index,dragon in enumerate(dragons):
                cells = sorted(set([cell for group in dragon for cell in group]))
                m = minApples[index]
                M = maxApples[index]
                if m == M:
                    print(f"   - Dragon {positions(cells)} has {m} apple trees")
                else:
                    print(f"   - Dragon {positions(cells)} has {m} to {M} apple trees")
            print(f"  There is only one combination that uses the maximum possible number of apple trees, ie {totalMax}")
            print(f"  There are {len(others)} other unmarked trees, and {number - flags} remaining apple trees")
            print(f"> Marking {positions(totalMaxCells)}")
            print()
            
            for cell in totalMaxCells:
                markTree(cell)
            BruteForceTechnique += 1
            
def recurseFindCombinations(dragon, applesInDragon, combFlag, combClear):
    if len(dragon) == 0:
        combinations.append(combFlag)
        return
    else:
        group = dragon[0]
        tail  = dragon[1:]
        n = applesInDragon[0]
        t = applesInDragon[1:]
        
        for cell in group:
            if combFlag[cellIndex.index(cell)]:
                n -= 1
                
                
        if n < 0:
            return
        elif n == 0:
            newCombClear = [b for b in combClear]
            for c in group:
                newCombClear[cellIndex.index(c)] = True
            recurseFindCombinations(tail,t,combFlag,newCombClear)    
        else:
            for cell in group:
                index = cellIndex.index(cell)
                if not combClear[index] :
                    newCombFlag = [b for b in combFlag]
                    newCombFlag[index] = True
                    newCombClear = [b for b in combClear]
                    for c in group:
                        newCombClear[cellIndex.index(c)] = True
                    
                    if n == 1:
                        recurseFindCombinations(tail,t,newCombFlag,newCombClear)
                    else:
                        applesInDragon[0] -=1
                        recurseFindCombinations(dragon,applesInDragon,newCombFlag,combClear)
            
    


def collectApples(s=0):
    # Beginnner 8 * 8 * 10
    # Intermediate 16 * 16 * 40
    # Advanced 16 * 31 * 99
    height = 16
    width  = 31
    number = 99

    global seed
    seed = s
    if seed == 0:
        seed = random.randrange(10000)
    print(f"Seed = {seed}")
    random.seed(seed)

    r = random.randrange(height)
    c = random.randrange(width)
    createOrchard(height, width, number, r, c)

    
    print()
    print(f"The forrester had planted {number} apple trees in the forrest, but he can't remember where.")
    print(f"He needs to make space for apple trees 🎄 to grow, by cutting off the other trees 🌲 .")
    print(f"Every apple tree drops an apple on each of the eight surrounding cells.")
    print(f"He will mark the apple trees with 🍏")
    print()
    print(f"The first tested cell ({position((r,c))}) is guaranteed to be a clearing")
    print()
    cutTree((r, c))
    stack.append((r, c))

    while len(stack) > 0:
        cell = stack.pop(0)
        beginnerTechniques(cell) 
        if len(stack) == 0 and number > flags:
            Twins(cell) 
        if len(stack) == 0 and number > flags:
            Triplets(cell)
        if len(stack) == 0 and number > flags:
            Dragons()
        if len(stack) == 0 and number > flags:
            DragonsBruteForce()
                
        # i discarded the return True -> continue syntax used at first because it doesn't work with the dragons techniques that can change the board without changing the stack

    if number == flags:
        if cleared < width * height - number:
            cutTrees = []
            for c in range(width):
                for r in range(height):
                    cell = (r,c)
                    if not clear(cell) and not flag(cell):
                        cutTree(cell)
                        cutTrees.append(cell)
            if verbose :
                print(f"\tNo remaining apple trees. Cutting of remaining unmarked trees {positions(cutTrees)}")
                        

    printOrchard()
    

verbose = True
collectApples(4435)
