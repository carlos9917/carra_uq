#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/odbsql-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/odbsql-%J.out
#SBATCH --job-name=runodbsql

#call the process_odb.py script for all dates

module load python3
days=($(seq -w 2 1 11))
wrkdir=$PWD
obstype=(1 2 3 )
for year in 2012;do
  for month in 07; do
    for day in ${days[@]}; do
      python3 search_HM_Date.py -d "$year/$month/$day" >& ./$year/$month/$day/summary.txt
    done #day
   done #month
done #year
