from pipes import Pipe
from functools import reduce
from itertools import permutations
import vm, threading


def amplifier(in_pipe, out_pipe, args):
    vm.Parser(file, vm.Machine(in_pipe, out_pipe, args)).parse()


file = 'day7.txt'
outputs = []
perms = permutations([0, 1, 2, 3, 4])
pipes = [Pipe() for _ in range(5)]
for perm in perms:
    vm.Parser(file, vm.Machine(pipes[0], pipes[1], [0, perm[0]])).parse()
    vm.Parser(file, vm.Machine(pipes[1], pipes[2], [perm[1]])).parse()
    vm.Parser(file, vm.Machine(pipes[2], pipes[3], [perm[2]])).parse()
    vm.Parser(file, vm.Machine(pipes[3], pipes[4], [perm[3]])).parse()
    vm.Parser(file, vm.Machine(pipes[4], pipes[0], [perm[4]])).parse()
    outputs.append(pipes[0].get_input())

print("Day 7 Part 1: ", reduce(max, outputs, 0))

perms = permutations([5, 6, 7, 8, 9])
outputs = []
for perm in perms:
    a0 = threading.Thread(target=amplifier, args=(pipes[0], pipes[1], [0, perm[0]],))
    threads = [a0]
    for index in range(1, 5):
        threads.append(
            threading.Thread(
                target=amplifier, args=(pipes[index], pipes[(index + 1) % 5], [perm[index]],)
            )
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    outputs.append(pipes[0].get_input())

print("Day 7 Part 2: ", reduce(max, outputs, 0))
