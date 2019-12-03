from functools import reduce

# Crossed wires


'''
program   -> wire '\n' wire
wire      -> move [, move]
                  position := { 'x'=0, 'y'=0 };
                  position = move(position)
                  moves.append(position)
move      -> direction digits
direction -> 'R' | 'L' | 'U' | 'D'
digits    -> digit [digit]
digit     -> '0' | '1' | ... | '9'
'''
symbols = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
file_position = 0
steps_taken = dict()
intersections = []
queue = []


def getChar():
    global file_position, file
    char = file.read(1)
    file_position += 1
    return char

def peekChar():
    file_position, file
    char = file.read(1)
    file.seek(file_position)
    return char


def program():
    global intersections, queue, file_position
    file_position = 0

    lines1 = wire()
    if (ord(peekChar()) != 10):
        print(peekChar())
        raise ValueError("Expected newline separating wires")
    else:
        getChar()

    # insert intersections back into queue
    intersections = queue.copy()
    queue.clear()

    lines2 = wire()

    return (lines1, lines2)

def wire():
    steps = 0
    moves = set()
    position = (0, 0)

    position, points, steps = move(position, steps)
    moves.update(points)

    while (peekChar() == ','):
        getChar()
        position, points, steps = move(position, steps)
        moves.update(points)

    return moves

def move(pos, steps): # (x, y), steps -> new (x, y), [(x,y), ...], steps
    global queue
    direct = direction()
    magnitude = digits()
    point = (0,0)
    points, x, y = set(), 0, 0

    if (direct == 'R'):
        x = 1
    elif (direct == 'L'):
        x = -1
    elif (direct == 'U'):
        y = 1
    elif (direct == 'D'):
        y = - 1
    else:
        raise ValueError("Direction error! got {0} expecting R, L, U, D".format(direct))

    for increment in range(1, magnitude+1):
        point = pos[0] + x * (increment), pos[1] + y * (increment)
        points.add(point)
        # check if visited already, otherwise add magnitude to steps to intersection
        # use queue, once visited pop from queue
        if point in intersections:
            intersections.remove(point)
            steps_taken[point] += steps + increment
            queue.append(point)

    return point, points, steps + magnitude

def direction():
    return getChar()

def digits():
    digit = ''
    while (peekChar() in symbols):
        digit += getChar()

    return int(digit)



with open("day3.txt") as file:
    lines = program()
    intersections = list(lines[0].intersection(lines[1]))
    shortest_intersection = reduce(min, map(lambda x : abs(x[0]) + abs(x[1]), intersections))
    print("Day 3 Part 1: {0}".format(shortest_intersection))

with open("day3.txt") as file:
    for intersect in intersections:
        steps_taken[intersect] = 0
    lines = program()
    smallest_steps_taken = reduce(min, steps_taken.values())
    print("Day 3 Part 2: {0}".format(smallest_steps_taken))


