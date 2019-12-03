#https://www.dailycodingproblem.com


#first try, doesn't count the paths but just the sum of each steps
# i.e. [1,2,1] [2,1,1] and [1,1,2] are just counted once
steps = [(1,0),(3,0),(5,0)]
goal = 10
count = 0

def num_ways(steps,goal):
    global count
    if len(steps) == 1 :
        return goal % steps[0][0]
    else:
        while steps[0][0] * steps[0][1] <= goal :
            result = num_ways(steps[1:len(steps)],goal - steps[0][0] * steps[0][1])
            if result == 0:
                count +=1
            steps[0] = list(steps[0])
            steps[0][1] += 1

        

num_ways(steps,goal)

# Solution form website
def staircase(n, X):
    if n < 0:
        return 0
    elif n == 0:
        return 1
    else:
        return sum(staircase(n-x, X) for x in X)

print(staircase(4, {1, 2}))

def DPstaircase(n,X):
    cache = [0 for _ in range(n+1)]
    cache[0] = 1
    for i in range(1,n+1):
        cache[i] += sum(cache[i-x] for x in X if i-x >=0)
    return cache[n]

goal = 6
steps = {1, 3,5}
result = DPstaircase(goal, steps)
print("There are %d ways to climb a stairs of %d steps with the intervals : %s" %(result,goal,steps))
