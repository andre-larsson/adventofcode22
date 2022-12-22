from collections import defaultdict

import numpy as np


with open("data/17.txt") as f:
    data = f.read()

direction_dict = {"<": -1, ">":1}
jet_streams = [direction_dict[x] for x in data]

# define the tower / grid
class Tower:
    def __init__(self):
        self.tower = defaultdict(lambda: False)
        self.width = 7

    @property
    def highest_rock(self):
        if len(self.tower) == 0:
            return 0
        else:
            return max([x[1] for x in self.tower.keys() if self.tower[x]])


    def detect_collision(self, blocks):
        collision = [self.detect_overlap(x) for x in blocks]
        return any(collision)


    def detect_overlap(self, block):
        return self.tower[tuple(block)] or block[0] < 0 or block[0] >= self.width or block[1] < 0

    def add_shape(self, shape):
        for x in shape.blocks:
            self.tower[tuple(x)] = True


# define the shapes

class ShapeBaseClass():
    def __init__(self, blocks):
        self.blocks = blocks

    @property
    def top_edge(self):
        return np.max(self.blocks[:,1])

    def push_horizontally(self, direction, tower):
        self.blocks[:,0] += direction

        if tower.detect_collision(self.blocks):
            self.blocks[:,0] -= direction
            return False
        else:
            return True

    def move_down(self, tower):
        self.blocks[:,1] = self.blocks[:,1] - 1

        if tower.detect_collision(self.blocks):
            self.blocks[:,1] += 1
            return False
        else:
            return True

    def __repr__(self):
        block_str = ", ".join([str(x) for x in self.blocks])
        return f"Shape: ({block_str})"


# -
class Shape1(ShapeBaseClass):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                 [left_edge+1, bottom_edge],
                                 [left_edge+2, bottom_edge],
                                 [left_edge+3, bottom_edge]]))
# +
class Shape2(ShapeBaseClass):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge+1],
                                   [left_edge+1, bottom_edge],
                                   [left_edge+1, bottom_edge+1],
                                   [left_edge+1, bottom_edge+2],
                                   [left_edge+2, bottom_edge+1]]))

# mirrored L
class Shape3(ShapeBaseClass):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                   [left_edge+1, bottom_edge],
                                   [left_edge+2, bottom_edge],
                                   [left_edge+2, bottom_edge+1],
                                   [left_edge+2, bottom_edge+2]]))
# I
class Shape4(ShapeBaseClass):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                   [left_edge, bottom_edge+1],
                                   [left_edge, bottom_edge+2],
                                   [left_edge, bottom_edge+3]]))
# cube
class Shape5(ShapeBaseClass):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                   [left_edge, bottom_edge+1],
                                   [left_edge+1, bottom_edge],
                                   [left_edge+1, bottom_edge+1]]))

# part a, simulate the falling rocks

def simulate_n_rocks(n):

    shape_classes = [Shape1, Shape2, Shape3, Shape4, Shape5]

    tower = Tower()
    index = 0
    num_stopped = 0
    highest_rock = -1
    heights = []

    while True:
        shape_class = shape_classes[num_stopped % len(shape_classes)]
        shape_stopped = False
        shape = shape_class(2, highest_rock+3+1)
        while not shape_stopped:
            shape.push_horizontally(jet_streams[index], tower)
            shape_stopped = not shape.move_down(tower)
            if shape_stopped:
                tower.add_shape(shape)
            index = (index + 1) % len(jet_streams) # cycle through jet streams


        highest_rock = max(highest_rock, shape.top_edge)
        heights.append(highest_rock)
        num_stopped += 1

        if num_stopped >= n:
            break
    return highest_rock, np.array(heights)

answer_a, _ = simulate_n_rocks(2022)

print(f"Part a: {answer_a+1}")

# part b
# simulation will at some point repeat
# try to find a pattern in subsequent height increases

def find_pattern(x):
    auto_corr = np.correlate(x, x, mode="full")[-len(x):]
    trend = auto_corr[1:] - auto_corr[:-1] # to find the peaks
    sorted_i = np.argsort(trend) # will be sorted from low to high
    period = sorted_i[-2] - sorted_i[-1] # index of second peak minus first peak
    return sorted_i[-1], period  # start_pos, period

_, heights = simulate_n_rocks(10_000)

print("Second simulation done.")

height_increases = heights[1:] - heights[:-1]
ps, pp = find_pattern(height_increases) # pattern_start, pattern_period

print(f"Found pattern with start: {ps}, period: {pp}")

pattern = height_increases[ps:ps + pp]

# verify that the pattern is correct
period = 0
while period < ((len(height_increases) - ps) // len(pattern)):
    one_repeat = np.all(height_increases[ps + pp * period:ps + pp * (period + 1)] == pattern)
    period += 1
    print(f"Period {period} matches found pattern: {one_repeat}")

num_rocks_b = 1000000000000
# initial_part --- pattern repeats --- end_part

num_periods_b = (num_rocks_b - ps) // pp

initial_sum = np.sum(height_increases[:ps])
pattern_sum = np.sum(pattern) * num_periods_b
end_num_rocks = num_rocks_b - ps - pp * num_periods_b
end_sum = np.sum(pattern[:end_num_rocks])

total_sum = initial_sum + pattern_sum + end_sum

print(f"Part b: {total_sum}")