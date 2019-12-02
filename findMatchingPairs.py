#https://www.youtube.com/watch?v=XKu_SEDAykw
# OK in this one i didn't pause soon enough, i got the idea from the video


def HasPair(list,goal):
    a = 0
    b = len(list)-1
    while a<b:
        sum = list[a] + list[b]
        if sum == goal:
            # print("Success : %d + %d = %d" % (list[a], list[b], goal))
            return True
        else:
            if sum > goal:
                b -= 1
            else:
                a += 1
    return False


print(HasPair([1, 2, 3, 9],8))
print(HasPair([1, 2, 4, 4],8))
print(HasPair([1, 2, 4, 4,6,9,13,16,17,21,27],35))