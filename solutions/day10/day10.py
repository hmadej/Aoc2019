from functools import reduce
from math import sqrt, cos

gPOSITION = 0


'''
parse    -> row ['\n' row]
row      -> node [node]
node     -> asteroid | empty
empty    -> '.'
asteroid -> '#'
'''

def getChar():
    global gPOSITION, file
    char = file.read(1)
    gPOSITION += 1

    return char


def peekChar():
    char = file.read(1)
    file.seek(gPOSITION)

    return char

def parse():
    asteroid_map = []
    galaxy_map = dict()
    y = 0
    x = row(asteroid_map, galaxy_map, y)
    while (peekChar() != ''):
        y += 1
        getChar()
        row(asteroid_map, galaxy_map, y)

    return (x, y), asteroid_map, galaxy_map

def row(map, map2, y):
    x = 0
    c = getChar()
    if c == '#':
        map.append((x,y))

    map2[(x,y)] = c
    x += 1

    while (peekChar() != ''):
        if (peekChar() == '\n'):
            return x
        else:
            c = peekChar()
            if c == '#':
                getChar()
                map.append((x,y))
            elif c == '.':
                getChar()
            map2[(x,y)] = c

            x += 1
    return x


def draw(map):
    for y in range(41):
        for x in range(41):
            print(map[(x,y)], end = '')
        print()
    input()

def quadrant(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]

    if x >= 0 and y >= 0:
        q = 1
    elif x < 0 and y < 0:
        q = 3
    elif x < 0 and y >= 0:
        q = 2
    else:
        q = 0

    return q

def visible(asteroid_map, start, w):
    count = 0
    slopes = [set(), set(), set(), set()]
    slope_maps = [[],[],[],[]]
    for asteroid in asteroid_map:
        num = asteroid[0] - start[0]
        denom = asteroid[1] - start[1]
        q = quadrant(asteroid, start)
        if denom == 0:
            slope = float('inf')
        else:
            slope = num / denom

        if slope not in slopes[q]:
            slopes[q].add(slope)
            count += 1

        slope_maps[q].append((slope, asteroid))
    
    return count, slope_maps


def dist(a, b):
    return sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]))


def sweep(asteroid_map, gmap):
    order = []
    count = 0
    while count < 200:
        for index in range(4):
            print("Q{0}".format(index))
            remove = []
            #print("{0}BEFORE:".format(index), asteroid_map[index])
            if asteroid_map[index]:
                previous_asteroid = asteroid_map[index][0]
                remove.append(previous_asteroid)
                order.append(previous_asteroid)
                count += 1
                gmap[previous_asteroid[1]] = 'B'
                print("BLASTED: {0}".format(previous_asteroid))
                draw(gmap)
                if count == 200:
                    return previous_asteroid, order

                for asteroid in asteroid_map[index][1:]:
                    if previous_asteroid[0] != asteroid[0]:
                        previous_asteroid = asteroid
                        gmap[previous_asteroid[1]] = 'B'
                        print("BLASTED: {0}".format(previous_asteroid))
                        draw(gmap)
                        remove.append(asteroid)
                        order.append(previous_asteroid)
                        count += 1
                        if count == 200:
                            return previous_asteroid, order

            for asteroid in remove:
                asteroid_map[index].remove(asteroid)

            #print("{0}AFTER:".format(index), asteroid_map[index])

with open('day10.txt', 'r') as file:
    dimensions, asteroid_map, galaxy_map = parse()
    max_asteroid = (0,0)
    max_count = 0
    max_slope_maps = []
    for asteroid in asteroid_map:
        copy = asteroid_map.copy()
        copy.remove(asteroid)
        temp, slope_maps = visible(copy, asteroid, dimensions[0])
        if temp > max_count:
            max_count = temp
            max_asteroid = asteroid
            max_slope_maps = slope_maps

    print(max_asteroid, max_count)

    for index in range(4):
        max_slope_maps[index].sort(key = lambda x : dist(max_asteroid, x[1]))
        max_slope_maps[index].sort(key = lambda x : x[0], reverse = True)

    galaxy_map[max_asteroid] = 'X'
    a, b = sweep(max_slope_maps, galaxy_map)
    #print(b)
    
