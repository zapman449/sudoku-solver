sudoku-solver
=============
The great Sudoku solver challenge for Python Atlanta!

Use your skills to produce a sudoku solver.  Rules:

1. Pure python solution

2. Totally local solution (no call-outs to a CUDA powered AWS instance, for example).

3. Your solution should be self contained in a single file.  The python standard library fair to use.

4. Must be callable via 'python <your script> <81char sudoku puzzle>' (full example below)

5. Puzzle spec must be 81 characters string.  Accept 0 as unknown slots in the sudoku puzzle.

6. Output must be the solved puzzle presented as an 81 character string.  The 81 characters begin in the top left of the puzzle.  The first 9 characters are the top row of the puzzle, left to right.  The next 9 are the second row, etc.  Full example:
  ```
  $ python ./sudoku1.py 020000000000600003074080000000003002080040010600500000000010780500009000000000040
  126437958895621473374985126457193862983246517612578394269314785548769231731852649
  ```

7. Name the file uniquely (sudoku1.py is a poor choice).

8. Place a leading docstring at the top of your file indicating your authorship.

9. Contest will either run on my multi-core macbook, or a multi-core linux VM.  Default python is 2.7.8.  Python3.4 is available on request.  

10. Submit your solution as a pull request into this github repo: https://github.com/zapman449/sudoku-solver.git   .  Please place your code either in the p2 directory (for python 2) or the p3 directory (for python 3).

11. The winner will need to discuss their solution and how it works in detail.  Other people should be willing to give a 'lightening talk' on their solution.

12. Cheating will cause you to be disqualified from winning, though may force you to give a ligtening talk about WHY your cheat was interesting.  Examples of cheating: searching for a source puzzles.txt file and finding the solution there.

13. Must be present at Python Atlanta August meetup to win.

Other details:

The script 'sudoku-harness.sh' (and 'compare.py') will run each solver, and
compare the results of the tests.  An assortment of puzzles will be attempted
with your solution.  Absolute timeout is 60 seconds.  If you take that long,
you've blown it.  Time will measured via gnu time's 'elapsed' time.  Each
puzzle will be attempted 3 times, and the best of those three times will be
used for scoring.  Note: the puzzles in puzzles.txt are NOT the puzzles you'll
be judged on, but they are representative.  Usage example:

```
$ ./sudoku-harness.sh ./p2
Usind directory p2 for puzzles
starting solver ./sudoku1.py puzzle5 puzzle6 done
starting solver ./sudoku2.py puzzle5 puzzle6 done
starting solver ./sudoku3.py puzzle5 puzzle6 done
Solver sudoku3.py has a score of 49.00
Solver sudoku2.py has a score of 41.40
```

Requirements: gnu-time.  sudoku-harness looks in $PATH for either time or gtime, and tries to ensure it's gnu-time.
