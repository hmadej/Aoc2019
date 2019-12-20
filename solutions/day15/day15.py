import vm, threading
from enum import Enum
from pipes import ConcurrentPipe, Pipe
from functools import reduce


class Direction(Enum):
    North = 1
    South = 2
    West = 3
    East = 4


directions = {
    Direction.North: Direction.South,
    Direction.South: Direction.North,
    Direction.West: Direction.East,
    Direction.East: Direction.West
}


def neighbours(graph, visited, node):
    x, y = node
    nodes = []
    for (a, b) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        key = (x + a, y + b)
        if key in graph.keys() and graph[key] != 0 and key not in visited:
            nodes.append(key)
    return nodes


def spf(graph, source):
    distance = dict()
    previous = dict()
    vertices = [source]
    visited = set()

    max_distance = len(graph.keys()) + 1

    for vertex in graph.keys():
        distance[vertex] = max_distance
        previous[vertex] = None

    distance[source] = 0
    while len(vertices) != 0:
        next = vertices.pop()
        visited.add(next)

        for neighbour in neighbours(graph, visited, next):
            dist = distance[next] + 1  # replace 1 with distance function from next to neighbour of next
            if dist < distance[neighbour]:
                distance[neighbour] = dist
                previous[neighbour] = next
            vertices.append(neighbour)

    return distance, previous


def draw(tiles, width, height):
    a, b = width
    c, d = height
    for y in range(c, d):
        for x in range(a, b):
            if (x, y) in tiles.keys():
                print('#' if tiles[(x, y)] == 0 else tiles[(x, y)], end='')
            else:
                print('.', end='')
        print()


def update_position(position, direction):
    x, y = position
    if direction == Direction.North:
        y += 1
    elif direction == Direction.South:
        y -= 1
    elif direction == Direction.East:
        x += 1
    elif direction == Direction.West:
        x -= 1
    return x, y


def run(program_memory, input_pipe, output_pipe, status_register):
    vm.Machine(program_memory, input_pipe, output_pipe, status_register, []).execute()


program = vm.Parser('day15.txt').parse()

in_pipe = ConcurrentPipe()
out_pipe = ConcurrentPipe()
status = Pipe()
current_position = (0, 0)
explored = dict()
explored[current_position] = 1

brain = threading.Thread(target=run, args=(program.copy(), in_pipe, out_pipe, status))
brain.start()

stack = []
for key, value in directions.items():
    stack.append(key)
    stack.append(value)

while len(stack) != 0:
    direction = stack.pop()
    current_position = update_position(current_position, direction)
    in_pipe.set_output(direction.value)
    status_code = out_pipe.get_input()

    if status_code == 0:
        explored[current_position] = status_code
        current_position = update_position(current_position, stack.pop())
    elif status_code == 1 or status_code == 2:
        if current_position not in explored.keys():
            for key, value in directions.items():
                stack.append(key)
                stack.append(value)
        explored[current_position] = status_code

    if status_code == 2:
        destination = current_position

draw(explored, (-25, 25), (-25, 25))


dist, prev = spf(explored, (0, 0))
print("Day 15 Part 1: {0}".format(dist[destination]))

dist, prev = spf(explored, destination)

print("Day 15 Part 2: {0}".format(reduce(max, filter(lambda x: x != 1661, dist.values()))))