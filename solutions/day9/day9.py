import vm
from pipes import Pipe

p = vm.Parser('day9.txt')
program = p.parse()
pipe = Pipe()

m1 = vm.Machine(program.copy(), pipe, pipe, [1])
m2 = vm.Machine(program.copy(), pipe, pipe, [2])
m1.execute()
print("Day 9 part 1:", pipe.inspect())
m2.execute()
print("Day 9 part 2:", pipe.inspect())