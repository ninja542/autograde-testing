#!/bin/bash
files=`ls`
find . -iname "*" | while read file
do
	echo $file
	folder=`echo $file | cut -d "-" -f 3 | xargs`
	echo "creating folder $folder"
	mkdir -p "$folder"
	newname=`echo $file | cut -d "-" -f5- | xargs`
	echo "Renaming to $newname"
	mv "$file" "./$folder/$newname"
done
