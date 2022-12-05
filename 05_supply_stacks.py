# read the file
import copy

with open("data/05.txt") as f:
    stack_and_moves = f.read().split("\n\n")

init_stack = stack_and_moves[0].split("\n")
move_orders = stack_and_moves[1].split("\n")

# create the initial stack
init_stack_dict = dict()
for l in init_stack[::-1]:
    # extract all numbers from the string
    numbers = [int(e) for e in l if e.isdigit()]

    if(len(numbers) > 0):
        # row describing which stack exists
        for num in numbers:
            init_stack_dict[num] = list()
        continue

    # row describing position of crates
    letters = l[1::4]
    for i, letter in enumerate(letters):
        if letter.isalpha():
            init_stack_dict[i + 1].append(letter)


# do move orders part a
stack_dict = copy.deepcopy(init_stack_dict)

for move_order in move_orders:
    num, from_id, to_id = move_order.split()[1::2]
    num, from_id, to_id = int(num), int(from_id), int(to_id)

    for i in range(num):
        stack_dict[to_id].append(stack_dict[from_id].pop())

# get top crate in each stack
result_a = "".join(stack_dict[key][-1] for key in sorted(stack_dict.keys()))
print(result_a)


# do move orders part b
stack_dict = copy.deepcopy(init_stack_dict)

for move_order in move_orders:
    num, from_id, to_id = move_order.split()[1::2]
    num, from_id, to_id = int(num), int(from_id), int(to_id)

    stack_dict[to_id] = stack_dict[to_id] + stack_dict[from_id][-num:]
    stack_dict[from_id] = stack_dict[from_id][:-num]

result_b = "".join(stack_dict[key][-1] for key in sorted(stack_dict.keys()))
print(result_b)