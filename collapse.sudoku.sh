#!/bin/bash

# takes a pretty-printed sudoku and collapses it back to an 81 character string

if [ $# -ge 1 -a -f "$1" ]; then
	input="$1"
else
	input="-"
fi

cat $input | xargs | sed -e 's/[ |+-]//g'
