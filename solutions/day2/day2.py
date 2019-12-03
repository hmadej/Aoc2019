
'''
program         -> opcode [, opcode]
opcode          -> '1' arguments | '2' arguments | '99' memory
arguments       -> argument argument argument
argument        -> memoryLocation ','
memoryLocation  -> '0' | '1' | ... | '9'
memory          -> memoryLocation ',' | memoryLocation
'''
EOF = ''
ADD = 1
MUL = 2
HALT = 99

position = 0


def getChar():
    global position, file
    char = file.read(1)
    position += 1
    return char

def peekChar():
    position, file
    char = file.read(1)
    file.seek(position)
    
    return char


def program():
    ops = opcode()
    while (peekChar() == ','):
      getChar() # consume ','
      ops += opcode()
    return ops

def opcode():
    char = getChar()
    if char == '1' or char == '2':
        args = arguments()
        return [int(char)] + args

    elif char == '9':
        getChar() # consume 9
        if (peekChar() == ''): # no additional memory locations
            return [99]
        else:
            return [99] + memory()

    else:
        raise ValueError('Character at position {0} is {1}, expected 1, 2'.format(0, char))

def arguments():
    input_location1 = argument()
    input_location2 = argument()
    output_location1 = argument()
    return [input_location1, input_location2, output_location1]

def argument():
    char = getChar()
    if char != ',':
        raise ValueError('Character at position {0} is ",", expected value'.format(0, char))
    return memoryLocation()


def memory():
    memory = []
    while (peekChar() == ','):
      getChar() # consume ','
      memory.append(memoryLocation())

    return memory

def memoryLocation():
    digit = ''
    while (peekChar() in ['0','1','2','3','4','5','6','7','8','9']):
        digit += getChar()

    return int(digit)

def evaluate(program):
    for instu_pointer in range(len(program) // 4):
        if program[instu_pointer*4] == ADD:
            program[program[instu_pointer*4 + 3]] = (
                program[program[instu_pointer*4 + 1]] + 
                program[program[instu_pointer*4 + 2]]
              )
        elif program[instu_pointer*4] == MUL:
            program[program[instu_pointer*4 + 3]] = (
                program[program[instu_pointer*4 + 1]] * 
                program[program[instu_pointer*4 + 2]]
            )
        elif program[instu_pointer*4] == HALT:
            break
        else:
            raise ValueError("something bad happened!")

    return program[0]

with open("day2.txt", "r") as file:
    program = program()
    print(evaluate(program.copy()))
    

    for noun in range(100):
        for verb in range(100):
            p = program.copy()
            p[1], p[2] = noun, verb
            result = evaluate(p)
            if (result == 19690720):
                print(noun, verb)
                print(100 * noun + verb)
                break