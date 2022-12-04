# read the file
with open("data/04.txt") as f:
    lines = f.readlines()

# part a
# count how many times one range fully contains the other
total_sum = 0

for line in lines:
    ranges = line.split(",")
    range_a = [int(e) for e in ranges[0].split("-")]
    range_b = [int(e) for e in ranges[1].split("-")]

    # is b insida a? or a inside b?
    if (range_a[0] <= range_b[0] and range_a[1] >= range_b[1])\
            or (range_b[0] <= range_a[0] and range_b[1] >= range_a[1]):
        total_sum += 1

print(total_sum)

# part b
# count how many times one range fully contains the other
total_sum = 0

for line in lines:
    ranges = line.split(",")
    range_a = [int(e) for e in ranges[0].split("-")]
    range_b = [int(e) for e in ranges[1].split("-")]

    # note: given ranges are inclusive
    set_a = set(range(range_a[0], range_a[1] + 1))
    set_b = set(range(range_b[0], range_b[1] + 1))

    # find if there is an overlap
    if set_a.intersection(set_b):
        total_sum += 1

print(total_sum)
