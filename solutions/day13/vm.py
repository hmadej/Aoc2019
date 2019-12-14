from enum import Enum
from pipes import Pipe


class Status(Enum):
    ALIVE = 0
    HALT  = -1
    ERR   = -2

class Instruction(Enum):
    ADD = 1
    MUL = 2
    READ = 3
    WRITE = 4
    JMPT = 5
    JMPF = 6
    LESS = 7
    EQUAL = 8
    RELB = 9
    HALT = 99

class Mode(Enum):
    POSITIONAL = 0
    IMMEDIATE  = 1
    RELATIVE   = 2

def is_numeric(char):
    if char == '':
        return False
    value = ord(char)
    if (value >= 48 and value <= 57):
        return True
    return False

class Machine():
    def __init__(self, memory, in_pipe, out_pipe, status_reg, args):
        self.memory = memory
        self.instruction_pointer = 0
        self.relative_base = 0
        self.in_pipe = in_pipe
        self.out_pipe = out_pipe
        self.status_reg = status_reg
        self.args = args

    def execute(self):
        while (self.memory[self.instruction_pointer] != Instruction.HALT.value):
            self.interpret()

        self.interpret()


    def interpret(self):
        '''
        ABCDE
         1202
        
        DE - two-digit opcode,      02 == opcode 2
        C - mode of 1st parameter,  2 == relative mode
        B - mode of 2nd parameter,  1 == immediate mode
        A - mode of 3rd parameter,  0 == position mode,
                                    omitted due to being a leading zero
        '''
        instruction = self.memory[self.instruction_pointer]

        opcode = (instruction % 100)

        mode3 = instruction // 10000
        mode2 = (instruction % 10000) // 1000
        mode1 = (instruction % 1000) // 100

        if opcode == Instruction.ADD.value:
            parameter_1 = self.read()
            parameter_2 = self.read()
            parameter_3 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            input_2 = self.get_memory(mode2, parameter_2)
            self.set_memory(mode3, parameter_3, (input_1 + input_2))

        elif opcode == Instruction.MUL.value:
            parameter_1 = self.read()
            parameter_2 = self.read()
            parameter_3 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            input_2 = self.get_memory(mode2, parameter_2)
            self.set_memory(mode3, parameter_3, (input_1 * input_2))

        elif opcode == Instruction.READ.value:
            parameter_1 = self.read()
            if len(self.args) != 0:
                input_2 = self.args.pop()
            else:
                input_2 = self.in_pipe.get_input()

            self.set_memory(mode1, parameter_1, input_2)

        elif opcode == Instruction.WRITE.value:
            parameter_1 = self.read()
            output = self.get_memory(mode1, parameter_1)
            self.out_pipe.set_output(output)

        elif opcode == Instruction.JMPT.value:
            parameter_1 = self.read()
            parameter_2 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            if (input_1 != 0):
                input_2 = self.get_memory(mode2, parameter_2)
                self.instruction_pointer = input_2 - 1

        elif opcode == Instruction.JMPF.value:
            parameter_1 = self.read()
            parameter_2 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            if (input_1 == 0):
                input_2 = self.get_memory(mode2, parameter_2)
                self.instruction_pointer = input_2 - 1

        elif opcode == Instruction.LESS.value:
            parameter_1 = self.read()
            parameter_2 = self.read()
            parameter_3 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            input_2 = self.get_memory(mode2, parameter_2)
            self.set_memory(mode3, parameter_3, (1 if input_1 < input_2 else 0))

        elif opcode == Instruction.EQUAL.value:
            parameter_1 = self.read()
            parameter_2 = self.read()
            parameter_3 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            input_2 = self.get_memory(mode2, parameter_2)

            self.set_memory(mode3, parameter_3, (1 if input_1 == input_2 else 0))

        elif opcode == Instruction.RELB.value:
            parameter_1 = self.read()
            input_1 = self.get_memory(mode1, parameter_1)
            self.relative_base += input_1
        
        elif opcode == Instruction.HALT.value:
            self.status_reg.set_output(Status.HALT.value)

        else:
            self.status_reg.set_output(Status.ERR.value)
            raise ValueError("Invalid OPCODE @ IP:{0} CODE:{1}".format(self.instruction_pointer, opcode))
    
        self.instruction_pointer += 1
            
    def read(self):
        self.instruction_pointer += 1
        return self.memory[self.instruction_pointer]

    def __lookup(self, pointer):
        val = 0
        if pointer in self.memory.keys():
            val = self.memory[pointer]
        else:
            self.memory[pointer] = 0
        return val
        


    def get_memory(self, mode, parameter):
        if mode == Mode.POSITIONAL.value:
            value = self.__lookup(parameter)
        elif mode == Mode.IMMEDIATE.value:
            value = parameter
        elif mode == Mode.RELATIVE.value:
            value = self.__lookup(self.relative_base + parameter)

        return value

    def set_memory(self, mode, parameter, result):
        if mode == Mode.POSITIONAL.value:
            address = parameter
        elif mode == Mode.IMMEDIATE.value:
            self.status_reg.set_output(Status.ERR.value)
            raise ValueError("Immediate mode in output!")
            address = parameter
        elif mode == Mode.RELATIVE.value:
            address = parameter + self.relative_base

        self.memory[address] = result

class Parser():
    def __init__(self, file):
        self.filename = file
        self.position = 0
        self.file_pointer = None

    def getChar(self):
        char = self.file_pointer.read(1)
        self.position += 1
        return char

    def peekChar(self):
        char = self.file_pointer.read(1)
        self.file_pointer.seek(self.position)
        return char

    def parse(self):
        program_memory = dict()
        index = 0
        with open(self.filename, 'r') as self.file_pointer:
            while (self.peekChar() != ''):
                program_memory[index] = self.numeric()
                index += 1
                self.getChar()

        return program_memory


    def numeric(self):
        # digit
        value = ''
        if (self.peekChar() == '-'):
            value += self.getChar()
        while (is_numeric(self.peekChar())): #(48 - 57)
            value += self.getChar()
        return int(value)

