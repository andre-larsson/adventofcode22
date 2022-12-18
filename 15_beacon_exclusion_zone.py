# load the data
with open("data/15.txt", "r") as f:
    lines = f.read().split("\n")


def extract_digits(string):
    digits = []
    current_digit = ""
    for c in string:
        if c.isdigit() or c == "-":
            current_digit += c
        elif current_digit != "":
            digits.append(int(current_digit))
            current_digit = ""
        else:
            current_digit = ""

    if current_digit != "":
        digits.append(int(current_digit))

    return digits


sensor_list = dict()
for line in lines:
    sensor_x, sensor_y, beacon_x, beacon_y = extract_digits(line)
    manh_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    sensor_list[(sensor_x, sensor_y)] = (beacon_x, beacon_y, manh_dist)

row_i = 2000000
blocked_positions = set()
for sensor, beacon in sensor_list.items():
    beacon_x, beacon_y, manh_dist = beacon
    sensor_x, sensor_y = sensor

    y_dist = abs(row_i - sensor[1])

    if y_dist < manh_dist:
        x_low = sensor_x - (manh_dist - y_dist)
        x_high = sensor_x + (manh_dist - y_dist)
        for x in range(x_low, x_high+1):
            if (x, row_i) != (beacon_x, beacon_y):
                blocked_positions.add(x)

    print(sensor, "Done!")

print(len(blocked_positions))
