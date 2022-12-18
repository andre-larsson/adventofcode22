# load the data
from collections import defaultdict
from time import perf_counter

from joblib import Parallel, delayed

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

print("Part a")

sensor_list = dict()
for line in lines:
    sensor_x, sensor_y, beacon_x, beacon_y = extract_digits(line)
    manh_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    sensor_list[(sensor_x, sensor_y)] = (beacon_x, beacon_y, manh_dist)

# part a
row_i = 10
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

# part b

print("Part b")

# Task: find the only pixel that is not blocked/scanned in a 4000000x4000000 grid
#
# since it is the only one not blocked, it must be surrounded by blocked (scanned) pixels.
# turns out we need to look for pixels that are on the perimeters of the sensors,
# and find the one found on most perimeters. I looked on the internet about info
# for this one (did not copy any code)... not 100.0 % sure of this solution, but
# found the correct answer for both the example and full input data, not sure how
# you would solve it otherwise.

def get_perimeter(sensor, dist):
    sensor_x, sensor_y = sensor
    perimeter = set()

    for x_dist in range(dist+2):
        y_dist = dist - x_dist
        perimeter.add((sensor_x + x_dist, sensor_y + y_dist+1))
        perimeter.add((sensor_x + x_dist, sensor_y - y_dist-1))
        perimeter.add((sensor_x - x_dist, sensor_y + y_dist+1))
        perimeter.add((sensor_x - x_dist, sensor_y - y_dist-1))
    return perimeter

def is_inside(pixel):
    x, y = pixel
    return x >= 0 and x <= 4000000 and y >= 0 and y <= 4000000


def find_perimeter_pixels(sensor_list):
    perimeter_dict = defaultdict(int)

    def worker(sensor, beacon):
        beacon_x, beacon_y, manh_dist = beacon
        perimeter = get_perimeter(sensor, manh_dist)
        perimeter.discard((beacon_x, beacon_y))
        return perimeter

    num_cores = min(len(sensor_list), 16)
    print("Collecting perimeter points using {} cores".format(num_cores))
    result =Parallel(n_jobs=num_cores)(delayed(worker)(sensor, beacon) for sensor, beacon in sensor_list.items())
    print("Merging results...")

    for perimeter in result:
        for pixel in perimeter:
            perimeter_dict[pixel] += 1

    return perimeter_dict

t0 = perf_counter()
perimeter_dict = find_perimeter_pixels(sensor_list)

print("Searching for the pixel found on most perimeters...")
max_count = 0
max_pixel = None

for pixel, count in perimeter_dict.items():
    if count > max_count and is_inside(pixel):
        max_count = count
        max_pixel = pixel

print(f"Found it! {max_pixel} on {max_count} perimeters")

print("Tuning frequency:", max_pixel[0] * 4000000 + max_pixel[1])

print("Time taken (part b):", perf_counter() - t0)