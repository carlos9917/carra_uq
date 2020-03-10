#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/logsout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/logsout-%J.out
#SBATCH --job-name=fetchlogs

#retrieve all the logfiles from ecfs. Extract the HM_Date files

wrkdir=$PWD
days=($(seq -w 4 1 11))
months=($(seq -w 4 1 5))
echo ${months[@]}
for year in 2012;do
  for month in 07; do
    for day in ${days[@]}; do
	  cd $wrkdir/$year/$month/$day/
      for init in `seq -w 0 3 21`; do
	  cd $init
      [ ! -f logfiles.tar ] && ecp ec:/suza/harmonie/JB_CARRA_alpha2_$year/$year/$month/$day/$init/logfiles.tar .
      tar xvf logfiles.tar 
      rm -f logfiles.tar
      cd -
    #done #mem
      done #init
    done #day	    
  done #month
done #year
