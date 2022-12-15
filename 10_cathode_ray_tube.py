# load the data
with open("data/10.txt") as f:
    cpu_instructions = f.read().split("\n")

cycle, X_value = 0, 1
sprite_positions = [X_value]  # for part a + b
for instruction in cpu_instructions:
    if instruction == "noop":
        add_num = 0
        cycle += 1
        sprite_positions.append(X_value)
        pass
    else:
        add_num = int(instruction.split()[1])
        cycle += 2
        sprite_positions.append(X_value)
        sprite_positions.append(X_value)

    X_value += add_num


# part a
# calculate signal strength
signals = [e*i for i, e  in enumerate(sprite_positions) if (i+20) % 40 == 0 and i != 0]

print("Part a:", sum(signals))

# part b
# draw the screen
x_pos = 0
display_str = ""
for cycle, X_value in enumerate(sprite_positions[1:]): # skip first value (cycle 0 not drawn)

    x_pos = cycle % 40  # current x_pos being drawn

    if abs(X_value-x_pos) < 2:
        display_str += "#"
    else:
        display_str += "."

    if cycle % 40 == 39:
        display_str += "\n"


print(display_str)