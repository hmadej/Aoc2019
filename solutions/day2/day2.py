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

OUTPUT_OFFSET = 3
INPUT1_OFFSET = 1
INPUT2_OFFSET = 2

position = 0


def get_char():
    global position, file
    char = file.read(1)
    position += 1
    return char


def peek_char():
    position, file
    char = file.read(1)
    file.seek(position)

    return char


def program():
    ops = opcode()
    while peek_char() == ',':
        get_char()  # consume ','
        ops += opcode()
    return ops


def opcode():
    char = get_char()
    if char == '1' or char == '2':
        args = arguments()
        return [int(char)] + args

    elif char == '9':
        get_char()  # consume 9
        if peek_char() == '':  # no additional memory locations
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
    char = get_char()
    if char != ',':
        raise ValueError('Character at position {0} is ",", expected value'.format(0, char))
    return memoryLocation()


def memory():
    memory = []
    while peek_char() == ',':
        get_char()  # consume ','
        memory.append(memoryLocation())

    return memory


def memoryLocation():
    digit = ''
    while peek_char() in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        digit += get_char()

    return int(digit)


def evaluate(program):
    instruction_pointer = 0
    while 1:
        if program[instruction_pointer] == ADD:
            output = (
                    program[program[instruction_pointer + INPUT1_OFFSET]] +
                    program[program[instruction_pointer + INPUT2_OFFSET]]
            )
            program[program[instruction_pointer + OUTPUT_OFFSET]] = output
            instruction_pointer += 4
        elif program[instruction_pointer] == MUL:
            output = (
                    program[program[instruction_pointer + INPUT1_OFFSET]] *
                    program[program[instruction_pointer + INPUT2_OFFSET]]
            )
            program[program[instruction_pointer + OUTPUT_OFFSET]] = output
            instruction_pointer += 4
        elif program[instruction_pointer] == HALT:
            instruction_pointer += 1
            break

    return program[0]


with open("day2.txt", "r") as file:
    program = program()
    print(evaluate(program.copy()))

    for noun in range(100):
        for verb in range(100):
            p = program.copy()
            p[1], p[2] = noun, verb
            result = evaluate(p)
            if result == 19690720:
                print(100 * noun + verb)
                break
