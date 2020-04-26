import argparse
from z3 import *
import random as rd
import itertools

def generate_board():
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
        board = [ [ m.evaluate(rows[i][j]) for j in range(9) ] for i in range(9) ]
    elif results == unsat:
        print("Constraints are unsatisfiable")
    else:
        print("Unable to Solve")
    return board

def solve_sudoku(grid):
    s = Solver()

    solve_grid = []
    solve_grid = [[Int('v%i%i' % (j, k)) for k in range(1,10)] for j in range(1,10)]

    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                s.add(solve_grid[r][c] == grid[r][c])

    for r in range(9):
        for c in range(9):
            s.add(And(1 <= solve_grid[r][c], solve_grid[r][c] <= 9))
    
    for r in range(9):
        s.add(Distinct(solve_grid[r]))
    
    for c in range(9):
        s.add(Distinct([solve_grid[r][c] for r in range(9)]))

    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            s.add(Distinct([solve_grid[j][k] for j, k in itertools.product(range(3), range(3))]))

    cntr = 0
    while s.check() == sat:
        cntr += 1
        m = s.model()
        for j in range(9):
            for k in range(9):
                s.add(Not(And(solve_grid[j][k] == m[solve_grid[j][k]])))
    return cntr


# command line input from player
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sudoku board generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--difficulty', help='level of board difficulty (1, 2, or 3)',
                        default=1, type=int)
    args = parser.parse_args()

# how many numbers removed for level of difficulty (might ammend later)
level = args.difficulty
if level == 0:
    num_remove = 0
if level == 1:
    num_remove = 9
if level == 2:
    num_remove = 18
if level == 3:
    num_remove = 27

# make the numbers 0-9 ints
n = [Int('i') for i in range(10)]
# seed for random number generator
rd.seed(None)

grid = generate_board()
#print(grid)

#for j in range(9):
#    for k in range(9):
#        grid[j][k] = int(grid[j][k])

# work with copy so if player solving integrated origional grid can be used to check
grid_copy = []
for r in range(0,9):
    grid_copy.append([])
    for c in range(0,9):
        grid_copy[r].append(grid[r][c])

while num_remove > 0:
    num_remove -= 1
# choose row/column that has not been removed already
    r = rd.randint(0,8)
    c = rd.randint(0,8)
    while grid_copy[r][c] == 0:
        r = rd.randint(0,8)
        c = rd.randint(0,8)
# put zero in place of removed number
    grid_copy[r][c] = 0

# solve sudoku and see how many solutions exist
    sols = solve_sudoku(grid_copy)
# if none/more than one solution exist, replace removed number
    if sols != 1:
        grid_copy[r][c] = grid[r][c]
        num_remove += 1

#print(', '.join(str(grid_copy[x][y]) for y in range(0,9)))