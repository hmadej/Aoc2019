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


def get_char():
    global file_position, file
    char = file.read(1)
    file_position += 1
    return char


def peek_char():
    file_position, file
    char = file.read(1)
    file.seek(file_position)
    return char


def program():
    points1 = wire()
    if ord(peek_char()) != 10:
        print(peek_char())
        raise ValueError("Expected newline separating wires")
    else:
        get_char()

    points2 = wire()

    return (points1, points2)


def wire():
    steps = 0
    steps_taken = dict()
    position = (0, 0)

    position, steps_taken, steps = move(position, steps_taken, steps)

    while peek_char() == ',':
        get_char()
        position, steps_taken, steps = move(position, steps_taken, steps)

    return steps_taken


def move(pos, steps_taken, steps):
    direct = direction()
    magnitude = digits()
    point = (0, 0)
    points, x, y = set(), 0, 0

    if direct == 'R':
        x = 1
    elif direct == 'L':
        x = -1
    elif direct == 'U':
        y = 1
    elif direct == 'D':
        y = - 1
    else:
        raise ValueError("Direction error! got {0} expecting R, L, U, D".format(direct))

    for increment in range(1, magnitude + 1):
        point = pos[0] + x * increment, pos[1] + y * increment
        if point not in steps_taken.keys():
            steps_taken[point] = steps + increment

    return point, steps_taken, (steps + magnitude)


def direction():
    return get_char()


def digits():
    digit = ''
    while peek_char() in symbols:
        digit += get_char()

    return int(digit)


with open("day3.txt") as file:
    wire1, wire2 = program()
    points1, points2 = set(wire1.keys()), set(wire2.keys())
    intersections = list(points1.intersection(points2))
    shortest_intersection = reduce(min, map(lambda x: abs(x[0]) + abs(x[1]), intersections))
    print("Day 3 Part 1: {0}".format(shortest_intersection))

    steps = []
    for point in intersections:
        steps.append(wire1[point] + wire2[point])

    smallest_steps_taken = reduce(min, steps)
    print("Day 3 Part 2: {0}".format(smallest_steps_taken))
