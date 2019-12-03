# https://www.youtube.com/watch?v=EuPSibuIKIg
# Google Coding Interview With A Competitive Programmer

import time

points = [
    (0, 0), (0, 1),
    (1, 0), 
    (2, 0), (2, 1), (2, 2),
    (3, 1), (3, 3), (1, 3),
    (4,2), (2,4),
    (4,0),(0,3),(3,7),(7,4),(7,0),
    (6,6)
]

# Display grid
print('Count the rectangles defined by these points :')
xmin = min(points)[0]
xmax = max(points)[0]+1
ymin = min(points,key= lambda t: t[1])[1]-1
ymax = max(points,key= lambda t: t[1])[1]
for y in range(ymax,ymin,-1):
    line = '{:>2} '.format(y)
    for x in range(xmin,xmax):
        if (x, y) in points:
            line += ". "
        else:
            line += "  "
    print(line)
line = '   '
for x in range(xmin,xmax):
    line += '{:<2}'.format(x)
print(line)


# My solution
def orth(O, A, B):
    # Dot Product = 0
    return (A[0]-O[0])*(B[0]-O[0]) + (A[1]-O[1])*(B[1]-O[1]) == 0

def CW(O,A,B):
    # Cross product > 0
    return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0]) > 0

t = time.time() * 1e6
rects = []
for p1 in points:
    for p2 in points:
        if p2[0] > p1[0] and p2[1] <= p1[1]:
            for p4 in points:
                if p4 != p1 and p4 != p2 and orth(p1, p2, p4) and CW(p1,p2,p4):
                    p3 = (p4[0] - p1[0] + p2[0], p4[1] - p1[1] + p2[1])
                    if p3 in points:
                        rects.append((p1, p2, p3, p4))

t = time.time()*1e6-t

# Display results

for rect in rects:
    print()
    for y in range(ymax,ymin,-1):
        line = ''
        for x in range(xmin,xmax):
            if (x, y) in rect:
                line += repr(rect.index((x,y))+1) + " "
            else:
                if (x, y) in points:
                    line += ". "
                else:
                    line += "  "
        print(line)

print("\n%d rectangles found in %d µs" % (len(rects), t))
