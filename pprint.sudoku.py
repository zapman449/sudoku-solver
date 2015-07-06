#!/usr/bin/env python

"""
takes an 81 character string from either stdin or the command line.
Outputs a pretty printed version on 11 lines
Ex:
./pprint.sudoku.py 839465712146782953752391486391824675564173829287659341628537194913248567475916238
839|465|712
146|782|953
752|391|486
---+---+---
391|824|675
564|173|829
287|659|341
---+---+---
628|537|194
913|248|567
475|916|238
"""

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
