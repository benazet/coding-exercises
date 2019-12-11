# bad
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    print (i**2)

# good 
for i in range(10):
    print (i**2)

colors = ['red', 'green', 'blue', 'yellow']

for color in colors:
    print (color)

for color in reversed(colors):
    print (color)

for i, color in enumerate(colors):
    print (i, '-->', colors[i])

names = ['jeanne', 'maximilien', 'roxane', 'joseph']
colors = ['red', 'green', 'blue','yellow']

for name, color in zip(names, colors):
    print(name, '-->', color)

for color in sorted(colors):
    print(color)