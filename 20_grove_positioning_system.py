import numpy as np

with open("data/20.txt") as f:
    lines = f.readlines()

numbers = np.array([int(x) for x in lines])

def mix_numbers(numbers):
    numbers = np.array(numbers)
    movement = np.array(numbers)
    n_num = len(numbers)

    for i, move in enumerate(movement):

        if move == 0:
            continue

        if len(np.where(numbers == move)) == 0:
            pass

        current_index = np.where(numbers == move)[0][0]

        # move position of this number
        new_index = current_index + move

        if new_index > 0:
            num_wrap_arounds = abs(new_index // (n_num-1))  # (n_num-1) since we get free move when reaching border
        else:
            num_wrap_arounds = (abs(new_index) // (n_num-1)) + 1

        # calc position of new index
        if move > 0:
            new_index = ((new_index % n_num) + num_wrap_arounds) % (n_num)
        else:
            new_index = ((new_index % n_num) - num_wrap_arounds) % (n_num)


        if move > 0:
            if num_wrap_arounds:
                numbers[new_index+1:current_index+1] = numbers[new_index:current_index]
            else:
                # get indices to the right
                numbers[current_index:new_index] = numbers[current_index+1:new_index+1]
        if move < 0:
            if num_wrap_arounds:
                numbers[current_index:new_index] = numbers[current_index+1:new_index+1]

            else:
                # get indices to the left
                numbers[current_index:new_index] = numbers[current_index+1:new_index+1]

        numbers[new_index] = move

        pass

    return numbers

def get_coords(numbers):
    zero_index = np.where(numbers == 0)[0][0]
    # 1000th number is number with index 999 etc...
    coords = [(e*1000 + zero_index-1) % len(numbers) for e in range(3)]
    return numbers[coords]

numbers = mix_numbers(numbers)


print(numbers)
print(get_coords(numbers))