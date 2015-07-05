#!/usr/bin/python

"""
Modified version of sudoku1.py showing how the same algorithm with a trivial
optimization (and some cleanups) gives a huge performance increase.

A more comprehensive algorithm will definitely be faster and better at solving
the harder problems, I just think it is useful to show how much faster the
baseline solver can be :-)

The main reason this is so much faster is that sudoku1 calls the same_ functions
millions of times to solve a puzzle:

    4030560 same_row
    3582720 same_col
    3184640 same_block

There are only 6561 different combinations that need to be checked, and
pre-computing the results removes the need for 10,000,000 function calls.

by Justin Azoff
"""

from __future__ import print_function
import sys

# 060900100308200000009006052400000005027080340500000008950700200000002607002004030
# 012345678901234567890123456789012345678901234567890123456789012345678901234567890
# 0         1         2         3         4         5         6         7         8
# s        s        s        s        s        s        s        s        s
#                            bbb      bbb      bb*
#                                              rr*rrrrrr
#   c        c        c        c        c        *        c        c        c
#   2        11       20       29       38       47       56       65       74

ALL_NUMBERS = set('123456789')

def same_row(i, j):
    """uses floor division.  If floor division is equal for both, same row"""
    return (i // 9 == j // 9)


def same_col(i, j):
    """if you're in the same column, subtracting indicies will result in a
    multiple of 9."""
    return (i - j) % 9 == 0


def same_block(i, j):
    """divide i and j by 27... that will give which set of 3 rows it's in.
    i and j mod 9 divided by 3 will give which set of three rows it's in."""
    return (i // 27 == j // 27 and i % 9 // 3 == j % 9 // 3)

# Pre compute what the 'interesting' locations are for all of the other locations
related_locations = [[] for _ in range(81)]

for i in range(81):
    for j in range(81):
        if same_row(i, j) or same_col(i, j) or same_block(i, j):
            related_locations[i].append(j)
# OR 
# related_locations = [
#    [j for j in range(81) if same_row(i, j) or same_col(i, j) or same_block(i, j)]
#    for i in range(81)
#]

def r(a):
    # global tickle
    # tickle += 1
    i = a.find('0')
    if i == -1:
        # print("number of recursive calls: " + str(tickle))
        print(a)
        sys.exit(0)

    excluded_numbers = set(a[j] for j in related_locations[i])

    for m in ALL_NUMBERS - excluded_numbers:
        r(a[:i] + m + a[i + 1:])
    # print("returning None. i is: " + str(i) + " j is: " + str(j) + " Excluded Numbers is: " + repr(sorted(list(excluded_numbers))))
    # print(a)


if __name__ == '__main__':
    # tickle = 0
    if len(sys.argv) == 2 and len(sys.argv[1]) == 81:
        r(sys.argv[1])
    else:
        print('Usage: python sudoku.py puzzle')
        print('''    where puzzle is an 81 character string
    representing the puzzle read left-to-right,
    top-to-bottom, and 0 is a blank''')
