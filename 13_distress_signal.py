# load the data
with open("data/13.txt", "r") as f:
    pairs = f.read().split("\n\n")

def is_correct_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
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

        return True
    elif isinstance(left, int) and isinstance(right, list):
        return is_correct_order([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return is_correct_order(left, [right])
    else:
        return True

correct_ids = []
for i, pair in enumerate(pairs):
    lines = pair.split("\n")
    first = eval(f"{lines[0]}")
    second = eval(f"{lines[1]}")
    print("1", first)
    print("2", second)
    if is_correct_order(first, second):
        print(f"Pair {i+1} is correct")
        correct_ids.append(i+1)

# correct answer on examplde data, but not on full input
print(sum(correct_ids))
