# Suduko Generator, Final Project ECEN 2703
# Ella Wawrzynek & XuTao Ho

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
                    
    s.add(rows[0][0] == rd.randint(1,9))

    results = s.check()
    if results == sat:
        print("Full Board")
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
            if type(grid[r][c]) != type(0):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sudoku board generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--difficulty', help='level of board difficulty (0, 1, 2, or 3)',
                        default=1, type=int)
    args = parser.parse_args()

level = args.difficulty
if level == 0:
    num_remove = 0
if level == 1:
    num_remove = 27
if level == 2:
    num_remove = 36
if level == 3:
    num_remove = 45

n = [Int('i') for i in range(10)]
rd.seed(None)

grid = generate_board()

grid_copy = []
for r in range(0,9):
    grid_copy.append([])
    for c in range(0,9):
        grid_copy[r].append(grid[r][c])

while num_remove > 0:
    num_remove -= 1
    r = rd.randint(0,8)
    c = rd.randint(0,8)
    while grid_copy[r][c] == 0:
        r = rd.randint(0,8)
        c = rd.randint(0,8)
    grid_copy[r][c] = 0

    sols = solve_sudoku(grid_copy)
    if sols != 1:
        grid_copy[r][c] = grid[r][c]
        num_remove += 1

for x in range(9):
    for y in range(9):
        if type(grid_copy[x][y]) == type(0):
            grid_copy[x][y] = '_'

print("Player's Board")
for x in range(0,9):
        print(', '.join(str(grid_copy[x][y]) for y in range(0,9)))