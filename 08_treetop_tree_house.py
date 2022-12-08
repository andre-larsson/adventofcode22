import numpy as np

with open("data/08.txt") as f:
    lines = f.read().splitlines()

tree_map = np.array([list(line) for line in lines]).astype(int)

# part a
num_visible = (tree_map.shape[0] - 1)*4
for row_i in range(1, tree_map.shape[0] - 1):
    for col_i in range(1, tree_map.shape[1] - 1):
        tree_height = tree_map[row_i, col_i]

        if (np.max(tree_map[0:row_i, col_i]) < tree_height) or \
            np.max(tree_map[row_i+1:, col_i]) < tree_height or \
            np.max(tree_map[row_i, 0:col_i]) < tree_height or \
            np.max(tree_map[row_i, col_i+1:]) < tree_height:
            num_visible += 1

print(num_visible)

# part b

high_score = 0

for row_i in range(1, tree_map.shape[0]-1):
    for col_i in range(1, tree_map.shape[1]-1):
        tree_height = tree_map[row_i, col_i]

        # up
        i = 0
        while row_i-i > 0 and (i==0 or tree_map[row_i-i, col_i] < tree_height):
            i += 1

        # down
        j = 0
        while row_i+j < tree_map.shape[0]-1 and (j==0 or tree_map[row_i+j, col_i] < tree_height):
            j += 1

        # left
        k = 0
        while col_i-k > 0 and (k==0 or tree_map[row_i, col_i-k] < tree_height):
            k += 1

        # right
        l = 0
        while col_i+l < tree_map.shape[1]-1 and (l==0 or tree_map[row_i, col_i+l] < tree_height):
            l += 1
        high_score = max(high_score, i*j*k*l)

print(high_score)