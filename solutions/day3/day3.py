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
    lines1 = wire()
    if (ord(peekChar()) != 10):
        print(peekChar())
        raise ValueError("Expected newline separating wires")
    else:
        getChar()
    lines2 = wire()

    return (lines1, lines2)

def wire():
    moves = []
    position = (0, 0)

    position = move(position)
    moves.append(position)

    while (peekChar() == ','):
        getChar()
        position = move(position)
        moves.append(position)

    return moves

def move(pos):
    direct = direction()
    magnitude = digits()
    if (direct == 'R'):
        position = (pos[0] + magnitude, pos[1])
    elif (direct == 'L'):
        position = (pos[0] - magnitude, pos[1])
    elif (direct == 'U'):
        position = (pos[0], pos[1] + magnitude)
    elif (direct == 'D'):
        position = (pos[0], pos[1] - magnitude)
    else:
        raise ValueError("Direction error! got {0} expecting R, L, U, D".format(direct))
    return position

def direction():
    return getChar()

def digits():
    digit = ''
    while (peekChar() in symbols):
        digit += getChar()

    return int(digit)

with open("day3.txt") as file:
    lines = program()
