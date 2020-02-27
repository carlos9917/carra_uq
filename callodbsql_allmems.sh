#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.out
#SBATCH --job-name=runodbsql


module load odb
wrkdir=$PWD
for year in 2012;do
  for month in 07; do
    for day in 01; do
      for init in `seq -w 0 3 21`; do
        for mem in 000 001 002 003 004 005 006 007 008 009; do
          #echo "mkdir -p $year/$month/$day/$init"
          echo "Doing member $year/$month/$day/$init/mbr$mem"
          dir=$wrkdir/$year/$month/$day/$init/mbr$mem/odb_ccma/CCMA/
          cd $dir
          odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == 1 AND codetype == 11 AND varno == 1" |sed "s/'//g" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat 
          cd -
        done #mem
      done #init
    done #day
   done #month
done #year