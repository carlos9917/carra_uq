#!/bin/bash
#go through all members for a given date and fetch
#the odb data

days=$($(seq -w 1 1 30))
months=$($(seq -w 4 1 5))
for year in 2017;do
  for month in 04; do
    for day in `seq -w 1 1 30`; do
      for init in `seq -w 0 3 21`; do
	for mem in 001 002 003 004 005 006 007 008 009; do
          echo "mkdir -p $year/$month/$day/$init"
	  dir=$year/$month/$day/$init/mbr$mem
          [ ! -d $dir ] && mkdir -p $dir
	  cd $dir
          echo "ecp ec:/suza/harmonie/JB_CARRA_alpha2_2012/$year/$month/$day/$init/mbr$mem/odb_stuff.tar ."
	  cd -
         done #mem

      done #init
    done #day	    
  done #month
done #year
