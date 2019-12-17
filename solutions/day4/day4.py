# secure container
import collections


def adjacent(string):
    for index in range(1, len(string)):
        if string[index - 1] == string[index]:
            return True
    return False


def increasing(string):
    for index in range(1, len(string)):
        if int(string[index - 1]) > int(string[index]):
            return False
    return True


def occurrence(password):
    most_common = collections.Counter(password).most_common()
    for frequency in most_common:
        if frequency[1] == 2:
            return True
    return False


valid_passwords = []
for number in range(264360, 746326):
    password = str(number)
    if adjacent(password) and increasing(password):
        valid_passwords.append(password)

print("Day 4 Part 1: {0}".format(len(valid_passwords)))

part2_valid_passwords = list(filter(occurrence, valid_passwords))
print("Day 4 Part 2: {0}".format(len(part2_valid_passwords)))
