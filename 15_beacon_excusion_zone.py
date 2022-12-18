import numpy as np

SENSOR = 1
BEACON = 2

# load the data
with open("data/15.txt", "r") as f:
    lines = f.read().split("\n")


class CaveMap:
    def __init__(self, x_lim, y_lim):
        self.size = (y_lim[1] - y_lim[0] + 1, x_lim[1] - x_lim[0] + 1)
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.map = np.zeros(self.size, dtype=np.int8)
        self.beacon_cannot_exist = np.zeros(self.size, dtype=bool)


    def get_cell(self, x, y):
        x = x - self.x_lim[0]
        y = y - self.y_lim[0]
        return self.map[y, x]

    def set_cell(self, x, y, value):
        x = x - self.x_lim[0]
        y = y - self.y_lim[0]
        self.map[y, x] = value

    def add_no_beacon(self, x, y, value):
        x = x - self.x_lim[0]
        y = y - self.y_lim[0]

        if self.map[y, x] == BEACON: # if there is a beacon, there can be a beacon
            return

        value = self.beacon_cannot_exist[y, x] or value
        self.beacon_cannot_exist[y, x] = value

    def get_row(self, y):
        y = y - self.y_lim[0]
        return self.map[y, :], self.beacon_cannot_exist[y, :]

    def get_col(self, x):
        x = x - self.x_lim[0]
        return self.map[:, x], self.beacon_cannot_exist[:, x]

    def get_nrows(self):
        return self.size[0]

    def get_ncols(self):
        return self.size[1]

    def get_row_range(self):
        return range(self.y_lim[0], self.y_lim[1])

    def get_col_range(self):
        return range(self.x_lim[0], self.x_lim[1])


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

min_x, max_x, min_y, max_y = 0, 0, 0, 0

for line in lines:
    sensor_x, sensor_y, beacon_x, beacon_y = extract_digits(line)
    sensor_list[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
    manh_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    min_x = min(min_x, beacon_x - manh_dist, sensor_x - manh_dist)
    max_x = max(max_x, beacon_x + manh_dist, sensor_x + manh_dist)
    min_y = min(min_y, beacon_y - manh_dist, sensor_y - manh_dist)
    max_y = max(max_y, beacon_y + manh_dist, sensor_y + manh_dist)

sensor_map = CaveMap((min_x, max_x), (min_y, max_y))

for sensor, beacon in sensor_list.items():
    sensor_map.set_cell(sensor[0], sensor[1], SENSOR)
    sensor_map.set_cell(beacon[0], beacon[1], BEACON)


for sensor, beacon in sensor_list.items():
    manh_dist_beacon = abs(beacon[0]-sensor[0]) + abs(beacon[1]-sensor[1])

    # sensor_map.add_no_beacon(sensor[1], sensor[0], True)
    # sensor_map.add_no_beacon(beacon[1], beacon[0], True)

    # calculate mahattan distances from the sensor
    for y in sensor_map.get_row_range():
        for x in sensor_map.get_col_range():
            is_within = (abs(sensor[0]-x) + abs(sensor[1]-y)) <= manh_dist_beacon
            sensor_map.add_no_beacon(x, y, is_within)
    pass

print(sum(sensor_map.get_row(10)[1]))