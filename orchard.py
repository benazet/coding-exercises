import random
import itertools


# global variables
tree = []
trees = 0
_flag = []
flags = 0
_apples = []
_clear = []
width = 0
height = 0
cleared = 0
stack = []
neighbour = []
linked = []
verbose = False
seed = 0
emoji = True

ClearingTechnique = 1
LumberjackTechnique = 0
ForresterTechnique = 0
TwinsTechnique = 0
TripletsTechnique = 0
DragonsTechnique = 0
StaticTreesTechnique = 0
AllAccountedForTechnique = 0
BruteDragonsTechnique = 0
GettingTrickyTechnique = 0


def createOrchard(h, w, n=-1, r=-1, c=-1):
    global width
    global height
    global trees
    global tree
    global _flag
    global _apples
    global _clear
    global neighbour
    global linked

    width = w
    height = h

    tree = [[False for _ in range(width)] for _ in range(height)]
    _flag = [[False for _ in range(width)] for _ in range(height)]
    _clear = [[False for _ in range(width)] for _ in range(height)]
    _apples = [[-1 for _ in range(width)] for _ in range(height)]
    neighbour = [[[] for _ in range(width)] for _ in range(height)]
    linked = [[[] for _ in range(width)] for _ in range(height)]

    if n == -1:
        n = width * height / 3
    n = min(n, width * height - 1)
    trees = n

    while n > 0:
        x = random.randrange(width)
        y = random.randrange(height)
        if not tree[y][x]:
            # if r == -1 or c == -1 or y != r or x != c:
            if r == -1 or c == -1 or abs(y - r) > 1 or abs(x - c) > 1:
                tree[y][x] = True
                n -= 1


def printOrchard(cheat=False):
    global seed
    global trees
    printCells(0, height, 0, width, cheat)
    print(f"   🍎  {trees - flags} / {trees} remaining apple trees")
    print(f"   🌲  {width * height - cleared - flags} / {width*height} unchecked trees")
    print(f"   🍏  {flags} marked apple trees")
    print()
    print(f"   seed = {seed}")
    print()
    print(f"Techniques used :")
    print(f"   {'Clearing':<20}{ClearingTechnique:>3}", end="")
    print(f"   {'Dragons':<20}{DragonsTechnique:>3}")
    print(f"   {'Lumberjack':<20}{LumberjackTechnique:>3}", end="")
    print(f"   {'Static trees':<20}{StaticTreesTechnique:>3}")
    print(f"   {'Forrester':<20}{ForresterTechnique:>3}", end="")
    print(f"   {'Getting tricky':<20}{GettingTrickyTechnique:>3}")
    print(f"   {'Twins':<20}{TwinsTechnique:>3}", end="")
    print(f"   {'All accounted for':<20}{AllAccountedForTechnique:>3}")
    print(f"   {'Triplets':<20}{TripletsTechnique:>3}", end="")
    print(f"   {'Brute dragons':<20}{BruteDragonsTechnique:>3}")
    print()


def printGroup(group, cheat=False):

    neighbours = [n for c in group for n in neighbourCells(c)]
    rMin = min(r for r, c in neighbours)
    rMax = max(r for r, c in neighbours) + 1
    cMin = min(c for r, c in neighbours)
    cMax = max(c for r, c in neighbours) + 1

    printCells(rMin, rMax, cMin, cMax, cheat)


def printCells(rMin, rMax, cMin, cMax, cheat):
    def expandLine(line):
        return (
            [line[4], line[0]][cMin == 0]
            + "".join(line[1:5] for _ in range(cMax - cMin - 1))
            + [line[1:5], line[5:9]][cMax == width]
        )

    line0 = expandLine("┌───┬───┐")
    line1 = expandLine("│ . │ . │")
    line2 = expandLine("├───┼───┤")
    line3 = expandLine("└───┴───┘")

    if emoji:
        symbol = " 12345678🌲"
    else:
        symbol = " 12345678▉"
    val = []
    for r in range(height):
        row = [""]
        for c in range(cMin, cMax):
            cell = symbol[_apples[r][c]]
            if cheat:
                if tree[r][c]:
                    cell = "🍎" if emoji else ""
            if _flag[r][c]:
                if tree[r][c] or not cheat:
                    cell = "🍏" if emoji else "⚑"
                else:
                    cell = "🍎" if emoji else "⚐"

            row += cell
        val.append(row)

    print()
    print("    " + " ".join(f"{c+1:^3}" for c in range(cMin, cMax)))
    print("   " + [line2, line0][rMin == 0])
    for r in range(rMin, rMax):
        print(f"{letter(r):^3}", end="")
        print("".join(a + b for a, b in zip(val[r], line1.split("."))), end="")
        print(f"{letter(r):^3}")
        print("   " + [line2, line3][r == height - 1])
    print("    " + " ".join(f"{c+1:^3}" for c in range(cMin, cMax)))
    print()


def position(cell):
    r, c = cell
    return f"{letter(r)}{c+1}"


def positions(group):
    return " ".join(position(cell) for cell in group)


def letter(r):
    if height <= 26:
        result = chr(r + 65)
    else:
        result = chr(r // 26 + 65) + chr(r % 26 + 65)
    return result


def apples(cell):
    r, c = cell
    if _apples[r][c] == -1:
        _apples[r][c] = 0
        for i, j in neighbourCells(cell):
            if tree[i][j]:
                _apples[r][c] += 1

    return _apples[r][c]


def clear(cell):
    r, c = cell
    return _clear[r][c]


def flag(cell):
    r, c = cell
    return _flag[r][c]


def neighbourCells(cell):
    r, c = cell
    if neighbour[r][c] == []:
        cells = []
        for i in range(max(r - 1, 0), min(r + 2, height)):
            for j in range(max(c - 1, 0), min(c + 2, width)):
                if i != r or j != c:
                    cells.append((i, j))
        neighbour[r][c] = cells

    return neighbour[r][c]


def borders():
    borderCells = []
    for r in range(height):
        for c in range(width):
            cell = (r, c)
            if not clear(cell) and not flag(cell):
                border = [c for c in neighbourCells(cell) if clear(c)]
                borderCells += border
    return sorted(set(borderCells))


def linkedCells(cell):
    r, c = cell
    if linked[r][c] == []:
        cells = []
        for i in range(max(r - 2, 0), min(r + 3, height)):
            for j in range(max(c - 2, 0), min(c + 3, width)):
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
        if neighbour in stack:
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
            print(f"OUCH - I just cut an apple tree at {position(cell)} !")
            printOrchard(True)
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
        printGroup(neighbourCells(cell), True)


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
                print(
                    f"CLEARING : no apple around {position(cell)}, cutting off {positions(group)}"
                )
            ClearingTechnique += 1
            for c in group:
                cutTree(c)
            return

    if a - f == 0:
        group = [c for c in n if not clear(c) and not flag(c)]
        if group != []:
            if verbose:
                print(
                    f"LUMBERJACK : all apple trees around {position(cell)} marked, cutting off {positions(group)}"
                )
            LumberjackTechnique += 1
            for c in group:
                cutTree(c)
            return

    if a == u > 0:
        group = [c for c in n if not clear(c) and not flag(c)]
        if group != []:
            if verbose:
                print(
                    f"FORRESTER : as many apples as trees around {position(cell)}, marking {positions(group)}"
                )
            ForresterTechnique += 1
            for c in group:
                markTree(c)
            if group == [(13, 6)]:
                print(positions(group))
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

    return min(len(group), a - f), a - f <= len(group)


def Twins(A):
    global TwinsTechnique
    listA = borders()
    for A in listA:
        nA = neighbourCells(A)
        unA = [c for c in nA if not clear(c) and not flag(c)]
        listB = [
            c for c in linkedCells(A) if clear(c) and apples(c) > 0 and not c in stack
        ]
        for B in listB:
            nB = neighbourCells(B)
            unB = [c for c in nB if not clear(c) and not flag(c)]
            nAiB = set(unA) & set(unB)
            if nAiB:
                a = apples(A)
                f = countFlag(nA)
                minB = minApples(nAiB, B)
                maxB, absoluteMaxB = maxApples(nAiB, B)
                xA = [c for c in unA if not c in nAiB]
                xB = [c for c in unB if not c in unA]
                if len(xA) > 0 or len(xB) > 0:
                    if a - f - minB == 0:
                        TwinsTechnique += 1
                        if verbose:
                            printGroup([A, B])
                            print(f"LUMBERJACK TWINS")
                            print(
                                f"  {position(A)} and {position(B)} share {len(nAiB)} neighbours {' '.join(position(c) for c in nAiB)}"
                            )
                            print(
                                f"  {position(B)} has minimum {minB} apple trees in the shared neighbours"
                            )
                            print(
                                f"  {position(A)} has no remaining apple trees in {' '.join(position(c) for c in xA)}"
                            )
                            print(f"> Cutting off {' '.join(position(c) for c in xA)}")
                            if len(xB) > 0:
                                print(f"> Marking {positions(xB)}")
                            print()
                        for c in xA:
                            cutTree(c)
                        for c in xB:
                            markTree(c)
                        return

                    if a - f - maxB == len(xA):
                        TwinsTechnique += 1
                        if verbose:
                            printGroup([A, B])
                            print(f"FORRESTER TWINS")
                            print(
                                f"  {position(A)} and {position(B)} share {len(nAiB)} neighbours {' '.join(position(c) for c in nAiB)}"
                            )
                            print(
                                f"  {position(B)} has maximum {maxB} apple trees in the shared neighbours"
                            )
                            print(
                                f"  {position(A)} has {a-f-maxB} remaining apple trees in {len(xA)} trees {' '.join(position(c) for c in xA)}"
                            )
                            print(f"> Marking {' '.join(position(c) for c in xA)}")
                            if absoluteMaxB and len(xB) > 0:
                                print(f"> Cutting off {positions(xB)}")
                            print()
                        for c in xA:
                            markTree(c)
                        if absoluteMaxB:
                            for c in xB:
                                cutTree(c)
                        return


def Triplets(A):
    global TripletsTechnique
    listA = borders()
    for A in listA:
        unA = [c for c in neighbourCells(A) if not clear(c) and not flag(c)]
        listB = [
            c for c in linkedCells(A) if clear(c) and apples(c) > 0 and not c in stack
        ]
        for B in listB:
            nB = neighbourCells(B)
            unB = [c for c in nB if not clear(c) and not flag(c)]
            nAiB = set(unA) & set(unB)
            if nAiB:
                listC = [
                    c
                    for c in linkedCells(B)
                    if clear(c) and apples(c) > 0 and not c in stack and c != A
                ]
                for C in listC:
                    unC = [c for c in neighbourCells(C) if not clear(c) and not flag(c)]
                    nBiC = set(unB) & set(unC)
                    if nBiC and not nBiC & nAiB:
                        xB = [c for c in unB if not c in nAiB and not c in nBiC]
                        xA = [c for c in unA if not c in unB]
                        xC = [c for c in unC if not c in unB]
                        if len(xB) > 0 or len(xA) > 0 or len(xC) > 0:
                            a = apples(B)
                            f = countFlag(nB)
                            minA = minApples(nAiB, A)
                            minC = minApples(nBiC, C)
                            if a - f - minA - minC == 0:
                                TripletsTechnique += 1
                                if verbose:
                                    printGroup([A, B, C])
                                    print(f"LUMBERJACK TRIPLETS")
                                    print(
                                        f"  {position(B)} shares {len(nAiB)} neighbours with {position(A)} and {len(nBiC)} with {position(C)}"
                                    )
                                    print(
                                        f"   - {position(A)} has {minA} apple trees in the shared neighbours {' '.join(position(c) for c in nAiB)}"
                                    )
                                    print(
                                        f"   - {position(C)} has {minC} apple trees in the shared neighbours {' '.join(position(c) for c in nBiC)}"
                                    )
                                    if len(xB) > 0:
                                        print(
                                            f"> Cutting off {' '.join(position(c) for c in xB)}"
                                        )
                                    if len(xA) > 0:
                                        print(f"> Marking {positions(xA)}")
                                    if len(xC) > 0:
                                        print(f"> Marking {positions(xC)}")
                                    print()
                                for c in xB:
                                    cutTree(c)
                                for c in xA:
                                    markTree(c)
                                for c in xC:
                                    markTree(c)
                                return

                            maxA, absoluteMaxA = maxApples(nAiB, A)
                            maxC, absoluteMaxC = maxApples(nBiC, C)
                            if a - f - maxA - maxC == len(xB):
                                TripletsTechnique += 1
                                if verbose:
                                    printGroup([A, B, C])
                                    print(f"FORRESTER TRIPLETS")
                                    print(
                                        f"  {position(B)} shares neighbours with {position(A)} and {position(C)}"
                                    )
                                    print(
                                        f"   - {position(A)} has {maxA} apple trees in the shared neighbours {' '.join(position(c) for c in nAiB)}"
                                    )
                                    print(
                                        f"   - {position(C)} has {maxC} apple trees in the shared neighbours {' '.join(position(c) for c in nBiC)}"
                                    )
                                    if len(xB) > 0:
                                        print(
                                            f"> Marking {' '.join(position(c) for c in xB)}"
                                        )
                                    if absoluteMaxA and len(xA) > 0:
                                        print(f"> Cutting off {positions(xA)}")
                                    if absoluteMaxC and len(xC) > 0:
                                        print(f"> Cutting off {positions(xC)}")
                                    print()

                                for c in xB:
                                    markTree(c)
                                if absoluteMaxA:
                                    for c in xA:
                                        cutTree(c)
                                if absoluteMaxC:
                                    for c in xC:
                                        cutTree(c)

                                return


def getDragons():
    # We call 'dragons' the groups of intersecting group of uncut trees adjacent to a cleared cell
    # The term comes from the game of Go

    groups = []
    inDragon = [[False for _ in range(width)] for _ in range(height)]
    nGroups = [[0 for _ in range(width)] for _ in range(height)]
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
        for j in range(i, len(groups)):
            if i != j:
                if set(groups[i]) & set(groups[j]):
                    if dragonNumber[j] != j:
                        for k in range(len(groups)):
                            if dragonNumber[k] == dragonNumber[j]:
                                dragonNumber[k] = dragonNumber[i]
                    else:
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

    if dragons == []:
        return

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
                        if (
                            nGroups[r][c] > max
                            and not hypFlag[r][c]
                            and not hypClear[r][c]
                        ):
                            max = nGroups[r][c]
                            bestr, bestc = r, c
                    hypFlag[bestr][bestc] = True
                    minAppleTrees[index] += 1
                    n -= 1

                for r, c in group:
                    if not hypFlag[r][c] and not hypClear[r][c]:
                        hypClear[r][c] = True

        totalMin += minAppleTrees[index]
        index += 1

    # Compare
    global trees
    global flags
    if totalMin == trees - flags:
        # Clear all cells not in a dragon
        cutTrees = []
        border = []
        for r in range(height):
            for c in range(width):
                cell = (r, c)
                if not clear(cell) and not flag(cell):
                    if not inDragon[r][c]:
                        cutTrees.append(cell)
                    else:
                        border.append(cell)

        if len(cutTrees) > 0:
            if verbose:
                print()
                printGroup([c for dragon in dragons for group in dragon for c in group])
                print(f"LUMBERJACK DRAGONS")
                print(
                    f"  {trees - flags} apple trees remaining in the orchard, and minimum {totalMin} in the following groups :"
                )
                index = 0
                for dragon in dragons:
                    cells = sorted(set([cell for group in dragon for cell in group]))
                    print(
                        f"   - minimum {minAppleTrees[index]} in group {positions(cells)}"
                    )
                    index += 1
                print(
                    f"> Cutting off all other remaining trees : {positions(cutTrees)}"
                )
                print()

            for cell in cutTrees:
                cutTree(cell)
            global DragonsTechnique
            DragonsTechnique += 1
            return

    # B COUNT THE MAX NUMBER OF APPLE TREES
    # To determine the minimum number of apple trees, populate first the cells that intersect the most groups

    hypFlag = [[False for _ in range(width)] for _ in range(height)]
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
                        if (
                            nGroups[r][c] < min
                            and not hypFlag[r][c]
                            and not hypClear[r][c]
                        ):
                            min = nGroups[r][c]
                            bestr, bestc = r, c
                    hypFlag[bestr][bestc] = True
                    maxAppleTrees[index] += 1
                    n -= 1

                for r, c in group:
                    if not hypFlag[r][c] and not hypClear[r][c]:
                        hypClear[r][c] = True

        totalMax += maxAppleTrees[index]
        index += 1

    # Compare
    others = []
    for r in range(height):
        for c in range(width):
            cell = (r, c)
            if not clear(cell) and not flag(cell) and not inDragon[r][c]:
                others.append(cell)

    if trees - flags - totalMax == len(others):
        # Flag all cells not in a dragon
        if len(others) > 0:
            if verbose:
                print()
                printGroup([c for dragon in dragons for group in dragon for c in group])
                print(f"FORRESTER DRAGONS")
                print(
                    f"  {trees - flags} apple trees remaining in the orchard, and maximum {totalMax} in the following groups :"
                )
                index = 0
                for dragon in dragons:
                    cells = sorted(set([cell for group in dragon for cell in group]))
                    print(
                        f"   - maximum {maxAppleTrees[index]} in group {positions(cells)}"
                    )
                    index += 1
                if len(others) == 1:
                    print(f"> Marking the other remaining tree : {positions(others)}")
                else:
                    print(
                        f"> Marking the {len(others)} other remaining trees : {positions(others)}"
                    )
                print()

            for cell in others:
                markTree(cell)
            DragonsTechnique += 1
            return


def BruteDragons():
    # Brute Force can give 4 types of answers :
    # - if a cell is the same throughout all the combinations
    # - if only one dragon has a variable number of possible apple and there are no other trees
    # - the now classic forrester and lumberkack techniques with the min and max values

    global StaticTreesTechnique
    global AllAccountedForTechnique
    global BruteDragonsTechnique
    global GettingTrickyTechnique

    dragons, groups, applesInGroup, nGroups, inDragon = getDragons()

    if dragons == []:
        return

    minApples = 0
    maxApples = 0
    minCells = []
    maxCells = []
    dragonMinApples = [0 for _ in range(len(dragons))]
    dragonMaxApples = [0 for _ in range(len(dragons))]
    dragonMinCells = [[] for _ in range(len(dragons))]
    dragonMaxCells = [[] for _ in range(len(dragons))]

    nCombinations = [0 for _ in range(len(dragons))]
    nVariable = 0
    iVariable = -1
    combVariable = []

    for index, dragon in enumerate(dragons):
        combinations = []
        if len(dragon) == 1:
            # no unique solution, but unique number of apple trees
            a = applesInGroup[groups.index(dragon[0])]
            n = len(dragon[0])
            dragonMaxApples[index] = a
            dragonMinApples[index] = a
            dragonMaxCells[index] = []
            dragonMinCells[index] = []
            nCombinations[index] = len(list(itertools.combinations(range(n), a)))
            # i know it is n! / (a! * (n-a)!)
        else:
            # here comes the brute force

            cells = sorted(set([cell for group in dragon for cell in group]))

            combinations.append([0 for _ in range(len(cells))])
            #  0 = unused
            #  1 = marked
            # -1 = max for the group reached

            for group in dragon:
                newCombinations = []
                for combination in combinations:
                    # counting remaining apples for this group in this combination
                    a = applesInGroup[groups.index(group)]
                    for cell in group:
                        if combination[cells.index(cell)] == 1:
                            a -= 1

                    # looking at all the theoretical combination
                    for iter in [
                        p
                        for p in itertools.product((True, False), repeat=len(group))
                        if sum(p) == a
                    ]:
                        newCombination = combination[:]  # shallow copy
                        count = 0
                        # Apply the combination, if it fits
                        for cell, bool in zip(group, iter):
                            if newCombination[cells.index(cell)] == 0:
                                if bool:
                                    newCombination[cells.index(cell)] = 1
                                    count += 1
                                else:
                                    newCombination[cells.index(cell)] = -1

                        # If it fits, append the existing combination
                        if count == a:
                            newCombinations.append(newCombination)

                # once all groups have been tested, the combination is complete
                combinations = newCombinations

            nCombinations[index] = len(combinations)

            # Computing global stats
            dragonMinApples[index] = len(cells)
            dragonMaxApples[index] = 0
            xor = [0 for _ in range(len(cells))]
            for combination in combinations:
                n = 0

                for i, cell in enumerate(combination):
                    if cell == 1:
                        n += 1
                        xor[i] += 1

                if n > dragonMaxApples[index]:
                    dragonMaxApples[index] = n
                    dragonMaxCells[index] = [
                        c
                        for group in dragon
                        for c in group
                        if combination[cells.index(c)] == 1
                    ]
                elif n == 0:
                    dragonMaxCells[index] = []
                    # There is no unique solution

                if n < dragonMinApples[index]:
                    dragonMinApples[index] = n
                    dragonMinCells[index] = [
                        c
                        for group in dragon
                        for c in group
                        if combination[cells.index(c)] == 1
                    ]
                elif n == 0:
                    dragonMaxCells[index] = []
                    # There is no unique solution

            if dragonMinApples[index] != dragonMaxApples[index]:
                nVariable += 1
                iVariable = index
                combVariable = combinations

            # Dragon method :
            toMark = []
            toCut = []
            for i in range(len(cells)):
                if xor[i] == len(combinations):
                    toMark.append(cells[i])
                elif xor[i] == 0:
                    toCut.append(cells[i])

            if toCut != [] or toMark != []:
                if verbose:

                    dragonCells = sorted(
                        set([cell for group in dragon for cell in group])
                    )
                    printGroup(dragonCells)
                    print(f"STATIC TREES")
                    print(
                        f"  Every solution has been tested for the group {positions(dragonCells)}"
                    )
                    print(f"  In each of the {len(combinations)} solutions", end="")
                    if toMark != []:
                        print(f", {positions(toMark)} is an apple tree", end="")
                    if toCut != []:
                        print(f", {positions(toCut)} is empty", end="")
                    print()
                    if toMark != []:
                        print(f"> Marking {positions(toMark)}")
                    if toCut != []:
                        print(f"> Cutting off {positions(toCut)}")
                    print()
                for c in toCut:
                    cutTree(c)
                for c in toMark:
                    markTree(c)
                StaticTreesTechnique += 1
                return

        minApples += dragonMinApples[index]
        maxApples += dragonMaxApples[index]
        minCells += dragonMinCells[index]
        maxCells += dragonMaxCells[index]

    # Global methods
    global trees
    global flags
    otherCells = []
    for r in range(height):
        for c in range(width):
            cell = (r, c)
            if not clear(cell) and not flag(cell) and not inDragon[r][c]:
                otherCells.append(cell)
    others = len(otherCells)

    if others == 0:
        if nVariable == 1:
            if maxApples >= trees - flags >= minApples:
                dragon = dragons[iVariable]
                cells = sorted(set([cell for group in dragon for cell in group]))
                goal = trees - flags - minApples + dragonMinApples[iVariable]
                combinations = []
                for combination in combVariable:
                    n = 0
                    for b in combination:
                        if b == 1:
                            n += 1
                    if n == goal:
                        combinations.append(combination)

                if len(combinations) == 1:
                    toMark = [cell for cell, b in zip(cells, combinations[0]) if b == 1]
                    toCut = [cell for cell, b in zip(cells, combinations[0]) if b != 1]
                    if verbose:
                        print()
                        printGroup(
                            [c for dragon in dragons for group in dragon for c in group]
                        )
                        dragonCells = sorted(
                            set([cell for group in dragon for cell in group])
                        )
                        print(f"ALL ACOUNTED FOR")
                        print(f"  {trees - flags} apple trees remaining in the orchard")
                        print(
                            f"  Every solution has been tested, they contain between {minApples} and {maxApples} apple trees."
                        )
                        if len(dragons) > 1:
                            print(
                                f"  All groups but one have a constant count, that add up to {trees - flags - goal}"
                            )
                            print(
                                f"  Group {positions(dragonCells)} has only one solution for {goal} apple trees : {positions(toMark)}"
                            )
                        else:
                            print(
                                f"  There is only one solution for {goal} apple trees : {positions(toMark)}"
                            )
                        if toMark != []:
                            print(f"> Marking {positions(toMark)}")
                        if toCut != []:
                            print(f"> Cutting off {positions(toCut)}")
                        print()

                    for c in toCut:
                        cutTree(c)
                    for c in toMark:
                        markTree(c)
                    AllAccountedForTechnique += 1
                    return
                else:
                    xor = [0 for _ in range(len(cells))]
                    for combination in combinations:
                        for i, cell in enumerate(combination):
                            if cell == 1:
                                xor[i] += 1
                    toMark = []
                    toCut = []
                    for i in range(len(cells)):
                        if xor[i] == len(combinations):
                            toMark.append(cells[i])
                        elif xor[i] == 0:
                            toCut.append(cells[i])

                    if toCut != [] or toMark != []:
                        if verbose:

                            dragonCells = sorted(
                                set([cell for group in dragon for cell in group])
                            )
                            printGroup(dragonCells)
                            print(f"IT'S GETTING TRICKY")
                            print(
                                f"  {trees - flags} apple trees remaining in the orchard"
                            )
                            print(
                                f"  Every solution has been tested, they contain between {minApples} and {maxApples} apple trees."
                            )
                            if len(dragons) > 1:
                                print(
                                    f"  All groups but one have a constant count, that add up to {trees - flags - goal}"
                                )
                            print(
                                f"  Group {positions(dragonCells)} has {len(combinations)} solution for the remaining {goal} apple trees."
                            )
                            print(
                                f"  In each of the {len(combinations)} solutions",
                                end="",
                            )
                            if toMark != []:
                                print(f", {positions(toMark)} is an apple tree", end="")
                            if toCut != []:
                                print(f", {positions(toCut)} is empty", end="")
                            print()
                            if toMark != []:
                                print(f"> Marking {positions(toMark)}")
                            if toCut != []:
                                print(f"> Cutting off {positions(toCut)}")
                            print()
                        for c in toCut:
                            cutTree(c)
                        for c in toMark:
                            markTree(c)
                        GettingTrickyTechnique += 1
                        return

    else:
        if trees - flags - minApples == 0:
            toMark = []
            toCut = []
            for cell in cells:
                if cell in minCells:
                    toMark.append(cell)
                else:
                    toCut.append(cell)

            if verbose:
                print()
                printGroup([c for dragon in dragons for group in dragon for c in group])
                print(f"BRUTE LUMBERJACK DRAGONS")
                print(f"  {trees - flags} apple trees remaining in the orchard")
                print(
                    f"  Every solution has been tested, they contain minimum total of {minApples} apple trees :"
                )
                for index, dragon in enumerate(dragons):
                    dragonCells = sorted(
                        set([cell for group in dragon for cell in group])
                    )
                    m = dragonMinApples[index]
                    M = dragonMaxApples[index]
                    n = nCombinations[index]
                    if m == M:
                        print(
                            f"  - Exactly {M} in the {n} solutions for {positions(dragonCells)}"
                        )
                    else:
                        print(
                            f"  - {m} to {M} in the {n} solutions for {positions(dragonCells)}"
                        )
                print(
                    f"> Cuting off all other remaining trees : {positions(otherCells)}"
                )
                print(f"  This minimum is obtained with a unique solution :")
                if toMark != []:
                    print(f"> Marking {positions(toMark)}")
                if toCut != []:
                    print(f"> Cutting off {positions(toCut)}")
                print()

            for c in toCut:
                cutTree(c)
            for c in toMark:
                markTree(c)
            for cell in otherCells:
                cutTree(cell)
            BruteDragonsTechnique += 1
            return

        if trees - flags - maxApples == others:
            toMark = []
            toCut = []
            for cell in cells:
                if cell in maxCells:
                    toMark.append(cell)
                else:
                    toCut.append(cell)

            if verbose:
                print()
                printGroup([c for dragon in dragons for group in dragon for c in group])
                print(f"BRUTE FORRESTER DRAGONS")
                print(f"  {trees - flags} apple trees remaining in the orchard")
                print(
                    f"  Every solution has been tested, they contain a maximum of {maxApples} apple trees :"
                )
                for index, dragon in enumerate(dragons):
                    dragonCells = sorted(
                        set([cell for group in dragon for cell in group])
                    )
                    m = dragonMinApples[index]
                    M = dragonMaxApples[index]
                    n = nCombinations[index]
                    if m == M:
                        print(
                            f"  - Exactly {M} in the {n} solutions for {positions(dragonCells)}"
                        )
                    else:
                        print(
                            f"  - {m} to {M} in the {n} solutions for {positions(dragonCells)}"
                        )
                print(f"  There are {others} other trees out of these groups")
                print(f"> Marking all other remaining trees {positions(otherCells)}")

                print(f"  This maximum is obtained with a unique solution :")
                if toMark != []:
                    print(f"> Marking {positions(toMark)}")
                if toCut != []:
                    print(f"> Cutting off {positions(toCut)}")
                print()

            for c in toCut:
                cutTree(c)
            for c in toMark:
                markTree(c)
            for cell in otherCells:
                markTree(cell)
            BruteDragonsTechnique += 1
            return

    # No result on the last method, display gathered info for the human,
    # maybe he wants to check my work ah ah ah ah !
    if verbose:
        print()
        print(f"NO RESULT")
        print(f"  {trees - flags} apple trees remaining in the orchard")
        if minApples < maxApples:
            print(
                f"  Every solution has been tested in the following groups, they contain between {minApples} and {maxApples} apple trees :"
            )
        else:
            print(
                f"  Every solution has been tested, they contain {minApples} apple trees :"
            )
        for index, dragon in enumerate(dragons):
            dragonCells = sorted(set([cell for group in dragon for cell in group]))
            m = dragonMinApples[index]
            M = dragonMaxApples[index]
            n = nCombinations[index]
            if m == M:
                print(
                    f"  - Exactly {M} in the {n} solutions for {positions(dragonCells)}"
                )
            else:
                print(
                    f"  - {m} to {M} in the {n} solutions for {positions(dragonCells)}"
                )
        if others > 0:
            if minApples < maxApples:
                print(
                    f"  And {max(0,trees - flags - maxApples)} to {min(others,trees - flags - minApples)} in the {others} remaining trees",
                    end="",
                )
            else:
                print(
                    f"  And {max(0,trees - flags - maxApples)} in the {others} remaining trees",
                    end="",
                )
            if others <= 10:
                print(f" : {positions(otherCells)}")
        print()


def collectApples(s=0):
    # Beginnner 8 * 8 * 10
    # Intermediate 16 * 16 * 40
    # Advanced 16 * 31 * 99
    height = 16
    width = 31
    trees = 99

    global seed
    seed = s
    if seed == 0:
        seed = random.randrange(10000)
    print(f"Seed = {seed}")
    random.seed(seed)

    r = random.randrange(height)
    c = random.randrange(width)
    createOrchard(height, width, trees, r, c)

    if verbose:
        print()
        print(
            f"The forrester has planted {trees} apple trees in the forrest, but he can't remember where."
        )
        print(
            f"He needs to make space for apple trees to grow, by cutting off the other trees."
        )
        print(
            f"Every apple tree drops an apple on each of the eight surrounding cells."
        )
        print()
        print(
            f"The first tested cell ({position((r,c))}) is guaranteed to be a clearing."
        )
        print()
    cutTree((r, c))
    stack.append((r, c))

    while len(stack) > 0:
        cell = stack.pop(0)
        Beginner(cell)
        if len(stack) > 0 or trees == flags:
            continue
        Twins(cell)
        if len(stack) > 0 or trees == flags:
            continue
        Triplets(cell)
        if len(stack) > 0 or trees == flags:
            continue
        Dragons()
        if len(stack) > 0 or trees == flags:
            continue
        BruteDragons()

        # i discarded the return True -> continue syntax used at first because it doesn't work with the dragons techniques that can change the board without changing the stack

    if trees > flags and cleared == width * height - trees:
        toMark = []
        for c in range(width):
            for r in range(height):
                cell = (r, c)
                if not clear(cell) and not flag(cell):
                    markTree(cell)
                    toMark.append(cell)
        if verbose:
            print(f"\tMarking of remaining trees : {positions(toMark)}")

    if trees == flags and cleared < width * height - trees:
        toCut = []
        for c in range(width):
            for r in range(height):
                cell = (r, c)
                if not clear(cell) and not flag(cell):
                    cutTree(cell)
                    toCut.append(cell)
        if verbose:
            print(f"\tCutting of remaining trees : {positions(toCut)}")

    printOrchard()


verbose = True
emoji = True
collectApples()
