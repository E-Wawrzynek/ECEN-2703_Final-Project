from z3 import *

number_list = [Int('n%i'%i) for i in range(0,81)]

s = Solver()
for x in number_list:
    s.add(And(x >= 1, x <= 9))

for x in range(0,9):
    row_number = [0+9*x for x in range(0,9)]

column_number = range(0,9)
square_number = [0,3,6,27,30,33,54,57,60]

rows = [[] for x in range(0,9)]
columns = [[] for y in range(0,9)]
squares = [[] for z in range(0,9)]

for x in column_number:
    for y in range(0,9):
        columns[x].append(number_list[x+9*y])

row = 0
for x in row_number:
    for y in range(0,9):
        rows[row].append(number_list[x+y])
    row += 1

square = 0
for x in square_number:
    for y in [0,9,18]:
        squares[square].append(number_list[x + y])
        squares[square].append(number_list[x + 1 + y])
        squares[square].append(number_list[x + 2 + y])
    square += 1

for x in range(0,9):
    for y in range(0,9):
        for z in range(0,9):
            if z != y:
                s.add(columns[x][z] != columns[x][y])
                s.add(rows[x][z] != rows[x][y])
                s.add(squares[x][z] != squares[x][y])

results = s.check()
if results == sat:
    print("Is satisfiable")
    m = s.model()
    for x in range(0,9):
        print(', '.join(str(m[rows[x][y]]) for y in range(0,9)))
elif results == unsat:
    print("Constraints are unsatisfiable")
else:
    print("Unable to Solve")