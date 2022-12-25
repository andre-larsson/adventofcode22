with open("data/25.txt") as f:
    lines = f.readlines()


symbols_dict = {"2" : 2,
                "1" : 1,
                "0" : 0,
                "-" : -1,
                "=" : -2,}

# reverse symbols dict
rsymbols_dict = {2 : "2",
            1 : "1",
            0 : "0",
            -1 : "-",
            -2 : "=",}

# parse numbers and convert from snafu to decimal
numbers = list()
for line in lines:
    number = sum([symbols_dict[x]*5**i for i, x in enumerate(line[::-1].strip())])
    numbers.append(number)
    # print(f"{line.strip()} = {number}")

print(f"Sum: {sum(numbers)}")


def convert_to_snafu(num_to_convert):
    new_num = list()
    base = 5
    i = 0
    while num_to_convert>0:
        divisor = base**i
        term = (num_to_convert // divisor) % 5
        if term >2 :
            term = term - 5

        new_num.append(rsymbols_dict[term])

        num_to_convert -= term*base**i
        i += 1

    return "".join(new_num[::-1])


print("Answer first part:", convert_to_snafu(sum(numbers)))



