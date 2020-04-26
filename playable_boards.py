# take sukodu board
# for easy, remove n = ? numbers
# for medium, remove n = ? numbers
# for hard, remove n = ? numbers

# remove random cell, check:
    # can it still be solved?
    # if yes, continue removing
    # if no, put number back in

import argparse
from z3 import *
import random as rd
import itertools

def solve_sudoku(grid):
    s = Solver()

    solve_grid = []
    solve_grid = [[Int('v%i%i' % (j, k)) for k in range(1,10)] for j in range(1,10)]
    #print(solve_grid)
    #number_list = [Int('n%i'%i) for i in range(0,81)]

    #solve_grid = []
    #for j in range(9):
        #solve_grid.append([Int('v1%i', % j+1), Int(), Int(), Int(), Int(), Int(), Int(), Int(), Int()])

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
        #for r in range(9):
            #s.add(Distinct(solve_grid[r][c]))
        s.add(Distinct([solve_grid[r][c] for r in range(9)]))

    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            s.add(Distinct([solve_grid[j][k] for j, k in itertools.product(range(3), range(3))]))

    cntr = 0
    while s.check() == sat:
        cntr += 1
        m = s.model()
        r = [ [ m.evaluate(solve_grid[i][j]) for j in range(9) ]
          for i in range(9) ]
        print(r)
        #s.add(Not(And(r == m[r])))
        s.add(Not(And([[solve_grid[j][k] == m[solve_grid[j][k]] for k in range (9)] for j in range(9)])))
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

# make the numbers 0-9 Reals
n = [Int('i') for i in range(10)]
# seed for random number generator
rd.seed(None)

#test_grid for working through code---this will be generated grid in final
test_grid = []
test_grid.append([1, 7, 9, 8, 3, 5, 2, 6, 4])
test_grid.append([4, 2, 5, 6, 1, 9, 7, 8, 3])
test_grid.append([8, 3, 6, 2, 7, 4, 5, 1, 9])
test_grid.append([6, 5, 1, 9, 4, 2, 3, 7, 8])
test_grid.append([3, 4, 2, 7, 5, 8, 6, 9, 1])
test_grid.append([7, 9, 8, 3, 6, 1, 4, 2, 5])
test_grid.append([2, 1, 3, 4, 8, 6, 9, 5, 7])
test_grid.append([5, 6, 7, 1, 9, 3, 8, 4, 2])
test_grid.append([9, 8, 4, 5, 2, 7, 1, 3, 6])

# work with copy so if player solving integrated origional grid can be used to check
grid_copy = []
for r in range(0,9):
    grid_copy.append([])
    for c in range(0,9):
        grid_copy[r].append(test_grid[r][c])

# take numbers out until level hits 0
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
        grid_copy[r][c] = test_grid[r][c]
        level += 1

print(test_grid)
print(grid_copy)







