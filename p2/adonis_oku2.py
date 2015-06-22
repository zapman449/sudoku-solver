__author__ = 'abovell'

""""Single threaded class based solution to the sudoku problem. Easier to understand"""

import random
import sys

class InvalidStateException(Exception):
    pass

class Square(object):
    OPTIONS = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

    def __init__(self, index, value):
        self.index = index
        self.column = index % 9
        self.row = index // 9
        self.block = (self.column // 3) + 3 * (self.row // 3)
        self.value = value
        self.options = Square.OPTIONS
        self.neighbors = set()

    def solve(self):
        self.update_options()
        n = len(self.options)
        if n == 1:
            self.value = self.options.pop()
            return True
        if n == 0:
            raise InvalidStateException('\t({0!s})'.format(self.index))
        return False

    def __repr__(self):
        return self.value

    def update_options(self):
        used_options = set()
        for square in self.neighbors:
            used_options.add(square.value)
        self.options = self.options - used_options

    def learn_neighbors(self, parent):
        for square in parent.row(self.row):
            self.neighbors.add(square)
        for square in parent.column(self.column):
            self.neighbors.add(square)
        for square in parent.block(self.block):
            self.neighbors.add(square)
        self.neighbors = self.neighbors - set([self])

class Puzzle(object):
    STATES = []

    def __init__(self, sequence):
        self.build_puzzle(sequence)

    def build_puzzle(self, sequence):
        self.squares = []
        self.unsolved = []
        for index, value in enumerate(sequence):
            self.squares.append(Square(index, value))
            if value == '0':
                self.unsolved.append(self.squares[index])
        for square in self.unsolved:
            square.learn_neighbors(self)

    def column(self, c):
        return [self.squares[index] for index in range(c, 81, 9)]

    def row(self, r):
        return [self.squares[index] for index in range(r*9, (r+1)*9)]

    def block(self, b):
        column = (b % 3) * 3
        row = (b // 3) * 3
        indices = []
        for i in range(3):
            start = (row+i)*9 + column
            indices.extend(range(start, start+3, 1))
        return [self.squares[index] for index in indices]

    def solve(self):
        unsolved = []
        for square in self.unsolved:
            if not square.solve():
                unsolved.append(square)
        unsolved.sort(key=lambda square: len(square.options), reverse=True)
        self.unsolved = unsolved

    def save_state_and_guess(self):
        # TODO: save more state parameters
        # TODO: spawn separate threads instead of guessing
        state = str(self)
        square = self.unsolved.pop()
        index = square.index
        square.value = random.sample(square.options, 1)[0]
        others = square.options - set(square.value)
        Puzzle.STATES.append((state, index, others))

    def restore_state_and_continue(self):
        state, index, others = Puzzle.STATES.pop()
        self.build_puzzle(state)
        self.squares[index].options = others

    def progress(self):
        start_state = len(self.unsolved)
        self.solve()
        return len(self.unsolved) - start_state

    def solved(self):
        return len(self.unsolved) == 0

    def __repr__(self):
        return self.__str__()
        string = ''
        for square in self.squares:
            string += str(square)
            if square.value == '0':
                string += ' ({0!s})'.format(len(square.options))
            string += '\t'
            if square.index % 9 == 8:
                string += '\n'
        string += 'Unsolved: ' + str(len(self.unsolved))
        return string

    def __str__(self):
        string = [str(square) for square in self.squares]
        return ''.join(string)

def main():
    puzzle = Puzzle(sys.argv[1])
    while True:
        if puzzle.solved():
            print puzzle
            return
        try:
            if puzzle.progress() == 0:
                puzzle.save_state_and_guess()
        except InvalidStateException as e:
            puzzle.restore_state_and_continue()

# if __name__ == '__main__':

main()

