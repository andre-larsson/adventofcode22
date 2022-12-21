from collections import defaultdict
from time import perf_counter

import numpy as np


with open("data/17.txt") as f:
    data = f.read()

direction_dict = {"<": -1, ">":1}
jet_streams = [direction_dict[x] for x in data]


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

    @property
    def highest_floor(self):
        for y in range(self.highest_rock, 0, -1):
            if all(self.tower[(x,y)] for x in range(self.width)):
                return y
        return 0

    def detect_collision(self, blocks):
        collision = [self.detect_overlap(x) for x in blocks]
        return any(collision)


    def detect_overlap(self, block):
        return self.tower[tuple(block)] or block[0] < 0 or block[0] >= self.width or block[1] < 0

    def add_shape(self, shape):
        for x in shape.blocks:
            self.tower[tuple(x)] = True


class ShapeC():
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
class Shape1(ShapeC):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                 [left_edge+1, bottom_edge],
                                 [left_edge+2, bottom_edge],
                                 [left_edge+3, bottom_edge]]))
# +
class Shape2(ShapeC):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge+1],
                                   [left_edge+1, bottom_edge],
                                   [left_edge+1, bottom_edge+1],
                                   [left_edge+1, bottom_edge+2],
                                   [left_edge+2, bottom_edge+1]]))

# mirrored L
class Shape3(ShapeC):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                   [left_edge+1, bottom_edge],
                                   [left_edge+2, bottom_edge],
                                   [left_edge+2, bottom_edge+1],
                                   [left_edge+2, bottom_edge+2]]))
# I
class Shape4(ShapeC):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                   [left_edge, bottom_edge+1],
                                   [left_edge, bottom_edge+2],
                                   [left_edge, bottom_edge+3]]))
# cube
class Shape5(ShapeC):
    def __init__(self, left_edge, bottom_edge):
        super().__init__(np.array([[left_edge, bottom_edge],
                                   [left_edge, bottom_edge+1],
                                   [left_edge+1, bottom_edge],
                                   [left_edge+1, bottom_edge+1]]))


shape_classes = [Shape1, Shape2, Shape3, Shape4, Shape5]

tower = Tower()
index = 0
num_stopped = 0
highest_rock = -1

t0 = perf_counter()
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
    num_stopped += 1
    if num_stopped % 10_000 == 0:
        print(num_stopped, highest_rock)

    if num_stopped >= 10_000:
        break

ratio = 1_000_000_000_000/10_000
print(f"Estimated run time: {(perf_counter() - t0)*ratio/3600:.2f} h") # Estimated run time: 51786.14 h
print(num_stopped, tower.highest_rock+1)