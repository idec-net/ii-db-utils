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

view() {
	if [ "$2" = "" ]
	then
		echoarea="`cat $indexdir/$1`"
		for msgid in $echoarea
		do
			echo "N=$i; id=$msgid;"
			cat $msgdir/$msgid
			echo ""
			i=$(($i+1))
		done
	else
		filesize=$((`stat $indexdir/$1 -c %s`))
		if [ "$2" = "len" ]
		then
			echo $(($filesize/21))
		else
			number=$(($2))
			echoarea="`cat $indexdir/$1`"
			i=0
			for msgid in $echoarea
			do
				if [ $i -eq $number ]
				then
					echo "N=$i; id=$msgid;"
					cat $msgdir/$msgid
				fi
				i=$(($i+1))
			done
		fi
	fi
}

nch() {
	echo "$1" | dd if=/dev/stdin bs=1 count=1 skip=$2 status=none
}

urlsafe_replace() {
	text=$1
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
	src=`echo "$1" | base64`
	for i in $src
	do
		urlsafe_replace $i
	done
}

reparseSubj() {
	str="`echo "$1" | dd if=/dev/stdin bs=1 count=3 status=none`"
	if [ "$str" != "Re:" ]
	then
		echo -n "Re: "
	fi

	echo -n $1
}

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
	echo=$1

	if [ "$2" = "" ]
	then
		template="$echo\nAll\n...\n\n"
		# не отвечаем, а пишем новое
	else
		echoarea="`cat $indexdir/$echo`"
		count=$(($2))
		i=0
		for msgid in $echoarea
		do
			if [ $i -eq $count ]
			then
				msg="`cat $msgdir/$msgid`"
				echo="`head -n 2 $msgdir/$msgid | tail -n 1 -`"
				user="`head -n 4 $msgdir/$msgid | tail -n 1 -`"
				subj="`head -n 7 $msgdir/$msgid | tail -n 1 -`"
				subj="`reparseSubj "$subj"`"
				template="$echo\n$user\n$subj\n\n@repto:$msgid\n"
			fi
			i=$(($i+1))
		done
	fi

	filename="$unsentdir/`date -Iseconds`"
	echo -e $template > $filename
	$editor $filename
}

send() {
	files=`ls -1 $unsentdir`

	for file in $files
	do
		file_contents=`cat $unsentdir/$file`
		b64=`base64_urlsafe "$file_contents"`
		result="`$loader $point/$authstr/$b64`"
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
"view") view $2 $3;;
"write") write $2 $3;;
"send") send;;
"") echo "help will be provided later";;
esac
