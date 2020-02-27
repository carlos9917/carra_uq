#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.out
#SBATCH --job-name=fetchlogs

#this loop will go inside get_all_members.sh

wrkdir=$PWD
days=($(seq -w 1 1 30))
months=($(seq -w 4 1 5))
echo ${months[@]}
for year in 2012;do
  for month in 07; do
    for day in 01; do
	  cd $wrkdir/$year/$month/$day/
      for init in `seq -w 0 3 21`; do
	  cd $init
      [ ! -f logfiles.tar ] && ecp ec:/suza/harmonie/JB_CARRA_alpha2_$year/$year/$month/$day/$init/logfiles.tar .
      tar xvf logfiles.tar 
      cd -
    #done #mem
      done #init
    done #day	    
  done #month
done #year
