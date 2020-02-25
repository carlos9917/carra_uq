#!/bin/bash
echo "Doing date 2012/07/01"
#for mem in 000 001 002 003 004 005 006 007 008 009; do
for mem in 002 003 004 005 006 007 008 009; do
    [ ! -d mbr$mem ] && mkdir mbr$mem
    ecp ec:/suza/harmonie/JB_CARRA_alpha2_2012/2012/07/01/00/mbr001/odb_stuff.tar ./mbr$mem
done
#ecp ec:/suza/harmonie/JB_CARRA_alpha2_2012/2012/07/01/00/mbr001/odb_stuff.tar ./mbr001
#ecp ec:/suza/harmonie/JB_CARRA_alpha2_2012/2012/07/01/00/mbr000/odb_stuff.tar ./mbr000

