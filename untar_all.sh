#!/bin/bash
echo "Doing date 2012/07/01"
#for mem in 000 001 002 003 004 005 006 007 008 009; do
for mem in 002 003 004 005 006 007 008 009; do
    echo "Doing member $mem"
    cd ./mbr$mem
    tar xvf odb_stuff.tar
    tar xvf odb_ccma.tar
    cd odb_ccma/CCMA
    dcagen
    cd ../../
    rm -f bdstrategy odb.tar odb_can.tar odb_can_merge.tar odb_can_ori.tar odb_ccma.tar odbvar.tar
    cd ../
done
#ecp ec:/suza/harmonie/JB_CARRA_alpha2_2012/2012/07/01/00/mbr001/odb_stuff.tar ./mbr001
#ecp ec:/suza/harmonie/JB_CARRA_alpha2_2012/2012/07/01/00/mbr000/odb_stuff.tar ./mbr000

