#!/bin/bash

dir="./" # current working directory
indexdir="echo/"
msgdir="msg/"

onpage=2 # how many messages take from every echoarea
echoes=(
	"mlp.15"
	"lor-opennet.15"
)
declare -a msgids
maslength=0

for i in ${echoes[*]}; do
	# echofile=(`curl -s http://ii-net.tk/ii/ii-point.php?q=/e/$i`)
	echofile=(`cat $dir/$indexdir/$i`)
	length=${#echofile[@]}
	for ((a=$length-1; a>$length-$onpage-1; a--, maslength++)); do
		msgids[$maslength]=${echofile[$a]}
	done
done

cd $dir/$msgdir
sortedmsg=(`ls -1 -t ${msgids[@]}`)

for i in ${sortedmsg[*]}; do
# for i in ${msgids[*]}; do
	# curl http://ii-net.tk/ii/ii-point.php?q=/m/$i
	cat $i
	echo ""
done
