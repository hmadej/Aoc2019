# space image format
from functools import reduce

gPOSITION = 0
gPIXEL_WIDE = 25
gPIXEL_TALL = 6

'''
Parse   -> Layer [Layer]
Layer   -> Pixel^6
Pixel   -> Digit^25
Digit   -> '0' | '1' | ... | '9'
'''


def get_char():
    global gPOSITION, file
    char = file.read(1)
    gPOSITION += 1

    return char


def peek_char():
    char = file.read(1)
    file.seek(gPOSITION)

    return char


def parse():
    image = [layer()]
    while peek_char() != '':
        image.append(layer())

    return image


def layer():
    pixels = []
    count = 0
    for _ in range(gPIXEL_TALL):
        zeros, value = pixel()
        count += zeros
        pixels.append(value)

    return (count, pixels)


def pixel():
    count = 0
    string = ''
    for _ in range(gPIXEL_WIDE):
        char = get_char()
        if char == '0':
            count += 1
        string += char

    return count, string


def draw(frame_buffer):
    for row in frame_buffer:
        print(reduce(lambda x, y: x + ('  ' if y == '0' else '\u2591\u2591'), row, ''))


def update(frame_buffer, next_layer):
    new_frame = ''
    for index in range(25):
        if next_layer[index] == '2':
            new_frame += frame_buffer[index]
        else:
            new_frame += next_layer[index]
    return new_frame


with open('day8.txt', 'r') as file:
    image = parse()
    count, layer = reduce(lambda x, y: x if x[0] < y[0] else y, image)
    layer = reduce(lambda x, y: x + y, layer)
    ones, twos = 0, 0
    for char in layer:
        if char == '1':
            ones += 1
        elif char == '2':
            twos += 1

    print("day 8 part 1:", ones * twos)

    stripped_image = reduce(lambda a, b: a + [b[1]], image, [])

    stripped_image.reverse()
    frame_buffer = ['2' * gPIXEL_WIDE for _ in range(gPIXEL_TALL)]

    for layer in stripped_image:
        for index in range(6):
            frame_buffer[index] = update(frame_buffer[index], layer[index])

    draw(frame_buffer)
