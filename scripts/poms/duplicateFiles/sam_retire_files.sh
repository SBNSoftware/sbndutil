#!/bin/bash
#Script that retires files in a txt file

#$1 txt file containing file locations to retire

for filelocation in $(cat $1)
do
  file=`basename $filelocation`
  samweb -e sbnd retire-file $file
done
