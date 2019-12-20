from functools import reduce


def mod(num):
    if num < 0:
        return 10 - (num % 10)
    else:
        return num % 10


def get_char(file):
    char = file.read(1)
    return char


def peek_char(file):
    pos = file.tell()
    char = file.read(1)
    file.seek(pos)
    return char


def parse(file_name):
    array = []
    length = 0
    with open(file_name, 'r') as file:
        while peek_char(file) != '':
            array.append(int(get_char(file)))
            length += 1
    return length, array


def pattern(base, phase):
    i = 0
    while True:
        value = base[i]
        for _ in range(phase):
            yield value
        i = (i + 1) % 4


def repeat(base, length):
    phase, i = 1, 0
    while True:
        p = pattern(base, phase)
        while i != length:
            value = next(p)
            if i == 0:
                value = next(p)
                yield value
            else:
                yield value
            # print(value, phase)
            i += 1

        phase += 1
        i = 0


input_length, input_array = parse('day16.txt')

for _ in range(100):
    output_array = []
    p = repeat([0, 1, 0, -1], input_length)
    for index in range(input_length):
        # print("INDEX: {0}".format(index))
        output_array.append(reduce(lambda x, y: x + y * next(p), input_array, 0))
        output_array = list(map(mod, output_array))
    input_array = output_array.copy()

print(input_array[:8])

"""
[0, 1, 0, 1]
pattern length ->
  a b c d e f g 
a 1 0 1 0 1 0 1
b 0 1 1 0 0 1 1
c 0 0 1 1 1 0 0
d 0 0 0 1 1 1 1
e 0 0 0 0 1 1 1
f 0 0 0 0 0 1 1
g 0 0 0 0 0 0 1

g = 1*g
f = 1*f + 1*g
e = 1*e + m[f,g]
d = 1*d + m[e,f,g]
c = 1*c + 1*d + 1*e
b = 1*b + 1*c + m[f,g]
a = 1*a + 1*c + 1*e + 1*g

"""
