class Monkey:

    def __init__(self, id, items=None, operation=None, action=None):
        self.id = id
        self.items = items
        self.operation = operation
        self.action = action
        self.num_inspected = 0

    def inspect(self, part_a=True):
        action_list = []
        for item in self.items:
            item = self.operation(item)
            item = item // 3 if part_a else item % 9699690  # 9699690 is the product of all primes up to 20
            action_list.append([item, self.action(item)])

        self.num_inspected += len(self.items)
        self.items = []
        return action_list

    def add_items(self, items):
        if isinstance(items, list):
            self.items.extend(items)
        else:
            self.items.append(items)
        return

    def __str__(self):
        return f"Monkey {self.id} has items {self.items} and has inspected {self.num_inspected} items"


with open("data/11.txt") as f:
    data = f.read().split("\n\n")


def create_throw_action(div_num, true_action, false_action):
    def throw_action(num):
        if num % div_num == 0:
            return true_action
        else:
            return false_action
    return throw_action

def create_operation(operation_str):
    return lambda old : eval(operation_str)

def initialise_monkeys(data):
    monkeys = []
    for data in data:
        monkey_id, items = (None, None)
        div_num, true_action, false_action = (1, 0, 0)
        operation_str = ""
        for row in data.split("\n"):
            if row.startswith("Monkey"):
                monkey_id = row.split(" ")[1]
            elif "Starting items:" in row:
                items = row.split(":")[1].split(",")
                items = [int(item) for item in items]
            elif "Operation:" in row:
                operation_str = row.split("= ")[1]
            elif "Test:" in row:
                div_num = int(row.split(":")[1].split(" ")[-1])
            elif "If true:" in row:
                true_action = int(row.split(":")[1].split(" ")[-1])
            elif "If false:" in row:
                false_action = int(row.split(":")[1].split(" ")[-1])


        action = create_throw_action(div_num, true_action, false_action)
        operation = create_operation(operation_str)

        monkey = Monkey(monkey_id, items, operation, action)
        monkeys.append(monkey)
    return monkeys

def simulate_monkey_business(monkeys, num_rounds, part_a=True, verbose=False):
    for i in range(num_rounds):
        for monkey in monkeys:
            if verbose:
                print(monkey)
            for item, mid in monkey.inspect(part_a):
                if verbose:
                    print(f"Item {item} was thrown to Monkey {mid}")
                monkeys[mid].add_items(item)
    num_inspected = sorted([monkey.num_inspected for monkey in monkeys])
    level = num_inspected[-1] * num_inspected[-2]

    return monkeys, level

# part a
init_monkeys = initialise_monkeys(data)
monkeys, level = simulate_monkey_business(init_monkeys, 20, True)
for monkey in monkeys:
    print(monkey)
print(level)

print("---------------------")

# part b
monkeys, level = simulate_monkey_business(init_monkeys, 10000, False)
for monkey in monkeys:
    print(monkey)
print(level)