import math

"""
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

"""
parse -> rule [ '\n' rule]
rule  -> LHS '=>' RHS
LHS   -> atom [', ' atom]
RHS   -> ' ' atom
atom  -> quantity ' ' kind
"""


class Rule:
    def __init__(self, lhs, rhs):
        self.right_side = rhs
        self.left_side = lhs

    def __repr__(self):
        return "{0} => {1}".format(self.left_side, self.right_side)


class Atom:
    def __init__(self, amount, atom_kind):
        self.quantity = amount
        self.kind = atom_kind

    def __repr__(self):
        return "{0} {1}".format(self.quantity, self.kind)


def get_char(file):
    char = file.read(1)

    return char


def peek_char(file):
    pos = file.tell()
    char = file.read(1)
    file.seek(pos)

    return char


def parse(file_name):
    pos = 0
    rules = []
    with open(file_name, 'r') as file:
        rules.append(rule(file))
        while get_char(file) == '\n':
            rules.append(rule(file))

    return rules


def rule(file):
    lhs = left_hand_side(file)
    get_char(file)
    get_char(file)
    get_char(file)
    rhs = right_hand_side(file)
    return Rule(lhs, rhs)


def left_hand_side(file):
    lhs = [atom(file)]
    while get_char(file) == ',':
        get_char(file)
        lhs.append(atom(file))
    return lhs


def right_hand_side(file):
    return atom(file)


def atom(file):
    """
    atom  -> quantity ' ' kind
    """
    value = quantity(file)
    get_char(file)
    return Atom(value, kind(file))


def quantity(file):
    num = ''
    value = peek_char(file)
    ord_value = ord(value)
    while 48 <= ord_value <= 57:
        num += get_char(file)
        ord_value = ord(peek_char(file))

    return int(num)


def kind(file):
    name = ''
    value = peek_char(file)
    ord_value = ord(value)
    while 65 <= ord_value <= 90:
        name += get_char(file)
        c = peek_char(file)

        if c == '':
            break

        ord_value = ord(c)

    return name


def find(chemical, reactions):
    return list(filter(lambda x: x.right_side.kind == chemical.kind, reactions))


def need(chemical, reactions, budget, amount_needed):
    if chemical.kind == 'ORE':
        return

    reaction = find(chemical, reactions)

    if not reaction:
        raise ValueError("ERR! No reactions with reactant{0}!!!".format(chemical))

    reactants, product = reaction[0].left_side, reaction[0].right_side

    if amount_needed - budget[product.kind] >= product.quantity:
        production = math.ceil((amount_needed - budget[product.kind]) / product.quantity)
    else:
        production = 1

    budget[product.kind] += product.quantity * production

    for reactant in reactants:
        # print('Have for {0}: {1}'.format(reactant, budget[reactant.kind]))
        # print('Need for {0}: {1}'.format(reactant, reactant.quantity))
        if budget[reactant.kind] >= production * reactant.quantity:
            budget[reactant.kind] -= production * reactant.quantity
        else:
            need(reactant, reactions, budget, production * reactant.quantity)
            budget[reactant.kind] -= production * reactant.quantity

    return


all_reactions = parse('day14.txt')
chemicals = dict()
for react in all_reactions:
    for chemical in react.left_side:
        chemicals[chemical.kind] = 0

chemicals['FUEL'] = 0

copy = chemicals.copy()

end = list(filter(lambda x: x.right_side.kind == 'FUEL', all_reactions))[0]
need(end.right_side, all_reactions, chemicals, 1)
print("Day 14 Part 1: {0}".format(abs(chemicals['ORE'])))

trillion = 1000000000000
rule_end = Rule([Atom(1, 'FUEL')], Atom(1, 'END'))
all_reactions.append(rule_end)
copy['END'] = 0

fuel_copy = copy.copy()


low, high = 0, trillion
old_mid = -1
while low <= high:
    mid = (low + high) // 2
    rule_end.left_side[0].quantity = mid
    need(rule_end.right_side, all_reactions, fuel_copy, 1)
    if abs(fuel_copy['ORE']) > trillion:
        high = mid + 1
    elif abs(fuel_copy['ORE']) < trillion:
        low = mid - 1
    if mid == old_mid:
        break
    old_mid = mid
    fuel_copy = copy.copy()

print("Day 14 Part 2: {0}".format(mid))