#!/usr/bin/env python

import decimal
# import itertools
import operator
import os


def get_etime(f):
    with open(f, 'r') as fo:
        for line in fo:
            if 'elapsed' in line:
                words = line.split()
                t = words[2]
                idx = t.find('e')
                t2 = t[:idx]
                t3 = t2[2:]
                return decimal.Decimal(t3)


def best_scores(solver, data):
    # print(repr(data))
    results = []
    for puzzle in data[solver]:
        results.append(min(data[solver][puzzle]))
    return results


def score_results(baseline, results):
    print(repr(baseline))
    print(repr(results))
    tally = decimal.Decimal(0)
    for b, r in zip(baseline, results):
        tally += ((b - r) * 10)
    return tally


def main():
    base_solver = 'sudoku1.py'
    files = os.listdir('.')
    data = {}
    for f in files:
        if f.endswith('time1') or f.endswith('time2') or f.endswith('time3'):
            # ${f}.${pname}.time2  $f is solver, $pname is puzzle
            words = f.split('@')
            etime = get_etime(f)
            data.setdefault(words[0], {}).setdefault(words[1], []).append(etime)
    baseline = best_scores(base_solver, data)
    # print(repr(baseline))
    finals = {}
    for solver in data:
        if solver == base_solver:
            continue
        results = best_scores(solver, data)
        finals[solver] = score_results(baseline, results)
    print(sorted(finals.items(), key=operator.itemgetter(1)))


if __name__ == '__main__':
    main()
