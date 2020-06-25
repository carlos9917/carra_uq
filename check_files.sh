#!/bin/bash
files=(`ls 2012/07/??/??/obs_code_var_unique.dat`)
for filename in ${files[@]}; do
 echo "$filename"
    check36=`grep 36 $filename`
    if [ ! -z "$check36" ];then
        echo "36 present in $filename"
    fi
 cat "$filename"
done 
