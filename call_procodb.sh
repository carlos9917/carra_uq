#!/bin/bash
#SBATCH --error=/scratch/ms/dk/nhd/carra_uq/out/procodb-%J.err
#SBATCH --output=/scratch/ms/dk/nhd/carra_uq/out/procodb-%J.out
#SBATCH --job-name=procodb

# seeing only these files with non zero content
#-rw-r-----.   1 nhd dk    1722 Mar  6 18:13 mbr000_1_11_1.dat
#-rw-r-----.   1 nhd dk    6080 Mar  6 18:13 mbr000_1_14_1.dat
#-rw-r-----.   1 nhd dk       0 Mar  6 18:13 mbr000_1_21_3.dat
#-rw-r-----.   1 nhd dk     277 Mar  6 18:13 mbr000_1_21_1.dat
#-rw-r-----.   1 nhd dk       0 Mar  6 18:13 mbr000_1_24_3.dat
#-rw-r-----.   1 nhd dk     221 Mar  6 18:13 mbr000_1_24_1.dat
#-rw-r-----.   1 nhd dk     199 Mar  6 18:13 mbr000_2_144_3.dat
#-rw-r-----.   1 nhd dk     189 Mar  6 18:13 mbr000_2_144_2.dat
#-rw-r-----.   1 nhd dk     450 Mar  6 18:13 mbr000_4_165_1.dat
#-rw-r-----.   1 nhd dk   39207 Mar  6 18:13 mbr000_5_35_3.dat
#-rw-r-----.   1 nhd dk   21150 Mar  6 18:14 mbr000_5_35_2.dat
#drwxr-x---. 219 nhd dk   16384 Mar  6 18:14 .
#-rw-r-----.   1 nhd dk   15946 Mar  6 18:14 mbr000_5_35_7.dat


#Adding these:


#call the process_odb.py script for all dates

module load python3
days=($(seq -w 1 1 11))
wrkdir=$PWD

#obstype,codetype and varno valid combinations
obstype=(1 1 1 1 2 2 4 5 5 5 5 5 5 2 2 2 2)
codetype=(11 14 21 24 144 144 165 35 35 35 36 36 36 142 142 144 144) 
varno=(1 1 1 1 3 2 1 3 2 7 2 3 7 2 3 2 3)
for year in 2012;do
  for month in 07; do
    for day in ${days[@]}; do
	    for i in "${!obstype[@]}"; do
            echo "Doing ${year}/$month/$day and ${obstype[i]} ${codetype[i]} ${varno[i]}"
            python3 process_odb.py -d "$year/$month/$day" -ot ${obstype[i]} -ct ${codetype[i]} -vn ${varno[i]} >& ./$year/$month/$day/summary_${obstype[i]}_${codetype[i]}_${varno[i]}.txt
            done
    done #day
   done #month
done #year
