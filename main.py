from itertools import chain, combinations, product, permutations
from queue import Queue

# Rules
# 24 number cards in total. 20 "small" between 1 and 10 (2 of each) and 4 "large" 25, 50, 75, 100.
# 6 numbers must be chosen at random using # small and # large
# Aim of the game is to get to the target number (3 digit number between 100 and 999) using the available numbers in as few moves as possible.
# Only the 4 elementary mathematical operators are allowed ( + - * / )
# All operations must result in integers

## Helper functions

def multiply(x, y):
    """
    Multiply x with y.
    """
    result = x * y
    if result > 999:
        return -1
    return result

def divide(x, y):
    """
    Divide x by y
    """
    result = x / float(y)
    if not result.is_integer():
        return -1
    return int(result)

def add(x, y):
    """
    Add y to x
    """
    result = x + y
    if result > 999:
        return -1
    return result

def subtract(x, y):
    """
    Subtract y from x
    """
    result = x - y
    if result < 0:
        return -1
    return result

## End helper functions

def solve(source, target):
    """
    Solve the problem of creating target number from array of source numbers
    """
    solutions = []
    queue = Queue()
    combinations = get_all_combinations(source)

    push_values_to_queue(queue, combinations)

    while not queue.empty():
        unsolved, solved = get_operations(queue.get(), target)
        push_values_to_queue(queue, unsolved)
        solutions.extend(solved)

    print(len(solutions))

    matches = [i for i in solutions if i == target]
    print('Found %d matches.' % len(matches))


def push_values_to_queue(queue, values):
    """
    Put a list of values onto the queue
    """
    [queue.put(value) for value in values]

def get_all_combinations(source):
    """
    Get all possible combinations and permutations of a source array of numbers.
    """
    combs = []
    perms = []
    for L in product((combinations(source, i) for i in range(1, len(source) + 1))):
        combs.extend(list(c) for c in chain.from_iterable(L))

    for combination in combs:
        perms.extend(list(p) for p in permutations(combination))

    return perms

def get_operations(combination, target):
    """
    Magic.
    """
    if len(combination) == 1:
        return [], combination
    if target in combination:
        return [], [combination[0]]

    x = combination.pop()
    y = combination.pop()

    operation_results = [
        add(x, y),
        subtract(x, y),
        multiply(x, y),
        divide(x, y)
    ]

    operation_results = [op for op in operation_results if op > 0 and op < 1000]

    unsolved_combinations = [[i] + combination for i in operation_results if len([i] + combination) > 1]
    solved_combinations = [([i] + combination)[0] for i in operation_results if len([i] + combination) == 1]

    return unsolved_combinations, solved_combinations

if __name__ == "__main__":
    chosen_numbers = [10, 10, 1]
    target = 100
    solve(chosen_numbers, target)
