#! /bin/bash

#Script that runs fife_util's duplicate file finder and then identifies all descendants to make a list of duplicate files and their children + children-children etc

#$1 sam def name to check for duplicates

direct_duplicates=`sam_dataset_duplicate_kids --dims="ischildof: ( isparentof: ( defname: $1 ) )" --include_metadata="file_format" --include_metadata="run_number" --include_metadata="subrun_number" | grep -v parent | grep -v duplicates`

for file in $direct_duplicates
do
  echo $file
  samweb -e sbnd file-lineage descendants $file
done
