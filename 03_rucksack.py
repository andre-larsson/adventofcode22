import string
import pandas as pd

# dict for mapping letters to priorities
ascii_table = {e: i+1 for i, e in enumerate(string.ascii_letters)}

def rucksack_to_priority(rucksack):
    # split into two equally sized char lists
    rucksack = list(rucksack)

    n_char = len(rucksack)
    part_a = rucksack[0:int(n_char/2)]
    part_b = rucksack[int(n_char/2):]

    # find overlap
    part_a = set(part_a)
    part_b = set(part_b)
    overlap = part_a.intersection(part_b).pop()

    # calc priority
    priority = ascii_table[overlap]
    return priority

# read data
rucksack_data = pd.read_csv("data/03.txt", header=None)

# 3a
print(rucksack_data.apply(lambda x: rucksack_to_priority(x.iloc[0]), axis=1).sum())

# 3b
n_groups = rucksack_data.shape[0]//3
prio_sum = 0
for i in range(n_groups):
    # rucksacks for group i
    group = rucksack_data.iloc[i*3:(i+1)*3, 0].values
    # find unique chars in each rucksack
    item_types = [set(rucksack) for rucksack in group]
    # find overlap between rucksack item types and calc priority
    overlap = set.intersection(*item_types).pop()
    prio_sum += ascii_table[overlap]

print(prio_sum)