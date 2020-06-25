#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.out
#SBATCH --job-name=2017011021

#go through all members for a given date and fetch
#the odb data and untar it, create odb tables with dcgen

module load odb
module load python3
dom=West
#East: /suza/harmonie/JB_CARRA_alpha2_2012 Summer
#      origin=/suza/harmonie/JB_CARRA_alpha2 #winter 201701
# West:
origin=/nhx/harmonie/beta2_IGB_brand/ #winter 201701. NOTE: ectmp, not ec
#origin=/nhe/harmonie/rc3_IGB_brand/ Summer, 201207
wrkdir=$PWD/$dom
days=($(seq -w 1 1 11))
days=(10)
#months=($(seq -w 4 1 5))
#echo ${months[@]}
for year in 2017;do
  for month in 01; do
    #for day in `seq -w 1 1 30`; do
    for day in ${days[@]}; do
      #for init in `seq -w 0 3 21`; do
      #for init in `seq -w 6 21`; do
      #for init in 06 09 12 15 18 21; do
      #for init in 12 15 18 21; do
      for init in 21; do
	    for mem in 004 005 006 007 008 009; do
	    #for mem in 000 001 002 003 004 005 006 007 008 009; do
	    #for mem in 004 005 006 007 008 009; do
	      dir=$wrkdir/$year/$month/$day/$init/mbr$mem
          [ ! -d $dir ] && mkdir -p $dir
          echo "Fetching data for $dir"    
	      cd $dir
          [ ! -f odb_stuff.tar ] && ecp ectmp:$origin/$year/$month/$day/$init/mbr$mem/odb_stuff.tar .
          echo "untar"
          tar xvf odb_stuff.tar
          tar xvf odb_ccma.tar
          cd odb_ccma/CCMA
          #mkdir -p odb_ccma/CCM2
          echo "Generate odb tables"
          dcagen
          #echo $PWD
          cd -
          rm -f bdstrategy odb.tar odb_can.tar odb_can_merge.tar odb_can_ori.tar odb_ccma.tar odbvar.tar odb_stuff.tar
          cd $wrkdir/$year/$month/$day/$init
          #echo $PWD
	  #cd -
        done #mem

      done #init
    done #day	    
  done #month
done #year
