import vm
from pipes import Pipe

p = vm.Parser('day9.txt')

pipe = Pipe()
m = vm.Machine(p.parse(), pipe, pipe, [2])
m.execute()