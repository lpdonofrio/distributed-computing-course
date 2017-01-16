# Homework 9
# Prompt: Consider a triangle of numbers. By starting at the top of the triangle
# and moving to adjacent numbers below, we want to find the maximum total from top to bottom.


import copy


def read_file(filename):
    with open(filename, 'r') as document:
        docs = document.read().splitlines()
    lines = []
    for doc in docs:
        nums_int = []
        line = doc.split()
        for num in line:
            num = int(num)
            nums_int.append(num)
        lines.append(nums_int)
    return lines


def next_line(n, maximum):
    index = []
    for item in (n, n + 1):
        if item < maximum:
            index.append(item)
    return index


def find_path(lines):
    '''create deep copy of triangle, zip current line and following line,
    find highest sum between each neighbor and the current number'''
    route = copy.deepcopy(lines)
    for (current_line, following) in zip(route[-2::-1], route[::-1]):
        for index, element in enumerate(current_line):
            sums_neighbors = [element + following[n] for n in next_line(index, len(following))]
            current_line[index] = max(sums_neighbors)
    '''starting from the top, pick the neighbor whose value equals the sum of the whole path minus the current item,
    use the index of that value to find the number in the original triangle and append it to the main path'''
    path = []
    for (current_line, following, all_lines) in zip(route, route[1:], lines): #current_line is now all sums
        path.append(all_lines[index])
        index = [x for x in next_line(index, len(following)) if following[x] == current_line[index] - all_lines[index]][0]
    path.append(lines[-1][index]) #add last row
    return route[0], path


def main():

    print("Enter the file name to read:")
    filename = input('> ')
    try:
        lines = read_file(filename)
    except IOError:
        print("Unable to find the file {}".format(filename))
    except:
        print("Sorry, there was an error")
    else:
        total, path = find_path(lines)
        path_new = path[0:-1]
        last = path[-1]
        for item in path_new:
            print('{} + '.format(item), end='')
        print('{} = '.format(last), end='')
        for item in total:
            print(item)

if __name__ == "__main__":
    main()
