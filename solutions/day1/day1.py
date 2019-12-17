from functools import reduce

modules = []
fuel_history = dict()
total = 0


def calculate_fuel(weight, history):
    if weight <= 0:
        return 0
    if weight in history.keys():
        return history[weight]
    else:
        fuel = ((weight // 3) - 2)

        if fuel <= 0:
            fuel = 0
            history[weight] = fuel
        else:
            history[weight] = fuel + calculate_fuel(fuel, history)

        return history[weight]


with open('day1.txt') as f:
    for line in f:
        total += calculate_fuel(int(line), fuel_history)

    print(total)
    # print(reduce(lambda x, y : x + ((abs(y) // 3) - 2), modules, 0))
