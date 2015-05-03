#!/usr/bin/python

from __future__ import print_function
import multiprocessing
import random
import sys
# import time

# 060900100308200000009006052400000005027080340500000008950700200000002607002004030
# 012345678901234567890123456789012345678901234567890123456789012345678901234567890
# 0         1         2         3         4         5         6         7         8
# s        s        s        s        s        s        s        s        s
#                            bbb      bbb      bb*
#                                              rr*rrrrrr
#   c        c        c        c        c        *        c        c        c
#   2        11       20       29       38       47       56       65       74


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


def r(a, lock, answer):
    # print('starting a is', a)
    if random.randint(0, 9) == 9 and answer.value != 0:
        return -1
    i = a.find('0')
    if i == -1:
        answer.value = 1
        print(a)
        return -1

    excluded_numbers = set()
    for j in range(81):
        if same_row(i, j) or same_col(i, j) or same_block(i, j):
            excluded_numbers.add(a[j])

    # with lock:
    #     print(len(excluded_numbers), repr(excluded_numbers))
    x = 0
    for m in '123456789':
        if m not in excluded_numbers:
            x = r(a[:i] + m + a[i + 1:], lock, answer)
            if x == -1:
                # with lock:
                #     print('got a neg1!')
                break
    if x == -1:
        return x
    # print("returning None. i is: " + str(i) + " j is: " + str(j) + " Excluded Numbers is: " + repr(sorted(list(excluded_numbers))))
    # print(a)


def r_mp(a):
    lock = multiprocessing.Lock()
    answer = multiprocessing.Value('i', 0)
    i = a.find('0')
#     if lock is None:
#         print("lock is None")
    if i == -1:
        print(a)
        return None

    excluded_numbers = set()
    for j in range(81):
        if same_row(i, j) or same_col(i, j) or same_block(i, j):
            excluded_numbers.add(a[j])

    processes = []
    for m in '123456789':
        if m not in excluded_numbers:
            # print('setting up process for m =', m)
            proc = multiprocessing.Process(target=r,
                                           args=(a[:i] + m + a[i + 1:],
                                                 lock,
                                                 answer))
            processes.append(proc)
    for proc in processes:
        # print('starting a proc:')
        proc.start()
    # print('joining each proc:')
    for proc in processes:
        proc.join()
    # print('all joins done')
    # print("returning None. i is: " + str(i) + " j is: " + str(j) + " Excluded Numbers is: " + repr(sorted(list(excluded_numbers))))
    # print(a)


if __name__ == '__main__':
    if len(sys.argv) == 2 and len(sys.argv[1]) == 81:
        r_mp(sys.argv[1])
    else:
        print('Usage: python sudoku.py puzzle')
        print('''    where puzzle is an 81 character string
    representing the puzzle read left-to-right,
    top-to-bottom, and 0 is a blank''')
