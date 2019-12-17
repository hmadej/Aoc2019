from functools import reduce

# Universal Orbit Map


# construct graph, and then DFS starting any node, repeat
# storing distance 
# keep map of nodes with visited

# or 

# construct graph, and BFS from COM

'''
parse -> pair ['\n' pair]
pair  -> node ')' node
node  -> [alphanumeric]
alphanumeric -> '0' | '1' | ... | '9' | 'A' | 'B' | ... | 'Z'
'''

gPOSITION = 0


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
    table = dict()

    pair(table)
    while peek_char() == '\n':
        get_char()
        pair(table)

    return table


def pair(table):
    a = node()
    char = get_char()
    b = node()
    table[b] = a
    # print("{0}<-{1}".format(a, b))


def node():
    # digit or char
    node_id = ''
    while alphanumeric(peek_char()):  # (48 - 57) (65 - 90)
        node_id += get_char()
    return node_id


def alphanumeric(char):
    if char == '':
        return False

    value = ord(char)
    if (48 <= value <= 57) or (65 <= value <= 90):
        return True
    return False


def orbits(store, table, entry, destination):
    if entry == destination:
        return 0
    if entry not in store.keys():
        store[entry] = 1 + orbits(store, table, table[entry], destination)
    return store[entry]


def trace(store, table, entry, destination):
    if entry == destination:
        return entry
    if entry not in store.keys():
        store[entry] = table[entry]
        return trace(store, table, table[entry], destination)
    else:
        return entry


with open('day6.txt', 'r') as file:
    table = parse()
    memory = dict()
    total_orbits = reduce(lambda x, y: x + y, [orbits(memory, table, key, 'COM') for key in table.keys()])
    print("DAY6 PART1: {0}".format(total_orbits))

    memory2 = dict()
    trace(memory2, table, 'SAN', 'COM')
    middle = trace(memory2, table, 'YOU', 'COM')
    rotations_to_SAN = orbits(dict(), table, 'SAN', middle) + orbits(dict(), table, 'YOU', middle) - 2
    print("DAY6 PART2: {0}".format(rotations_to_SAN))
