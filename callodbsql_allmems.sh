#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/odbsql-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/odbsql-%J.out
#SBATCH --job-name=170111


module load odb
module load python3
days=($(seq -w 1 1 11))
days=(10)
dom=West
wrkdir=$PWD/$dom
cd $wrkdir
cp ../search_HM_Date.py .
for year in 2017;do
  for month in 01; do
    for day in ${days[@]}; do
      echo "Going through $year/$month/$day"
      python3 search_HM_Date.py -d "$year/$month/$day" >& ./$year/$month/$day/out_hm_search.txt
      chmod 755 ./$year/$month/$day/out_hm_search.txt
      #for init in `seq -w 0 3 21`; do
      #  for mem in 000 001 002 003 004 005 006 007 008 009; do
      #    echo "Doing member $year/$month/$day/$init/mbr$mem"
      #    dir=$wrkdir/$year/$month/$day/$init/mbr$mem/odb_ccma/CCMA/
      #    cd $dir
      #    odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == 1 AND codetype == 11 AND varno == 1" |sed "s/'//g" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat 
      #    cd -
      #  done #mem
      #done #init
    done #day
   done #month
done #year
