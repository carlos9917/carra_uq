#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.out
#SBATCH --job-name=2012070921

#go through all members for a given date and fetch
#the odb data and untar it, create odb tables with dcgen

module load odb
module load python3
dom=West
#East: /suza/harmonie/JB_CARRA_alpha2_2012
origin=/nhe/harmonie/rc3_IGB_brand/
wrkdir=$PWD/$dom
days=($(seq -w 5 1 11))
days=(09)
#months=($(seq -w 4 1 5))
#echo ${months[@]}
for year in 2012;do
  for month in 07; do
    #for day in `seq -w 1 1 30`; do
    for day in ${days[@]}; do
      #for init in `seq -w 0 3 21`; do
      #for init in 12 15 18 21; do
      #for init in 09 12 15 18 21; do
      #for init in `seq -w 6 21`; do
      for init in 21; do
	    for mem in 000 001 002 003 004 005 006 007 008 009; do
	      dir=$wrkdir/$year/$month/$day/$init/mbr$mem
          [ ! -d $dir ] && mkdir -p $dir
          echo "Fetching data for $dir"    
	      cd $dir
          [ ! -f odb_stuff.tar ] && ecp ec:$origin/$year/$month/$day/$init/mbr$mem/odb_stuff.tar .
          echo "untar"
          tar xvf odb_stuff.tar
          tar xvf odb_ccma.tar
          cd odb_ccma/CCMA
          #mkdir -p odb_ccma/CCMA
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
