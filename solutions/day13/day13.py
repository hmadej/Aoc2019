
import vm, threading, time
from pipes import ConcurrentPipe, Pipe

program = vm.Parser('day13.txt').parse()
in_pipe = ConcurrentPipe()
out_pipe = ConcurrentPipe()
status = Pipe()

tile_set = {0 : '.', 1 : '#', 2 : '@', 3 : '-', 4 : 'o'}

def run(program, in_pipe, out_pipe, status):
    brain = vm.Machine(program, in_pipe, out_pipe, status, [])
    brain.execute()


def draw(tiles, width, height):
    for y in range(height):
        for x in range(width):
            if (x, y) in tiles.keys():
                print(tile_set[tiles[(x,y)]], end = '')
            else:
                print('.', end ='')
        print()
    print("score: {0}".format(tiles[(-1, 0)]))


def initialize(tiles, width, height, pipe):
    count = 0
    while (count != (width * height)):
        x = out_pipe.get_input()
        y = out_pipe.get_input()
        tile = out_pipe.get_input()

        if (x, y) not in tiles.keys():
            tiles[(x,y)] = tile
            count += 1
            if tile == 4:
                ball = (x, y)
            elif tile == 3:
                paddle = (x, y)

    output = set_paddle(paddle, ball)
    pipe.set_output(output)
    x = out_pipe.get_input()
    y = out_pipe.get_input()
    tile = out_pipe.get_input()
    tiles[(x,y)] = tile

    return ball, paddle, output

def set_paddle(paddle, ball):
    output = 0
    if paddle[0] < ball[0]:
        output = 1
    elif paddle[0] > ball[0]:
        output = -1

    return output

brain = threading.Thread(target = run, args=(program.copy(), in_pipe, out_pipe, status))
brain.start()

count = 0
width, height = 37, 22
tiles = dict()
tiles[(-1,0)] = 0

ball, paddle, output = initialize(tiles, width, height, in_pipe)

sequence, l = 4, 2


for tile in tiles.keys():
    if tiles[tile] == 2:
        count += 1

while (brain.is_alive()):

    if output != 0:
        sequence = 4
    else:
        sequence = 2

    for _ in range(sequence):
        x = out_pipe.get_input()
        y = out_pipe.get_input()
        tile = out_pipe.get_input()
        tiles[(x,y)] = tile

        if tile == 4:
            ball = (x, y)
        elif tile == 3:
            paddle = (x, y)

    if (status.get_input() == -1):
        draw(tiles, width, height)
        break

    while (x == -1):
        for _ in range(l):
            x = out_pipe.get_input()
            y = out_pipe.get_input()
            tile = out_pipe.get_input()
            tiles[(x,y)] = tile

            if tile == 4:
                ball = (x, y)
            elif tile == 3:
                paddle = (x, y)

    draw(tiles, width, height)

    output = set_paddle(paddle, ball)
    in_pipe.set_output(output)



print("Day 13 Part 1:", count)
print("Day 13 Part 2:", tiles[(-1, 0)])

