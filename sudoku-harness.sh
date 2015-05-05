#!/bin/bash

if [ -d $1 ]; then
	DIR=$1
else
	echo "USAGE: $0 <directory of sudoku solvers>"
fi

ROOTDIR=$(dirname $0)

if [ "$ROOTDIR" == "." ]; then
	ROOTDIR=$(pwd)
fi

PUZZLES=${ROOTDIR}/puzzles.txt

cd $DIR

for f in ./*.py ; do
	echo -n "starting solver $f"
	cat $PUZZLES | while read pname puzzle solution; do
		echo -n " $pname"
		result=$(timeout 60 gtime --output=${f}@${pname}@time1 python ${f} ${puzzle} 2>&1)
		if [ "$result" != "$solution" ]; then
			echo
			echo "file $f failed to solve puzzle $puzzle"
			echo "wrong: -- $result --"
			echo "right: -- $solution --"
			break
		fi
		result=$(timeout 60 gtime --output=${f}@${pname}@time2 python ${f} ${puzzle} 2>&1)
		result=$(timeout 60 gtime --output=${f}@${pname}@time3 python ${f} ${puzzle} 2>&1)
		for res in ${f}@${pname}@time?; do
			t=$(cat $res | grep elapsed)
		done
	done
	echo " done"
done

${ROOTDIR}/compare.py
