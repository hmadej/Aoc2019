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
READ = 3
WRIT = 4
JMPT = 5
JMPF = 6
LESS = 7
EQUA = 8
HALT = 99

gPOSITION = 0
gMEMORY_PTR = 0
gMEMORY_TABLE = dict()


class Instruction():
    '''
    modes order C,B,A
    '''

    def __init__(self, operation, modes, parameters):
        # print(modes, operation, parameters)
        self.op = operation
        self.mode_1, self.mode_2, self.mode_3 = modes
        self.input_1, self.input_2, self.output = parameters

    def execute(self, memory):
        global gMEMORY_PTR
        value1 = (self.input_1 if self.mode_1 == 1 else _seek(memory, self.input_1))
        value2 = (self.input_2 if self.mode_2 == 1 else _seek(memory, self.input_2))

        if self.op == ADD:
            memory[self.output] = value1 + value2

        elif self.op == MUL:
            memory[self.output] = value1 * value2

        elif self.op == JMPT:
            if value1 != 0:
                _jump(value2)

        elif self.op == JMPF:
            if value1 == 0:
                _jump(value2)

        elif self.op == LESS:
            memory[self.output] = (1 if value1 < value2 else 0)

        elif self.op == EQUA:
            memory[self.output] = (1 if value1 == value2 else 0)

        elif self.op == READ:
            print("INPUT: ")
            value = int(input())
            memory[self.input_1] = value

        elif self.op == WRIT:
            print("OUTPUT: {0}".format(value1))
        elif self.op == HALT:
            print("END")
        else:
            raise ValueError("Unknown Operation {0}".format(self.op))


def get_char():
    global gPOSITION, file
    char = file.read(1)
    gPOSITION += 1
    return char


def peek_char():
    char = file.read(1)
    file.seek(gPOSITION)
    return char


def add_to_table(value):
    global gMEMORY_TABLE, gMEMORY_PTR

    if gMEMORY_PTR not in gMEMORY_TABLE.keys():
        gMEMORY_TABLE[gMEMORY_PTR] = value

    gMEMORY_PTR += 1


def parse():
    global gMEMORY_PTR, gPOSITION, gMEMORY_TABLE

    gPOSITION = 0
    gMEMORY_PTR = 0
    gMEMORY_TABLE = dict()
    opcode()

    while peek_char() == ',':
        get_char()  # consume ','
        opcode()


def opcode():
    global gMEMORY_PTR
    '''
    ABCDE
      1002
    
    DE - two-digit opcode,      02 == opcode 2
    C - mode of 1st parameter,  0 == position mode
    B - mode of 2nd parameter,  1 == immediate mode
    A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero
    '''
    op_string = ''

    while peek_char() != ',' and peek_char() != '':
        op_string += get_char()

    if gMEMORY_PTR in gMEMORY_TABLE.keys():
        instr_value = gMEMORY_TABLE[gMEMORY_PTR]
        op_string = str(instr_value)
        gMEMORY_PTR += 1
    else:
        instr_value = int(op_string)
        add_to_table(instr_value)

    op_length = len(op_string)
    modes = param_modes(op_string)

    if op_string[-1] == '1':
        args = arguments3()
        parameters = (args[0], args[1], args[2])
        Instruction(ADD, modes, parameters).execute(gMEMORY_TABLE)

    elif op_string[-1] == '2':
        args = arguments3()
        parameters = (args[0], args[1], args[2])
        Instruction(MUL, modes, parameters).execute(gMEMORY_TABLE)

    elif op_string[-1] == '3':
        arg = argument()
        Instruction(READ, modes, (arg, 0, 0)).execute(gMEMORY_TABLE)

    elif op_string[-1] == '4':
        arg = argument()
        Instruction(WRIT, modes, (arg, 0, 0)).execute(gMEMORY_TABLE)

    elif op_string[-1] == '5':
        args = arguments2()
        Instruction(JMPT, modes, (args[0], args[1], 0)).execute(gMEMORY_TABLE)

    elif op_string[-1] == '6':
        args = arguments2()
        Instruction(JMPF, modes, (args[0], args[1], 0)).execute(gMEMORY_TABLE)

    elif op_string[-1] == '7':
        args = arguments3()
        parameters = (args[0], args[1], args[2])
        Instruction(LESS, modes, parameters).execute(gMEMORY_TABLE)

    elif op_string[-1] == '8':
        args = arguments3()
        parameters = (args[0], args[1], args[2])
        Instruction(EQUA, modes, parameters).execute(gMEMORY_TABLE)

    elif op_string[-1] == '9':
        if peek_char() == '':  # no additional memory locations
            Instruction(HALT, modes, (0, 0, 0)).execute(gMEMORY_TABLE)
        else:
            memory()
            Instruction(HALT, modes, (0, 0, 0)).execute(gMEMORY_TABLE)
    else:
        raise ValueError('Invalid opcode {0}'.format(op_string))


def param_modes(opcode_string):
    op_length = len(opcode_string)
    # C, B, A
    if op_length == 3:
        modes = int(opcode_string[0]), 0, 0
    elif op_length == 4:
        modes = int(opcode_string[1]), int(opcode_string[0]), 0
    else:
        modes = 0, 0, 0

    return modes


def arguments2():
    input_value1 = argument()
    input_value2 = argument()

    return [input_value1, input_value2]


def arguments3():
    input_value1 = argument()
    input_value2 = argument()
    output_value1 = argument()

    return [input_value1, input_value2, output_value1]


def argument():
    global gMEMORY_PTR

    char = get_char()  # consume ,
    val = value()

    if gMEMORY_PTR in gMEMORY_TABLE.keys():
        val = gMEMORY_TABLE[gMEMORY_PTR]
        gMEMORY_PTR += 1
    else:
        add_to_table(val)

    return val


def memory():  # may have to be changed now jumps possible
    while peek_char() == ',':
        get_char()  # consume ','
        if gMEMORY_PTR not in gMEMORY_TABLE.keys():
            add_to_table(value())


def value():
    digit = ''
    if peek_char() == '-':
        digit += get_char()
    while peek_char() in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        digit += get_char()

    return int(digit)


def _jump(pointer):
    global file, gPOSITION, gMEMORY_PTR

    offset = gMEMORY_PTR - pointer
    if offset > 0:
        while offset != 0:
            if peek_char() == ',':
                offset -= 1
                argument()
            elif peek_char() == '':
                break

    else:
        gPOSITION = 0
        gMEMORY_PTR = 0
        file.seek(0)
        while gMEMORY_PTR != pointer:
            if peek_char() == ',':
                gMEMORY_PTR += 1
            get_char()

        gPOSITION -= 1
        file.seek(gPOSITION)


def _seek(memory, pointer):
    global file, gPOSITION

    if pointer in memory.keys():
        return memory[pointer]
    else:
        offset = 0
        temp_g_position = gPOSITION
        gPOSITION = 0
        file.seek(0)
        while offset != pointer:
            if peek_char() == ',':
                offset += 1
            get_char()

        if peek_char() == ',':
            get_char()  # consume ','

        val = value()
        memory[pointer] = val

        file.seek(temp_g_position)
        gPOSITION = temp_g_position
        return memory[pointer]


with open("day5.txt", "r") as file:
    parse()
