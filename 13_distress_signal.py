import functools

# load the data
with open("data/13.txt", "r") as f:
    pairs = f.read().split("\n\n")

def is_correct_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None  # equal, continue comparing
        else:
            return left < right
    elif isinstance(left, list) and isinstance(right, list):

        for i in range(len(left)):
            if i >= len(right):
                return False
            result = is_correct_order(left[i], right[i])
            if result is None:
                continue
            else:
                return result

        if len(left) == len(right):
            return None  # equal, continue comparing
        return True
    elif isinstance(left, int) and isinstance(right, list):
        return is_correct_order([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return is_correct_order(left, [right])
    else:
        return True

# part a
packets = []
correct_ids = []
for i, pair in enumerate(pairs):
    lines = pair.split("\n")
    first = eval(f"{lines[0]}")
    second = eval(f"{lines[1]}")
    packets.append(first)
    packets.append(second)
    if is_correct_order(first, second):
        correct_ids.append(i+1)

print(sum(correct_ids))

# part b

def cmp_function(left, right):
    answer = is_correct_order(left, right)
    if answer is None:
        return 0
    elif answer:
        return -1
    else:
        return 1

packets.append([[2]])
packets.append([[6]])
sorted_packets = sorted(packets, key=functools.cmp_to_key(cmp_function))

decoder_key = (sorted_packets.index([[2]])+1)*(sorted_packets.index([[6]])+1)

print(decoder_key)