"""
Solve sudoku problems using CSP (Constraint Satisfaction Programming).

Copyright (c) 2015, Leif Poorman <leif.poorman@gmail.com>
License: MIT License; http://opensource.org/licenses/MIT

Dependencies:
python-constraint==1.2

I believe the external dependency, while pure python, makes this program
disqualified under the rules of the pyatl contest.
"""

import sys
import constraint as cp

### Util

def pp_puzzle_string(ps):
    "pretty print puzzle string"
    res = ''
    hsep = '|-------+-------+-------|'
    for r in range(0, 81, 9):
        row = ps[r:r+9]
        if r in (27, 54):
            res += hsep + '\n'
        res += '| '
        res += ' | '.join(
                ' '.join(n for n in chunk)
                for chunk in(row[0:3], row[3:6], row[6:9]))
        res += ' |\n'
    return res

### CSP

def sudoku_constraints(vars):
    row_constraints = [(cp.AllDifferentConstraint(), row) for row in vars]
    col_constraints = [(cp.AllDifferentConstraint(), [row[c] for row in vars])
            for c in range(9)]
    blocks = [[(rs + i, cs + j) for i in range(3) for j in range(3)]
            for rs in (0, 3, 6) for cs in (0, 3, 6)]
    block_constraints = [
            (cp.AllDifferentConstraint(), [vars[r][c] for r, c in block])
            for block in blocks]
    return (row_constraints, col_constraints, block_constraints)

def initial_values(puzzle_string):
    nums = [[int(c) for c in puzzle_string[r:r+9]] for r in range(0, 81, 9)]
    return {(r, c): nums[r][c]
            for r in range(9) for c in range(9) if nums[r][c] != 0}

def get_domain(init_vals, r, c):
    if (r, c) in init_vals:
        return cp.Domain(set([init_vals[(r, c)]]))
    else:
        return cp.Domain(set(range(1, 10)))

def setup_problem(puzzle_string, solver=None):
    assert len(puzzle_string) == 81
    problem = cp.Problem(solver)
    vars = [[cp.Variable('x_%d%d' % (r, c)) for c in range(9)] for r in range(9)]
    init_vals = initial_values(puzzle_string)
    for r in range(9):
        for c in range(9):
            problem.addVariable(vars[r][c], get_domain(init_vals, r, c))
    for cs in sudoku_constraints(vars):
        for c, vs in cs:
            problem.addConstraint(c, vs)
    return problem

### Output

def solution_str(sol):
    s = ['0']*81
    for var, val in sol.iteritems():
        name = var.name
        r, c = int(name[2]), int(name[3])
        s[9 * r + c] = str(val)
    return ''.join(s)

def main(ps):
    prob = setup_problem(ps)
    sol = prob.getSolution()
    print solution_str(sol)

if __name__ == '__main__':
    if len(sys.argv) == 2 and len(sys.argv[1]) == 81:
        main(sys.argv[1])
    else:
        print('Usage: python sudoku.py puzzle')
        print('''    where puzzle is an 81 character string
    representing the puzzle read left-to-right,
    top-to-bottom, and 0 is a blank''')
