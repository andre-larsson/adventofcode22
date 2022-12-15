import numpy as np

# read move instructions
with open("data/09.txt") as f:
    move_instructions = f.read().split("\n")

# parse to (direction, distance) tuples
move_instructions = [(s_move[0], int(s_move[1])) for s_move in
                     [move.split() for move in move_instructions]]

# part a
# find the maximum size of the grid we need
# worst case scenario: all moves in a direction happens consecutively
r_sum = 0
l_sum = 0
u_sum = 0
d_sum = 0

for move in move_instructions:
    if move[0] == "R":
        r_sum += move[1]
    elif move[0] == "L":
        l_sum += move[1]
    elif move[0] == "U":
        u_sum += move[1]
    elif move[0] == "D":
        d_sum += move[1]


visited_matrix = np.zeros((u_sum + d_sum+ 1, r_sum + l_sum + 1))

# begin at a position that will not fall outside the grid
# even if all moves in a direction happens at once
head_position = np.array([d_sum, l_sum])
tail_position = head_position.copy()
visited_matrix[tuple(tail_position)] = 1

def move_head(head_position, direction):
    if direction == "R":
        head_position[1] += 1
    elif direction == "L":
        head_position[1] -= 1
    elif direction == "U":
        head_position[0] += 1
    elif direction == "D":
        head_position[0] -= 1
    else:
        raise ValueError("Unknown direction")

    return head_position

def move_tail(tail_position, dist):
    v_dist, h_dist = abs(dist[0]), abs(dist[1])

    # move tail once
    if min(v_dist, h_dist) > 0 and max(v_dist, h_dist) > 1:
        tail_position += np.sign(dist)
    elif v_dist > 1:
        tail_position[0] += np.sign(dist[0])
    elif h_dist > 1:
        tail_position[1] += np.sign(dist[1])
    else:
        raise ValueError("Error: check code logic")

    return tail_position


for move in move_instructions:

    if len(move) == 0:
        # newline?
        continue

    direction, num_steps = move

    for step in range(num_steps):
        head_position = move_head(head_position, direction)

        dist = head_position - tail_position
        while (dist**2).sum()**0.5 >= 2:
            # need to move tail
            v_dist, h_dist = abs(dist[0]), abs(dist[1])

            # move tail once
            tail_position = move_tail(tail_position, dist)

            # recalculate distance
            dist = head_position - tail_position

            # update visited matrix
            visited_matrix[tuple(tail_position)] = 1

print(visited_matrix.shape)
print(int(visited_matrix.sum()))


# part b

# begin at a position that will not fall outside the grid
# even if all moves in a direction happens at once
visited_matrix = np.zeros((u_sum + d_sum+ 1, r_sum + l_sum + 1))

# our rope is now a 2D matrix where each row is a knot (top row is head)
knot_positions = np.full((10,2), fill_value=[d_sum, l_sum])


# for mapping numbers to characters for printing
num_to_char_map = {x : str(x) for x in range(10)}
num_to_char_map[0] = "H"
num_to_char_map[-1] = "-"

def print_visited_matrix(matrix):
    for row in matrix[::-1]:
        chars = ["-" if x==0 else "#" for x in row ]
        print("".join(chars))

def print_snake(snake, m):
    m = np.full_like(m, -1)
    for i in range(snake.shape[0]):
        m[tuple(snake[i])] = i

    for row in m[::-1]:
        chars = [num_to_char_map[int(x)] for x in row]
        print("".join(chars))


visited_matrix[tuple(knot_positions[0])] = 1
for move in move_instructions:

    if len(move) == 0:
        # newline?
        continue

    direction, num_steps = move

    for step in range(num_steps):
        # move head
        knot_positions[0] = move_head(knot_positions[0], direction)

        for i in range(knot_positions.shape[0]-1):
            dist = knot_positions[i] - knot_positions[i+1]
            while (dist**2).sum()**0.5 >= 2:
                # need to move tail
                knot_positions[i+1] = move_tail(knot_positions[i+1], dist)

                # recalculate distance
                dist = knot_positions[i] - knot_positions[i+1]
            # only update visited matrix on last move
            if i == knot_positions.shape[0]-2:
                visited_matrix[tuple(knot_positions[-1])] = 1
    # print(knot_positions)
    # print_snake(knot_positions, visited_matrix)


# print_matrix(visited_matrix)
print(int(visited_matrix.sum()))