#Homework 9
#In functional programming find the largest reversi number that is a product of two 3-digit numbers.

def reversi():

    list_nums = list(range(1, 1000))
    tracker = [[str(x*y), str(x), str(y)] for x in list_nums for y in list_nums]
    new_nums = [str(x*y) for x in list_nums for y in list_nums]
    only_rev = list(filter(lambda x: x[0] == x[0][::-1], tracker))
    integers = [[int(x[i]) for i in range(3)] for x in only_rev]
    maximum = max(integers)
    print("{} x {} = {}".format(maximum[2], maximum[1], maximum[0]))

reversi()