#!/bin/bash
#Script that loops through a file list (typically containing only the name of a file in SAM) and converts that to an ifdh-readable path
#$1 the input list of files

for file in $(cat $1)
do
  sam_file=`basename $file`
  ifdh_path=`samweb -e sbnd get-file-access-url $sam_file`
  echo $ifdh_path
done
