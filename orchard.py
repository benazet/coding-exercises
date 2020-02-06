import random
import itertools


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
emoji     = True

ClearingTechnique   = 1
LumberjackTechnique = 0
ForresterTechnique  = 0
TwinsTechnique      = 0
TripletsTechnique   = 0
DragonsTechnique    = 0

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
    print(f"   🌲  {width * height - cleared - flags} unchecked trees")
    print(f"   🍎  {number - flags} apple trees")
    print(f"   🍏  {flags} flags")
    print()
    print(f"   seed = {seed}")
    print()
    print(f"Techniques used :")
    print(f"   {'Clearing':<12}{ClearingTechnique:>3}")
    print(f"   {'Lumberjack':<12}{LumberjackTechnique:>3}")
    print(f"   {'Forrester':<12}{ForresterTechnique:>3}")
    print(f"   {'Twins':<12}{TwinsTechnique:>3}")
    print(f"   {'Triplets':<12}{TripletsTechnique:>3}")
    print(f"   {'Dragons':<12}{DragonsTechnique:>3}")
    print(f"   {'Brute Force':<12}{0:>3}")
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

    if emoji:
    	symbol = ' 12345678🌲'
    else:
    	symbol = ' 12345678▉'
    val = []
    for r in range(height):
        row = [""]
        for c in range(cMin,cMax):
            cell = symbol[_apples[r][c]]
            if cheat:
                if tree[r][c]:
                    cell = '🍎' if emoji else ''
            if _flag[r][c]:
                if tree[r][c] or not cheat:
                    cell = '🍏' if emoji else '⚑'
                else:
                    cell = '🍎' if emoji else '⚐'
                    
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

def position(cell):
    r, c = cell
    return f"{letter(r)}{c+1}"

def positions(group):
    return ' '.join(position(cell) for cell in group)

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

def cutTree(cell):
    global cleared
    r, c = cell
    if not flag(cell) and not clear(cell):
        if tree[r][c]:
            printOrchard(True)
            print(f"OUCH - I just cut an apple tree at {position(cell)}")
            exit()
        else:
            cleared += 1
            _clear[r][c] = True
            checkNeighbours(cell)
            checkCell(cell)

def markTree(cell):
    global flags
    r, c = cell
    _flag[r][c] = True
    flags += 1
    checkNeighbours((r, c))
    if not tree[r][c]:
        print(f"{position(cell)}\tThat tree is not an apple tree !")
        printGroup(neighbourCells(cell),True)


def Beginner(cell):
    global ClearingTechnique
    global LumberjackTechnique
    global ForresterTechnique
    
    n = neighbourCells(cell)
    u = countUnclear(n)
    f = countFlag(n)
    a = apples(cell)
    
    if a == 0:
        group = [c for c in n if not clear(c) and not flag(c)]
        if group != []:
            if verbose:
                print(f"CLEARING : no apple around {position(cell)}, cutting off {positions(group)}")
            ClearingTechnique += 1
            for c in group:
                cutTree(c)
            return 

    if a - f == 0:
        group = [c for c in n if not clear(c) and not flag(c)]
        if group != []:
            if verbose:
                print(f"LUMBERJACK : all apple trees around {position(cell)} marked, cutting off {positions(group)}")
            LumberjackTechnique +=1
            for c in group:
                cutTree(c)
            return 

    if a == u > 0:
        group = [c for c in n if not clear(c) and not flag(c)]
        if group != []:
            if verbose:
                print(
                    f"FORRESTER : as many apples as trees around {position(cell)}, marking {positions(group)}")
            ForresterTechnique += 1
            for c in group:
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
                        if verbose:
                            printGroup([A,B])
                            print(f"LUMBERJACK TWINS")
                            print(f"  {position(A)} and {position(B)} share {len(nAiB)} neighbours {' '.join(position(c) for c in nAiB)}")
                            print(f"  {position(B)} has minimum {minB} apple trees in the shared neighbours")
                            print(f"  {position(A)} has no remaining apple trees in {' '.join(position(c) for c in xA)}")
                            if len(xA):print(f"> Cutting off {' '.join(position(c) for c in xA)}")
                            print()
                        for c in xA: cutTree(c)
                        return
                
                    if a - f - maxB == len(xA):
                        TwinsTechnique +=1
                        if verbose:
                            printGroup([A,B])
                            print(f"FORRESTER TWINS")
                            print(f"  {position(A)} and {position(B)} share {len(nAiB)} neighbours {' '.join(position(c) for c in nAiB)}")
                            print(f"  {position(B)} has maximum {maxB} apple trees in the shared neighbours")
                            print(f"  {position(A)} has {a-f-maxB} remaining apple trees in {len(xA)} trees {' '.join(position(c) for c in xA)}")
                            if len(xA):print(f"> Marking {' '.join(position(c) for c in xA)}")
                            print()
                        for c in xA: markTree(c)
                        return
            

    
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
                                if verbose:
                                    printGroup([A,B,C])
                                    print(f"LUMBERJACK TRIPLETS")
                                    print(f"  {position(B)} shares {len(nAiB)} neighbours with {position(A)} and {len(nBiC)} with {position(C)}")
                                    print(f"   - {position(A)} has minimum {minA} apple trees in the shared neighbours {' '.join(position(c) for c in nAiB)}")
                                    print(f"   - {position(C)} has minimum {minC} apple trees in the shared neighbours {' '.join(position(c) for c in nBiC)}")
                                    print(f"> Cutting off {' '.join(position(c) for c in xB)}")
                                    print()
                                for c in xB: cutTree(c)
                                return
                            
                            maxA = maxApples(nAiB,A)
                            maxC = maxApples(nBiC,C)
                            if a - f - maxA - maxC == len(xB):
                                TripletsTechnique +=1
                                if verbose:
                                    printGroup([A,B,C])
                                    print(f"FORRESTER TRIPLETS")
                                    print(f"  {position(B)} shares neighbours with {position(A)} and {position(C)}")
                                    print(f"   - {position(A)} has maximum {maxA} apple trees in the shared neighbours {' '.join(position(c) for c in nAiB)}")
                                    print(f"   - {position(C)} has maximum {maxC} apple trees in the shared neighbours {' '.join(position(c) for c in nBiC)}")
                                    print(f"> Marking {' '.join(position(c) for c in xB)}")
                                    print()
                                for c in xB: markTree(c)
                                return
                                
            
    


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
            if verbose :
                print()
                printGroup([c for dragon in dragons for group in dragon for c in group])
                print(f"LUMBERJACK DRAGONS")
                print(f"  {number - flags} apple trees remaining in the orchard, and minimum {totalMin} in the following groups :")
                index = 0
                for dragon in dragons:
                    cells = sorted(set([cell for group in dragon for cell in group]))
                    print(f"   - minimum {minAppleTrees[index]} in group {' '.join(position(cell) for cell in cells)}")
                    index +=1
                print(f"> Cutting off all other remaining trees : {' '.join(position(cell) for cell in cutTrees)}")
                print()
            
            for cell in cutTrees:
                cutTree(cell)
            global DragonsTechnique
            DragonsTechnique += 1
            return 
        
        
        
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
            if verbose:
                print()
                printGroup([c for dragon in dragons for group in dragon for c in group])
                print(f"FORRESTER DRAGONS")
                print(f"  {number - flags} apple trees remaining in the orchard, and maximum {totalMax} in the following groups :")
                index = 0
                for dragon in dragons:
                    cells = sorted(set([cell for group in dragon for cell in group]))
                    print(f"   - maximum {maxAppleTrees[index]} in group {' '.join(position(cell) for cell in cells)}")
                    index +=1
                if len(others) == 1:
                    print(f"> Marking the other remaining tree : {' '.join(position(cell) for cell in others)}")
                else:
                    print(f"> Marking the {len(others)} other remaining trees : {' '.join(position(cell) for cell in others)}")
                print()
            
            for cell in others:
                markTree(cell)
            DragonsTechnique += 1
            return 
        
        
        
        
   


def BruteDragons():
    dragons, groups, applesInGroup, nGroups, inDragon = getDragons()
    
    minApples = 0
    maxApples = 0
    minCells = []
    maxCells = []
    dragonMinApples = [0 for _ in range(len(dragons))]
    dragonMaxApples = [0 for _ in range(len(dragons))]
    dragonMinCells  = [[]for _ in range(len(dragons))]
    dragonMaxCells  = [[]for _ in range(len(dragons))]
    
    printGroup([cell for dragon in dragons for group in dragon for cell in group])
    for index,dragon in enumerate(dragons):
        combinations = []
        if len(dragon) == 1:
            # no unique solution, but unique number of apple trees
            dragonMaxApples[index] = applesInGroup[groups.index(dragon[0])]
            dragonMinApples[index] = applesInGroup[groups.index(dragon[0])]
            dragonMaxCells[index] = []
            dragonMinCells[index] = []
        else:
            # here comes the brute force
            
            cells = sorted(set([cell for group in dragon for cell in group]))
            
            combinations.append([0 for _ in range(len(cells))])
            #  0 = unused
            #  1 = marked
            # -1 = max for the group reached
            
            printGroup([cell for dragon in dragons for group in dragon for cell in group])
            
            for group in dragon:
                newCombinations = []
                for combination in combinations:
                    # counting remaining apples for this group in this combination
                    a = applesInGroup[groups.index(group)]
                    for cell in group:
                        if combination[cells.index(cell)] == 1:
                            a -= 1
                    
                    # looking at all the theoretical combination
                    for iter in [p for p in itertools.product((True, False),repeat=len(group)) if sum(p) == a]:
                        newCombination = combination[:] #shallow copy
                        count = 0
                        # Apply the combination, if it fits
                        for cell,bool in zip(group,iter):
                            if newCombination[cells.index(cell)] == 0:
                                if bool :
                                    newCombination[cells.index(cell)] = 1
                                    count +=1
                                else:
                                    newCombination[cells.index(cell)] = -1
                        
                        # If it fits, append the existing combination
                        if count == a:
                            newCombinations.append(newCombination)
                
                # once all groups have been tested, the combination is complete
                combinations = newCombinations
            
            # Computing global stats
            dragonMinApples[index] = len(combination)
            dragonMaxApples[index] = 0
            xor = [0 for _ in range(len(cells))]
            for combination in combinations:
                n = 0
                
                for i,cell in enumerate(combination):
                    if cell == 1:
                        n +=1
                        xor[i] +=1

                if n > dragonMaxApples[index]:
                    dragonMaxApples[index] = n
                    dragonMaxCells = [c for group in dragon for c in group if combination[cells.index(c)] == 1]
                elif n == 0:
                    dragonMaxCells = []
                    # There is no unique solution
                    
                if n < dragonMinApples[index]:
                    dragonMinApples[index] = n
                    dragonMinCells = [c for group in dragon for c in group if combination[cells.index(c)] == 1]
                elif n == 0:
                    dragonMaxCells = []
                    # There is no unique solution
                    
                    
                # Dragon methods
                
                
        minApples += dragonMinApples[index]
        maxApples += dragonMaxApples[index]
        minCells += dragonMinCells[index]
        maxCells += dragonMaxCells[index]    
        
       
        
        
    
    # Global methods        

            
            

     

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

    if verbose :
        print()
        print(f"The forrester had planted {number} apple trees in the forrest, but he can't remember where.")
        print(f"He needs to make space for apple trees 🎄 to grow, by cutting off the other trees 🌲 .")
        print(f"Every apple tree drops an apple on each of the eight surrounding cells.")
        print(f"He will mark the apple trees with 🍏")
        print()
        print(f"The first tested cell ({position((r,c))})is guaranteed to be a clearing")
        print()
    cutTree((r, c))
    stack.append((r, c))

    while len(stack) > 0:
        cell = stack.pop(0)
        Beginner(cell) 
        if len(stack) > 0 or number == flags: continue
        Twins(cell) 
        if len(stack) > 0 or number == flags: continue
        Triplets(cell)
        if len(stack) > 0 or number == flags: continue
        Dragons()
        if len(stack) > 0 or number == flags: continue
        BruteDragons()
                
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
                print(f"\tNo remaining apple trees. Cutting of remaining unmarked trees : {'-'.join(position(cell) for cell in cutTrees)}")
                        

    printOrchard()
    

verbose = False
emoji = True
collectApples(2599)
