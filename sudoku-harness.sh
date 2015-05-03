#!/bin/bash

for f in ./*.py ; do
	cat ../puzzles.txt | while read pname puzzle solution; do
		result=$(timeout 60 gtime --output=${f}@${pname}@time1 python ${f} ${puzzle} 2>&1)
		if [ "$result" != "$solution" ]; then
			echo "file $f failed to solve puzzle $puzzle"
			echo "wrong: -- $result --"
			echo "right: -- $solution --"
			continue
		fi
		result=$(timeout 60 gtime --output=${f}@${pname}@time2 python ${f} ${puzzle} 2>&1)
		result=$(timeout 60 gtime --output=${f}@${pname}@time3 python ${f} ${puzzle} 2>&1)
		for res in ${f}.${pname}.time?; do
			t=$(cat $res | grep elapsed)
	done
done

../compare.py
