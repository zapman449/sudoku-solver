#!/usr/bin/python

import itertools
#import sys

rows = []
columns = []
blocks = []

# rows is a list of lists. The sublists hold the indices of each row.
# columns is the same, but for colums.
for i in range(9) :
    rows.append(range(i*9, (i*9)+9, 1))
    columns.append(range(i, 81, 9))

# blocks does the same as rows and columns, but it's build is much more complex.
for i in 0, 3, 6,  27, 30, 33,  54, 57, 60 :
    blocks.append( [] )
    for j in 0, 1, 2,  9, 10, 11,  18, 19, 20 :
        blocks[-1].append(i+j)

def gen_board() :
    """generate a full board, all posibilities open"""
    board = []
    for x in range(81) :
        board.append([1,2,3,4,5,6,7,8,9])
    return board

def which_rcb(idx) :
    """takes an index into the board (a number between 0 and 80 inclusive)
    Returns a tuple containing the index of which board, column and block
    that contain that index"""
    if idx < 0 or idx > 80 :
        return None
    row = idx // 9
    column = idx % 9
    block = ( 3 * ( row // 3 )) + ( column // 3 )
    #print "which_rcb given idx %d yields row %d column %d block %d" % (idx, row, column, block)
    return (row, column, block)

def index_constrains(idx) :
    """Given an index into the board, return a sorted and unique'ed list of 
    all indexes in its row, column and block"""
    if idx < 0 or idx > 80 :
        return None
    row, column, block = which_rcb(idx)
    spaces = set()
    for tidx in rows[row] :
        spaces.add(tidx)
    for tidx in columns[column] :
        spaces.add(tidx)
    for tidx in blocks[block] :
        spaces.add(tidx)
    return sorted(list(spaces))

def print_indexes() :
    """print the index position of all indexes in the board.
    Useful mostly for debugging"""
    counter = 0
    for row in rows :
        print "%2d %2d %2d | %2d %2d %2d | %2d %2d %2d" % ( row[0], row[1], row[2], 
                                                            row[3], row[4], row[5],
                                                            row[6], row[7], row[8] )
	if counter == 2 or counter == 5 :
            print "-" * 30
        counter += 1

def constrain_spaces(board, spaces, idx) :
    """takes a board, a list of spaces tied to an index, and the index
    eliminate the value at idx from all indexes in spaces"""
    #print 'cs1 spaces', spaces
    if idx < 0 or idx > 80 :
        return None
    if len(board[idx]) != 1 :
        return None
    for tidx in spaces :
        if tidx == idx :
            continue
        #print 'cs', 'tidx', tidx, 'board[tidx]', board[tidx], 'idx', idx, 'board[idx]', board[idx],
        if len(board[tidx]) > 1 :
            try :
                board[tidx].remove(board[idx][0])
            except ValueError:
                pass
            if len(board[tidx]) == 1 :
                constrain(board, tidx)
        #print '---', board[tidx]

def constrain(board, idx) :
    """wrapper function for constrain_spaces"""
    if idx < 0 or idx > 80 :
        return None
    spaces = index_constrains(idx)
    constrain_spaces(board, spaces, idx)

def initial_constraints(constraint_str, board) :
    """apply the initial constraints to the board."""
    for idx, c in enumerate(constraint_str) :
        if c == '_' :
            continue
        board[idx] = [int(c),]
    apply_constraints(board)

def apply_constraints(board) :
    for idx in range(len(board)) :
        if len(board[idx]) > 1 :
           continue
        #b1 = board_printer(board, printme=False)
        constrain(board, idx)
        #b2 = board_printer(board, printme=False)
        #print 'ac idx %d board[idx] %s' % (idx, repr(board[idx]))
        #compare_two_boards(b1, b2)

def test9(subsection, board) :
    """test that a subsection of 9 indexes contains 9 unique numbers between 1
    and 9."""
    x = set()
    for s in subsection :
        if 1 <= s <= 9 :
            x.add(board[s][0])
    if len(x) == 9 :
        return True
    return False

def validate_solution(board) :
    """validate that a board has a proper solution.
    Work to be done: test9 validates unique 9.  Need a for i in board : check i
    holds number unique to it 'spaces'."""
    x = sum(map(len, board))
    if x != 81 :
        print 'x is', x
        return False
    for subsection in itertools.chain(rows, columns, blocks) :
        x = test9(subsection, board)
        if x is False :
            #print subsection
            return False
    return True

def compare_two_boards(boardstr1, boardstr2) :
    """take two boards (as output by board_printer(board, printme=False)), and 
    print both of them side by side."""
    for x in itertools.izip(boardstr1.splitlines(), boardstr2.splitlines()) :
        print "        ".join(x)
    print

def board_printer(board, printme=True) :
    """print out a board."""
    result = ''
    hcounter = 1
    vcounter = 1
    for row in rows :
        r1 = ''
        r2 = ''
        r3 = ''
        for space in row :
            #print 'space', space, 'board[space]', board[space]
            #print 'start r1 %s r2 %s r3 %s done' % (r1, r2, r3)
            if len(board[space]) == 1 :
                r1 += "   "
                r2 += "-%d-" % board[space][0]
                r3 += "   "
            else :
                x = ''
                for i in range(1, 10) :
                    if i in board[space] :
                        x += str(i)
                    else :
                        x += ' '
                r1 += x[:3]
                r2 += x[3:6]
                r3 += x[6:]
                #print 'x is', x, 'r1 is', r1, 'r2 is', r2, 'r3 is', r3, 'fin'
            if vcounter % 3 == 0 :
               r1 += '||'
               r2 += '||'
               r3 += '||'
            else :
               r1 += '|'
               r2 += '|'
               r3 += '|'
            vcounter += 1
            #print 'finish r1 %s r2 %s r3 %s done' % (r1, r2, r3)
        if hcounter % 3 == 0 :
            hbar = '-_-_-_' * 6 
            hbar += '-'
        else :
            hbar = '-' * 37
        hcounter += 1
        if printme :
            print r1[:-2]
            print r2[:-2]
            print r3[:-2]
            print hbar
        result += r1[:-2]
        result += '\n'
        result += r2[:-2]
        result += '\n'
        result += r3[:-2]
        result += '\n'
        result += hbar
        result += '\n'
    result = result[:-39]    # strip training newline
    return result
                    
def main() :
    constraints = '63_2_8_1_2___5__891_9_6__3___8__6_5____187____6_5__9___9__7_1_681__2___5_2_4_3_97'
#63_2_8_1_
#2___5__89
#1_9_6__3_
#__8__6_5_
#___187___
#_6_5__9__
#_9__7_1_6
#81__2___5
#_2_4_3_97'

#635 298 714
#274 351 689
#189 764 532

#748 936 251
#952 187 463
#361 542 978

#493 875 126
#817 629 345
#526 413 897

    board = gen_board()
    initial_constraints(constraints, board)
    apply_constraints(board)
    solved = validate_solution(board)
    if solved :
        board_printer(board)
    #x = board_printer(board, printme=False)
    #print x

if __name__ == '__main__' :
    main()
