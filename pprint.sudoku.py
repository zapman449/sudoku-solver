#!/usr/bin/env python

import sys

if len(sys.argv) >= 2:
    puzzle = sys.argv[1].strip()
else:
    puzzle = sys.stdin.read().strip()

metas = [ '|', '|', '\n', '|', '|', '\n', '|', '|', '\n---+---+---\n', '|', '|', '\n', '|', '|', '\n', '|', '|', '\n---+---+---\n', '|', '|', '\n', '|', '|', '\n', '|', '|']

buf = ''
for i, c in enumerate(puzzle):
    if i % 3 == 0 and i != 0:
        # note: pop reads from the right normally. The list above is symetric so
        # it doesn't matter.  Might be clearer to call pop(0) though
        buf += metas.pop()
    buf += c

print buf
