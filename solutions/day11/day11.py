import vm, threading
from enum import Enum
from functools import reduce
from pipes import ConcurrentPipe


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


def rotate(direction, rotation):
    rotate = (-1 if rotation == 0 else 1)
    return Direction((direction.value + rotate) % 4)


def robot_paint(in_pipe, out_pipe, thread, initial_value):
    hull = dict()
    x, y = 0, 0
    in_pipe.set_output(initial_value)
    thread.start()
    robot_direction = Direction.North

    while thread.is_alive():
        colour = out_pipe.get_input()
        rotation = out_pipe.get_input()
        robot_direction = rotate(robot_direction, rotation)

        hull[(x, y)] = colour

        if robot_direction == Direction.North:
            y += 1
        elif robot_direction == Direction.East:
            x += 1
        elif robot_direction == Direction.South:
            y -= 1
        else:
            x -= 1

        if (x, y) in hull.keys():
            in_pipe.set_output(hull[(x, y)])
        else:
            in_pipe.set_output(0)

    thread.join()

    return hull


def run(program, in_pipe, out_pipe):
    brain = vm.Machine(program, in_pipe, out_pipe, [])
    brain.execute()


p = vm.Parser('day11.txt')
program = p.parse()
in_pipe = ConcurrentPipe()
out_pipe = ConcurrentPipe()

brain = threading.Thread(target=run, args=(program.copy(), in_pipe, out_pipe))
hull = robot_paint(in_pipe, out_pipe, brain, 0)

print("Day 11 Part 1:", len(hull.keys()))
in_pipe.get_input()

brain = threading.Thread(target=run, args=(program.copy(), in_pipe, out_pipe))
hull = robot_paint(in_pipe, out_pipe, brain, 1)

positions = hull.keys()

min_x = reduce(lambda x, y: min(x, y[0]), positions, 10000)
max_x = reduce(lambda x, y: max(x, y[0]), positions, -10000)
min_y = reduce(lambda x, y: min(x, y[1]), positions, 10000)
max_y = reduce(lambda x, y: max(x, y[1]), positions, -10000)

rows = []
for y in range((max_y - min_y) + 1):
    row = ''
    for x in range((max_x - min_x) + 1):
        pos = (min_x + x, min_y + y)
        if pos in hull.keys():
            row += ('..' if hull[pos] == 0 else '##')
        else:
            row += '..'
    rows.append(row)

rows.reverse()

print("Day 11 Part 2:")
for row in rows:
    print(row)
