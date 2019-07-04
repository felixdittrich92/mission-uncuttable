#!/bin/sh
git log --shortstat | grep -E "(Author: )(\b\s*([A-Z]\w+)){2}|fil(e|es) changed" | awk '
{
 if($1 ~ /Author/) {
  author = $2" "$3
 } else {
  files[author]+=$1
  inserted[author]+=$4
  deleted[author]+=$6
 }
}
END { for (key in files) { print "Author: " key "\n\tfiles changed: ", files[key], "\n\tlines inserted: ", inserted[key], "\n\tlines deleted: ", deleted[key] } }
'
