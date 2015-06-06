#!/bin/bash

USAGE(){
	echo "USAGE: $0 <directory of sudoku solvers>"
	exit
}

if [ -z $1 ]; then
	USAGE
elif [ -d $1 ]; then
	DIR=$1
	shift
	echo "Usind directory $DIR for puzzles"
else
	USAGE
fi

ROOTDIR=$(dirname $0)

if [ "$ROOTDIR" == "." ]; then
	ROOTDIR=$(pwd)
fi

PUZZLES=${ROOTDIR}/puzzles.txt

if [ -z "$1" ]; then
	:	# : is a shell noop
elif [ "$1" == "-p" ] && [ -f "$2" ]; then
	PUZZLES=${ROOTDIR}/$2
	shift
	shift
else
	USAGE
fi

TIME=''
for clock in time gtime ; do
	which $clock >/dev/null 2>&1
	if [ "$?" == "1" ]; then
		continue
	fi
	version=$($clock -V 2>&1)
	if [ "$?" != "0" ]; then
		continue
	fi
	echo $version | grep GNU > /dev/null
	if [ "$?" == "0" ]; then
		TIME=$clock
		break
	fi
done

# echo $TIME
if [ -z "$TIME" ]; then
	echo "Could not find valid gnu time executable in your PATH"
	exit
fi

cd $DIR

for f in ./*.py ; do
	echo -n "starting solver $f"
	cat $PUZZLES | while read pname puzzle solution; do
		echo -n " $pname"
		result=$(timeout 60 $TIME --output=${f}@${pname}@time1 python ${f} ${puzzle} 2>&1)
		if [ "$result" != "$solution" ]; then
			echo
			echo "file $f failed to solve puzzle $puzzle"
			echo "wrong: -- $result --"
			echo "right: -- $solution --"
			break
		fi
		result=$(timeout 60 $TIME --output=${f}@${pname}@time2 python ${f} ${puzzle} 2>&1)
		result=$(timeout 60 $TIME --output=${f}@${pname}@time3 python ${f} ${puzzle} 2>&1)
		# for res in ${f}@${pname}@time?; do
		# 	t=$(cat $res | grep elapsed)
		# done
	done
	echo " done"
done

${ROOTDIR}/compare.py
rm -f *time?
