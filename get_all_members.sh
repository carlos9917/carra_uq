#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/runout-%J.out
#SBATCH --job-name=fetchodb

#go through all members for a given date and fetch
#the odb data and untar it, create odb tables with dcgen

function call_odb ()
{
odbsql -q 'SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == $obstype AND codetype == $codetype AND varno == 1' |sed "s/'//g" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat
echo "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == $obstype AND codetype == $codetype AND varno == 1"
}

module load odb
wrkdir=$PWD
days=($(seq -w 1 1 30))
obs=(11 12 13)
months=($(seq -w 4 1 5))
echo ${months[@]}
for year in 2012;do
  for month in 07; do
    #for day in `seq -w 1 1 30`; do
    for day in 01; do
      for init in `seq -w 0 3 21`; do
	for mem in 000 001 002 003 004 005 006 007 008 009; do
      #echo "mkdir -p $year/$month/$day/$init"
	  dir=$wrkdir/$year/$month/$day/$init/mbr$mem
      [ ! -d $dir ] && mkdir -p $dir
      echo "Fetching data for $dir"    
	  cd $dir
      [ ! -f odb_stuff.tar ] && ecp ec:/suza/harmonie/JB_CARRA_alpha2_$year/$year/$month/$day/$init/mbr$mem/odb_stuff.tar .
      echo "untar"
      tar xvf odb_stuff.tar
      tar xvf odb_ccma.tar
      cd odb_ccma/CCMA
      #mkdir -p odb_ccma/CCMA
      echo "Generate odb tables"
      dcagen
      #echo $PWD
      cd -
      rm -f bdstrategy odb.tar odb_can.tar odb_can_merge.tar odb_can_ori.tar odb_ccma.tar odbvar.tar
      cd $wrkdir/$year/$month/$day/$init
      for obstype in ${obs[@]}; do
	      call_odb
      done
      #echo $PWD
	  #cd -
    done #mem

      done #init
    done #day	    
  done #month
done #year
