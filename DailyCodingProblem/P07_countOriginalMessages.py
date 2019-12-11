# Good morning! Here's your coding interview problem for today.
# This problem was asked by Facebook.
# Given the mapping a = 1, b = 2, ... z = 26, and an encoded message, count the number of ways it can be decoded.
# For example, the message '111' would give 3, since it could be decoded as 'aaa', 'ka', and 'ak'.
# You can assume that the messages are decodable. For example, '001' is not allowed.

# Brute force

def countWays(message):
    if len(message) <= 1 :
        return 1
    else :
        if int(message[0:1]) <= 26 :
            return countWays(message[2:]) + countWays(message[1:])
        else:
            return countWays(message[1:])



print (countWays('1110'))
 