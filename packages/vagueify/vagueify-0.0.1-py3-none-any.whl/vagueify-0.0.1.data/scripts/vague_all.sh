#!/usr/bin/env bash

FILES=$(find $1 -type f)
for f in $FILES
do
  echo "Processing $f file..."
  python vagueify.vagueify -i $f -o res.txt;
done;
