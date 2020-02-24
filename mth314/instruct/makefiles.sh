#!/bin/bash
files=`ls`
find . -iname "*" | while read file
do
	echo $file
	folder=`echo $file | cut -d "-" -f 3 | xargs`
	newname=`echo $file | cut -d "-" -f5- | xargs`
	echo "Renaming to $newname"
	mv "$file" "$newname"
done
