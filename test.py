from z3 import *

v = [Int('v%i' % i) for i in range(9)]

print(v)
solve_grid = []
for j in range(9):
    solve_grid.append([Int('%i%i' % (j+1) (k+1)) for k in range(9)])