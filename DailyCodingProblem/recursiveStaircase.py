
steps = [(1,0),(2,0)]
goal = 4


def num_ways(steps,goal):
    step = 
    if len(steps) == 1 :
        return goal %% steps[0][0]
    else:
        while steps[0][0] * steps[0][1] < goal :
            result = num_ways(steps[1:len(steps)],goal)
            if result = 0:
                
            steps[0][1] += 1

        

print(num_ways(steps,goal))