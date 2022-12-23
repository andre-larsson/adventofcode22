from copy import deepcopy

with open("data/20.txt") as f:
    lines = f.readlines()

numbers = [(i, int(x)) for i, x in enumerate(lines)]


def find_pos_by_i(numbers, num_i):
    for j in range(len(numbers)):
        if numbers[j][0] == num_i:
            return j

def find_pos_by_value(numbers, value):
    for j in range(len(numbers)):
        if numbers[j][1] == value:
            return j

def mix_numbers(numbers):

    new_numbers = deepcopy(numbers)
    n_num = len(numbers)

    for i in range(n_num):
        # find the number to move in new_numbers
        num_i = find_pos_by_i(new_numbers, i)

        # remove from new_numbers
        this_num = new_numbers.pop(num_i)
        new_index = (num_i + this_num[1]) % (n_num-1)
        new_numbers.insert(new_index, this_num)

    return new_numbers


def mix_numbers_n(numbers, n, multiplier):
    numbers = [(i, n * multiplier) for i, n in numbers]
    for _ in range(n):
        numbers = mix_numbers(numbers)
    return numbers

def get_coords(numbers):
    zero_index = find_pos_by_value(numbers, 0)
    # 1000th number is number with index 999 etc...
    coords = [numbers[(e*1000 + zero_index) % len(numbers)][1] for e in range(1, 4)]
    print(coords)
    return coords


answer_a = sum(get_coords(mix_numbers(numbers)))

print(f"Answer a: {answer_a}")


numbers_b = mix_numbers_n(numbers, 10, 811589153)

answer_b = sum(get_coords(numbers_b))
print(f"Answer b: {answer_b}")