import random

# global variables
tree = []
number = 0
flag = []
flags = 0
apples = []
clear = []
width = 0
height = 0
cleared = 0
stack = []
neighbour = []
linked = []
verbose = False


def createOrchard(h, w, n=-1, r=-1, c=-1):
    global width
    global height
    global number
    global tree
    global flag
    global apples
    global clear
    global neighbour
    global linked

    width = w
    height = h
    if n == -1:
        n = width * height / 3
    number = n
    tree = [[False for _ in range(width)] for _ in range(height)]
    flag = [[False for _ in range(width)] for _ in range(height)]
    clear = [[False for _ in range(width)] for _ in range(height)]
    apples = [[-1 for _ in range(width)] for _ in range(height)]
    neighbour = [[[] for _ in range(width)] for _ in range(height)]
    linked = [[[] for _ in range(width)] for _ in range(height)]

    number = min(number, width*height-1)
    while number > 0:
        x = random.randrange(width)
        y = random.randrange(height)
        if not tree[y][x]:
            # if r == -1 or c == -1 or y != r or x != c:
            if r == -1 or c == -1 or abs(y-r) > 1 or abs(x-c) > 1:
                tree[y][x] = True
                number -= 1


def printOrchard(cheat=False):

    symbol = " 12345678▉"
    val = [[""] + [symbol[a] for a in row] for row in apples]
    for r in range(height):
        for c in range(width):
            if cheat:
                if tree[r][c]:
                    val[r][c+1] = ""
            if flag[r][c]:
                if tree[r][c] or not cheat:
                    val[r][c+1] = "⚑"
                else:
                    val[r][c+1] = "⚐"

    for r in range(height):
        print("".join(c for c in val[r]))


def fancyOrchard(cheat=False):
    def expandLine(line):
        return line[0] + "".join(line[1:5] for _ in range(width-1)) + line[5:9]
    line0 = expandLine("┌───┬───┐")
    line1 = expandLine("│ . │ . │")
    line2 = expandLine("├───┼───┤")
    line3 = expandLine("└───┴───┘")

    symbol = " 12345678▉"
    val = [[""] + [symbol[a] for a in row] for row in apples]
    for r in range(height):
        for c in range(width):
            if cheat:
                if tree[r][c]:
                    val[r][c+1] = ""
            if flag[r][c]:
                if tree[r][c] or not cheat:
                    val[r][c+1] = "⚑"
                else:
                    val[r][c+1] = "⚐"

    print("    " + " ".join(f"{c+1:^3}" for c in range(width)))
    print("   " + line0)
    for r in range(height):
        print(f"{letter(r):^3}", end='')
        print("".join(a+b for a, b in zip(val[r], line1.split("."))), end='')
        print(f"{letter(r):^3}")
        print("   " + [line2, line3][r == height-1])
    print("    " + " ".join(f"{c+1:^3}" for c in range(width)))


def position(cell):
    r, c = cell
    return f"{letter(r)}{c+1}"


def letter(r):
    if height <= 26:
        result = chr(r+65)
    else:
        result = chr(r//26+65) + chr(r % 26+65)
    return result


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


def neighbourApples(cell):
    count = 0
    for r, c in neighbourCells(cell):
        if tree[r][c]:
            count += 1
    return count


def countUnclear(cells):
    count = 0
    for r, c in cells:
        if not clear[r][c]:
            count += 1
    return count


def countFlag(cells):
    count = 0
    for r, c in cells:
        if flag[r][c]:
            count += 1
    return count


def checkNeighbours(cell):
    for neighbour in neighbourCells(cell):
        checkCell(neighbour)


def checkCell(cell):
    r, c = cell
    if not cell in stack and clear[r][c]:
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
    if not flag[r][c] and not clear[r][c]:
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
            clear[r][c] = True
            apples[r][c] = neighbourApples(cell)
            checkNeighbours(cell)
            checkCell(cell)
            return True


def mark(cell):
    global flags
    r, c = cell
    flag[r][c] = True
    flags += 1
    checkNeighbours((r, c))
    if not tree[r][c]:
        print(f"{position(cell)}\tThat tree is not an apple tree !")
        fancyOrchard(True)


def test(cell):
    r, c = cell

    n = neighbourCells(cell)
    u = countUnclear(n)
    f = countFlag(n)
    a = apples[r][c]

    if a == 0:
        result = cutNeighbours(cell)
        if result != []:
            if verbose:
                print(f"{position(cell)}\tNo apple, cutting off " +
                      ", ".join(position(cell) for cell in result))
            return True

    if a - f == 0:
        result = cutNeighbours(cell)
        if result != []:
            if verbose:
                print(f"{position(cell)}\tAll apple trees marked, cutting off " +
                      ", ".join(position(cell) for cell in result))
            return True

    if a == u > 0:
        for r, c in n:
            if not clear[r][c] and not flag[r][c]:
                if verbose:
                    print(
                        f"{position(cell)}\tAs many apples as trees, marking {position((r,c))} ")
                mark((r, c))

    # collect all linked cells (ie cells that share a neighbour)
    l = []
    # if any of this cell is not updated, pass to the next test and come back later
    for i, j in linkedCells(cell):
        if apples[i][j] > 0 and not (i, j) in stack:
            l.append((i, j))

    for linkedCell in l:
        # printOrchard()
        # print(position(cell), position(linkedCell))
        u = countUnclear(n)
        f = countFlag(n)

        n2 = neighbourCells(linkedCell)
        a2 = neighbourApples(linkedCell)
        u2 = countUnclear(n2)
        f2 = countFlag(n2)

        inter = [cell for cell in n if cell in n2]
        uI = countUnclear(inter)
        fI = countFlag(inter)

        flaggedCells = []
        clearedCells = []
        if (a - f) - (a2 - f2) == u - uI:
            for i, j in n:
                if not (i, j) in inter and clear[i][j] == False and flag[i][j] == False:
                    flaggedCells.append((i, j))
                    mark((i, j))

            for i, j in n2:
                if not (i, j) in inter and clear[i][j] == False and flag[i][j] == False:
                    clearedCells.append((i, j))
                    cutTree((i, j))

        if (a2 - f2) - (a - f) == (u2 - f2) - (uI - fI):
            for i, j in n2:
                if not (i, j) in inter and clear[i][j] == False and flag[i][j] == False:
                    flaggedCells.append((i, j))
                    mark((i, j))

            for i, j in n:
                if not (i, j) in inter and clear[i][j] == False and flag[i][j] == False:
                    clearedCells.append((i, j))
                    cutTree((i, j))
        if verbose:
            if len(flaggedCells) > 0 or len(clearedCells) > 0:
                print(f"{position(cell)}-{position(linkedCell)}\t", end='')
            if len(flaggedCells) > 0:
                print(f"marking " + ", ".join(position(cell)
                                              for cell in flaggedCells) + " ", end='')
            if len(flaggedCells) > 0 and len(clearedCells) > 0:
                print(", ", end='')
            if len(clearedCells) > 0:
                print(f"cutting off " + ", ".join(position(cell)
                                                  for cell in clearedCells), end='')
            if len(flaggedCells) > 0 or len(clearedCells) > 0:
                print()

    return True


def collectApples():
    # Beginnner 8 * 8 * 10
    # Intermediate 16 * 16 * 40
    # Advanced 16 * 31 * 99
    height = 16
    width = 31
    number = 99

    r = random.randrange(height)
    c = random.randrange(width)
    createOrchard(height, width, number, r, c)
    print("We need to make space for apple trees, by cutting other trees.")
    print("Every apple tree drops an apple on each of the eight surrounding cells.")
    print("Mark the apple trees")
    cutTree((r, c))
    stack.append((r, c))

    while len(stack) > 0:
        cell = stack.pop(0)
        test(cell)

    fancyOrchard(True)

    if number == flags:
        if cleared < width * height - number:
            for c in range(width):
                for r in range(height):
                    if not clear[r][c] and not flag[r][c]:
                        test((r, c))

        print("Orchard cleared of unwanted trees !")
    else:
        print(
            f"{number - flags} apple trees remaining amongst {width * height - cleared - flags} trees")

    print()


collectApples()
