from enum import Enum
from functools import reduce
from math import gcd

'''
parse       -> position ['\n' position]
position   -> '<' args '>'
args       -> arg comma arg comma arg
arg        -> identifier num
identifier -> letter '='
comma      -> ', '
num        -> [-] digit+
digit      -> '0' | '1' | ... | '9'
'''
pos = 0


def get_char():
    global pos, file
    char = file.read(1)
    pos += 1

    return char


def peek_char():
    global pos, file
    char = file.read(1)
    file.seek(pos)

    return char


def parse():
    global pos
    pos = 0
    positions = [position()]
    get_char()
    while peek_char() != '':
        positions.append(position())
        if peek_char() == '\n':
            get_char()

    return positions


def position():
    c = peek_char()
    if c != '<':
        raise ValueError("Expecting '<' at position {0} but was {1}".format(pos, c))
    get_char()

    pos_tuple = args()

    c = peek_char()
    if c != '>':
        raise ValueError("Expecting '>' at position {0} but was {1}".format(pos, c))
    get_char()

    return pos_tuple


def comma():
    c = get_char()
    if c != ',':
        raise ValueError("Expecting ',' at position {0} but was {1}".format(pos, c))
    c = get_char()
    if c != ' ':
        raise ValueError("Expecting ' ' at position {0} but was {1}".format(pos, c))


def identifier():
    c = get_char()
    value = ord(c)
    if not (97 <= value <= 122):
        raise ValueError("Expecting letter at position {0} but was {1}".format(pos, c))

    get_char()
    return c


def number():
    num = ''
    value = peek_char()
    if value == '-':
        num += get_char()
        value = peek_char()

    ord_value = ord(value)
    while 48 <= ord_value <= 57:
        num += get_char()
        ord_value = ord(peek_char())

    return int(num)


def arg():
    return identifier(), number()


def args():
    x = arg()
    comma()
    y = arg()
    comma()
    z = arg()
    return (x[1], y[1], z[1])


def apply_velocity(pair):
    position, velocity = pair
    return (position[0] + velocity[0], position[1] + velocity[1], position[2] + velocity[2]), velocity


def change(a, b):
    val = 0
    if a < b:
        val = 1
    elif a > b:
        val = -1
    return val


def apply_gravity(a, b):
    pos_1, pos_2 = a[0], b[0]
    vel_1, vel_2 = a[1], b[1]

    new_velocity = (vel_1[0] + change(pos_1[0], pos_2[0]),
                    vel_1[1] + change(pos_1[1], pos_2[1]),
                    vel_1[2] + change(pos_1[2], pos_2[2])
                    )

    return pos_1, new_velocity


def accumulate_gravity(obj, objects):
    for item in objects:
        obj = apply_gravity(obj, item)
    return obj


with open('day12.txt', 'r') as file:
    positions = parse()
    position_and_velocity = list(map(lambda x: (x, (0, 0, 0)), positions))

    x_match, y_match, z_match = False, False, False
    match = False
    c = 1
    while not match:
        for index in range(4):
            list_slice = position_and_velocity[:index] + position_and_velocity[index + 1:]
            position_and_velocity[index] = accumulate_gravity(position_and_velocity[index], list_slice)

        position_and_velocity = list(map(lambda x: apply_velocity(x), position_and_velocity))

        if not x_match:
            x_match = (
                    (position_and_velocity[0][1][0] == 0) and
                    (position_and_velocity[1][1][0] == 0) and
                    (position_and_velocity[2][1][0] == 0) and
                    (position_and_velocity[3][1][0] == 0)
            )
            x_cycle = 2 * c

        if not y_match:
            y_match = (
                    position_and_velocity[0][1][1] == 0 and
                    position_and_velocity[1][1][1] == 0 and
                    position_and_velocity[2][1][1] == 0 and
                    position_and_velocity[3][1][1] == 0
            )
            y_cycle = 2 * c

        if not z_match:
            z_match = (
                    position_and_velocity[0][1][2] == 0 and
                    position_and_velocity[1][1][2] == 0 and
                    position_and_velocity[2][1][2] == 0 and
                    position_and_velocity[3][1][2] == 0
            )
            z_cycle = 2 * c

        match = x_match and y_match and z_match
        if c == 1000:
            total = 0
            for item in position_and_velocity:
                total += reduce(lambda x, y: abs(x) + abs(y), item[0]) * reduce(lambda x, y: abs(x) + abs(y), item[1])
            print("Day 12 Part 1:", total)

        c += 1

    lcm_xy = x_cycle * y_cycle // gcd(x_cycle, y_cycle)
    lcm_xyz = lcm_xy * z_cycle // gcd(lcm_xy, z_cycle)
    print("Day 12 Part 2:", lcm_xyz)
