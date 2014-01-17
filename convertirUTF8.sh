#!/bin/bash


DIRECTORIO=$1

cd $1
for file in *.txt
do
	iconv -c  -f ISO-8859-15 -t UTF-8 "$file" -o "${file%.txt}.utf8.txt"
	rm $file

done
