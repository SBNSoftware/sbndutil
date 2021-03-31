#!/bin/bash
#Script that deletes files via ifdh in a txt file

#$1 txt file containing file locations to delete

for filelocation in $(cat $1)
do
  ifdh rm  $filelocation
done
