# https://www.youtube.com/watch?v=EuPSibuIKIg
# Google Coding Interview With A Competitive Programmer

import time

points = [
    (0, 0), (0, 1),
    (1, 0), (1, 1),
    (2, 0), (2, 1), (2, 2),
    (0, 2),
    (3, 1), (3, 3), (1, 3)
]

# Display grid
print ('Count the rectangles defined by these points')
for y in sorted(set([y for x, y in points]), reverse=True):
    line = '{:>2} '.format(y)
    for x in sorted(set([x for x, y in points])):
        if (x, y) in points:
            line += ". "
        else:
            line += "  "
    print(line)
line = '   '
for x in sorted(set([x for x, y in points])):
    line += '{:<2}'.format(x)
print(line)


# Errichto's solution
t = time.time() * 10e6
count = {}  # Dictionary
answer = 0
for p in points:
    for above in points:
        if p[0] == above[0] and p[1] < above[1]:
            line = (p[1], above[1])
            if line in count.keys():
                answer += count[line]
            else:
                count[line] = 0
            count[line] += 1

print("\nErricho's algorithm finds %d rectangles in %d μs" % (answer, time.time()*10e6-t))


# My solution
t = time.time() * 10e6
rects = []
for p in points:
    for above in points:
        if p[0] == above[0] and p[1] < above[1]:
            for right in points:
                if p[0] < right[0] and p[1] == right[1]:
                    for diag in points:
                        if diag[0] == right[0] and diag[1] == above[1]:
                            rects.append((p, above, right, diag))


# Display results
print("\nGéraud finds these %d rectangles in %d μs :" % (len(rects), time.time()*10e6-t))
for y in sorted(set([y for x, y in points]), reverse=True):
    line = ''
    for rect in rects:
        for x in sorted(set([x for x, y in points])):
            if (x, y) in rect:
                line += "o "
            else:
                if (x, y) in points:
                    line += ". "
                else:
                    line += "  "
        line += '   '
    print(line)
