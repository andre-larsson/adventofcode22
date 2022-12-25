from sympy import *

with open("data/21.txt") as f:
    lines = f.readlines()

import sys
sys.setrecursionlimit(100000)

def substitute(expression):
    if expression.isdigit():
        return expression
    elif expression in expression_dict.keys():
        return substitute(expression_dict[expression])
    elif expression == "x":
        return "x"
    else:
        expression = expression.split(" ")
        return "(" + substitute(expression[0]) + expression[1] + substitute(expression[2]) + ")"

expression_dict = dict()

for line in lines:
    line = line.strip()
    lhs_str, rhs_str = line.split(": ")
    expression_dict[lhs_str] = rhs_str

root_expression = substitute("root")
print("Part 1:", eval(root_expression))

# part 2
# replace + with = for root equation
expression_dict["root"] = expression_dict["root"].replace("+", "=")
expression_dict["humn"] = "x" # replace value of humn with x
root_expression = substitute("root")[1:-1] # remove two outer parentheses
lhs, rhs = root_expression.split("=")
lhs = parse_expr(lhs)
rhs = parse_expr(rhs)
solution = solveset(Eq(lhs, rhs)) # solve for x (only non-number in expression)
print("Part 2:", solution)
