#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.out
#SBATCH --job-name=fetchodb

#go through all members for a given date and fetch
#the odb data and untar it, create odb tables with dcgen
#months=($(seq -w 4 1 5))
dom=East
wrkdir=$PWD
days=($(seq -w 1 1 11))
yy=2012
mm=07
echo ${months[@]}
for year in $yy;do
  for month in $mm; do
    for day in ${days[@]}; do
      for init in `seq -w 0 3 21`; do
	    for mem in 000 001 002 003 004 005 006 007 008 009; do
	      dir=$wrkdir/$dom/$year/$month/$day/$init/mbr$mem/odb_ccma/CCMA
          rdir=$wrkdir/results/$dom/$year/$month/$day/$init/mbr$mem
          mkdir -p $rdir
          cp $dir/mbr${mem}*.dat $rdir
        done #mem
      done #init
    done #day	    
  done #month
done #year

#now change the damn permissions
echo "changing permissions"
for year in $yy;do
  chmod 755 $wrkdir/results/$dom/$year
  for month in $mm; do
    chmod 755 $wrkdir/results/$dom/$year/$month
    for day in ${days[@]}; do
      chmod 755 $wrkdir/results/$dom/$year/$month/$day
      for init in `seq -w 0 3 21`; do
         chmod 755 $wrkdir/results/$dom/$year/$month/$day/$init
	     for mem in 000 001 002 003 004 005 006 007 008 009; do
           rdir=$wrkdir/results/$dom/$year/$month/$day/$init/mbr$mem
          chmod 755 $rdir
          chmod 755 $rdir/*dat
        done #mem
      done #init
    done #day	    
  done #month
done #year
