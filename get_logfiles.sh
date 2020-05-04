#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/logsout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/logsout-%J.out
#SBATCH --job-name=fetchlogs

#retrieve all the logfiles from ecfs. Extract the HM_Date files
dom=West
wrkdir=$PWD/$dom
#East: /suza/harmonie/JB_CARRA_alpha2_2012 #summer
#origin=/nhe/harmonie/rc3_IGB_brand/ #West summer
origin=/nhx/harmonie/beta2_IGB_brand/ #West winter. NOTE: use ectmp
#origin=/suza/harmonie/JB_CARRA_alpha2 #East winter
days=($(seq -w 1 1 11))
#months=($(seq -w 4 1 5))
echo ${months[@]}
for year in 2017;do
  for month in 01; do
    for day in ${days[@]}; do
	  cd $wrkdir/$year/$month/$day/
      for init in `seq -w 0 3 21`; do
	  cd $init
      [ ! -f logfiles.tar ] && ecp ectmp:${origin}/$year/$month/$day/$init/logfiles.tar .
      tar xvf logfiles.tar 
      rm -f logfiles.tar
      cd -
    #done #mem
      done #init
    done #day	    
  done #month
done #year
