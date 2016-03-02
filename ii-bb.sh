#!/usr/bin/busybox sh
# ii-клиент на чистом busybox

loader="wget -q -O -"

node="http://ii-net.tk/ii/ii-point.php?q="
authstr="your_authstr"
echolist="test.15 ii.test.14"
editor="vi"

indexdir="./echo"
msgdir="./msg"
unsentdir="./toss"
outdir="./out"

index="$node/u/e"
msg="$node/m"
point="$node/u/point"

mkdir -p $indexdir
mkdir -p $msgdir
mkdir -p $unsentdir
mkdir -p $outdir

fetch() {
	for echoarea in $echolist
	do
		msglist_query="$index/$echoarea"
		echo "fetch $msglist_query"
		msglist=`$loader $msglist_query`

		for i in $msglist
		do
			if [ "$i" = "$echoarea" ]
			then
				continue
			fi

			if [ -e "$msgdir/$i" ]
			then
				continue
			fi

			msg_query="$msg/$i"
			echo "fetch $msg_query"
			text=`$loader $msg_query`
			echo "$text" > $msgdir/$i
			echo "$i" >> $indexdir/$echoarea
		done
	done
}

write() {
	echo "not implemented"
}

view() {
	echo "not implemented"
}

nch() {
	echo "$1" | dd if=/dev/stdin bs=1 count=1 skip=$2 status=none
}

urlsafe_replace() {
	text=`echo "$1" | base64`
	len=${#text}
	i=0;
	while [ $i -le $len ]
	do
		char=`nch $text $i`
		if [ "$char" = "+" ]
		then
			echo -n "-"
		elif [ "$char" = "/" ]
		then
			echo -n "_"
		else
			echo -n $char
		fi
		i=$(($i+1))
	done
}

base64_urlsafe() {
	for i in $@
	do
		urlsafe_replace $i
	done
}

send() {
	files=`ls -1 $unsentdir`

	for file in $files
	do
		file_contents=`cat $unsentdir/$file`
		b64=`base64_urlsafe "$file_contents"`
		request="$point/$authstr/$b64"
		result=`$request`
		stat=`echo "$result" | dd if=/dev/stdin bs=1 count=6 status=none`
		echo "$result"

		if [ "$stat" = "msg ok" ]
		then
			mv $unsentdir/$file $outdir/$file
		fi
	done
}

case $1 in
"fetch") fetch;;
"view") view;;
"write") write;;
"send") send;;
"") echo "help will be provided later";;
esac
