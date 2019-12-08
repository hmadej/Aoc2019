from functools import reduce
from itertools import permutations
from time import sleep
from collections import deque
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

class Instruction():
    '''
    modes order C,B,A
    '''
    def __init__(self, operation, modes, parameters):
        #print(modes, operation, parameters)
        self.op = operation
        self.mode_1, self.mode_2, self.mode_3 = modes
        self.input_1, self.input_2, self.output = parameters

    def execute(self, parser):
        value1 = (self.input_1 if self.mode_1 == 1 else parser._seek(self.input_1))
        value2 = (self.input_2 if self.mode_2 == 1 else parser._seek(self.input_2))

        if self.op == ADD:
            parser.memory_table[self.output] = value1 + value2

        elif self.op == MUL:
            parser.memory_table[self.output] = value1 * value2

        elif self.op == JMPT:
            if value1 != 0:
                parser._jump(value2)

        elif self.op == JMPF:
            if value1 == 0:
                parser._jump(value2)

        elif self.op == LESS:
            parser.memory_table[self.output] = (1 if value1<value2 else 0)

        elif self.op == EQUA:
            parser.memory_table[self.output] = (1 if value1==value2 else 0)

        elif self.op == READ:
            while (len(parser.inbox) == 0):
                sleep(1) # implement callback to next thread 
            parser.memory_table[self.input_1] = parser.inbox.popleft()
    
        elif self.op == WRIT:
            parser.outbox.append(value1)
        elif self.op == HALT:
            parser.inbox.append(-99)
            print("END")
        else:
            raise ValueError("Unknown Operation {0}".format(self.op))


class Parser():
    def __init__(self, file, memory_table, inbox, outbox):
        self.file_pointer = None
        self.filename = file
        self.position = 0
        self.memory_table = memory_table
        self.instruction_pointer = 0
        self.outbox = outbox
        self.inbox = inbox

    def parse(self):
        with open(self.filename, 'r') as self.file_pointer:
            self.opcode()
            while (self.peekChar() == ','):
                self.getChar()
                self.opcode()

    def getChar(self):
        char = self.file_pointer.read(1)
        self.position += 1
        return char


    def peekChar(self):
        char = self.file_pointer.read(1)
        self.file_pointer.seek(self.position)
        return char

    def add_to_table(self, value):
        if self.instruction_pointer not in self.memory_table.keys():
            self.memory_table[self.instruction_pointer] = value

        self.instruction_pointer += 1

    def param_modes(self, opcode_string):
        op_length = len(opcode_string)
        # C, B, A
        if op_length == 3:
            modes = int(opcode_string[0]), 0, 0
        elif op_length == 4:
            modes = int(opcode_string[1]), int(opcode_string[0]), 0
        else:
            modes = 0, 0, 0

        return modes

    def arguments2(self):
        input_value1 = self.argument()
        input_value2 = self.argument()

        return [input_value1, input_value2]

    def arguments3(self):
        input_value1 = self.argument()
        input_value2 = self.argument()
        output_value1 = self.argument()

        return [input_value1, input_value2, output_value1]

    def argument(self):
        char = self.getChar() # consume ,
        val = self.value()

        if self.instruction_pointer in self.memory_table.keys():
            val = self.memory_table[self.instruction_pointer]
            self.instruction_pointer += 1
        else:
            self.add_to_table(val)

        return val

    def memory(self): # may have to be changed now jumps possible
        while (self.peekChar() == ','):
            self.getChar() # consume ','
            if self.instruction_pointer not in self.memory_table.keys():
                self.add_to_table(self.value())

    def value(self):
        digit = ''
        if (self.peekChar() == '-'):
            digit += self.getChar()
        while (self.peekChar() in ['0','1','2','3','4','5','6','7','8','9']):
            digit += self.getChar()

        return int(digit)

    def opcode(self):
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

        while(self.peekChar() != ',' and self.peekChar() != ''):
            op_string += self.getChar()

        if self.instruction_pointer in self.memory_table.keys():
            instr_value = self.memory_table[self.instruction_pointer]
            op_string = str(instr_value)
            self.instruction_pointer += 1
        else:
            instr_value = int(op_string)
            self.add_to_table(instr_value)

        op_length = len(op_string)
        modes = self.param_modes(op_string)

        if op_string[-1] == '1':
            args = self.arguments3()
            parameters = (args[0],args[1],args[2])
            Instruction(ADD, modes, parameters).execute(self)

        elif op_string[-1] == '2':
            args = self.arguments3()
            parameters = (args[0],args[1],args[2])
            Instruction(MUL, modes, parameters).execute(self)

        elif op_string[-1] == '3':
            arg = self.argument()
            Instruction(READ, modes, (arg,0,0)).execute(self)

        elif op_string[-1] == '4':
            arg = self.argument()
            Instruction(WRIT, modes, (arg,0,0)).execute(self)

        elif op_string[-1] == '5':
            args = self.arguments2()
            Instruction(JMPT, modes, (args[0], args[1], 0)).execute(self)

        elif op_string[-1] == '6':
            args = self.arguments2()
            Instruction(JMPF, modes, (args[0], args[1], 0)).execute(self)

        elif op_string[-1] == '7':
            args = self.arguments3()
            parameters = (args[0],args[1],args[2])
            Instruction(LESS, modes, parameters).execute(self)

        elif op_string[-1] == '8':
            args = self.arguments3()
            parameters = (args[0],args[1],args[2])
            Instruction(EQUA, modes, parameters).execute(self)

        elif op_string[-1] == '9':
            if (self.peekChar() == ''): # no additional memory locations
                Instruction(HALT, modes, (0,0,0)).execute(self)
            else:
                self.memory()
                Instruction(HALT, modes, (0,0,0)).execute(self)
        else:
            raise ValueError('Invalid opcode {0}'.format(op_string))

    def _jump(self, pointer):

        offset = self.instruction_pointer - pointer
        if offset > 0:
            while (offset != 0):
                if (self.peekChar() == ','):
                    offset -= 1
                    self.argument()
                elif (self.peekChar() == ''):
                    break

        else:
            self.position = 0
            self.instruction_pointer = 0
            self.file_pointer.seek(0)
            while (self.instruction_pointer != pointer):
                if (self.peekChar() == ','):
                    self.instruction_pointer += 1
                self.getChar()

            self.position -= 1
            self.file_pointer.seek(self.position)


    def _seek(self, pointer):

        if pointer in self.memory_table.keys():
            return self.memory_table[pointer]
        else:
            offset = 0
            temp_POSITION = self.position
            self.position = 0
            self.file_pointer.seek(0)
            while (offset != pointer):
                if (self.peekChar() == ','):
                    offset += 1
                self.getChar()


            if (self.peekChar() == ','):
                self.getChar() # consume ','

            val = self.value()
            self.memory_table[pointer] = val

            self.file_pointer.seek(temp_POSITION)
            self.position = temp_POSITION
            return self.memory_table[pointer]

'''
with open("day7.txt", "r") as file:
    outputs = []
    memo = dict()
    perms = permutations([0,1,2,3,4])
    for perm in perms:
        gMESSAGE_QUEUE = list(perm)
        gMESSAGE_QUEUE.insert(-1, 0)
        for _ in range(5):
            phase, input_value = gMESSAGE_QUEUE[-2], gMESSAGE_QUEUE[-1]

            if (phase, input_value) in memo.keys():
                gMESSAGE_QUEUE.pop()
                gMESSAGE_QUEUE.pop()
                gMESSAGE_QUEUE.insert(-1, memo[(phase, input_value)])
            else:
                parse()
                if len(gMESSAGE_QUEUE) == 1:
                    memo[(phase, input_value)] = gMESSAGE_QUEUE[0]
                else:
                    memo[(phase, input_value)] = gMESSAGE_QUEUE[-2]

        outputs += gMESSAGE_QUEUE

    print(reduce(max, outputs, 0))
'''

'''
mailbox0 -> mailbox1 -> mailbox2 -> mailbox3 -> mailbox4 
parse() -> parse() -> parse() -> parse() -> parse()

thread(mailbox)

READ:
while (mailbox.isEmpty()):
    sleep(0.5)
mailbox.pop()

WRIT:
message = program(mailbox)
send(next_mailbox, message)

'''