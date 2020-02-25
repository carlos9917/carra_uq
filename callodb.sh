#module load odb
for mem in 001 002 003 004 005 006 007 008 009; do
#for mem in 001; do 
    echo "Doing member $mem"
    cd mbr$mem/odb_ccma/CCMA/
    #odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == 1 AND codetype == 11 AND varno == 1" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat 
    #odbsql -q "SELECT varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == 1 AND codetype == 11 AND varno == 1" | awk '{$2=$2};1' | sed "s/'//g" >& mbr${mem}_obs_1_11_1.dat 
    #odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == 1 AND codetype == 11 AND varno == 1" -o test.dat 
    #sed -i "s/'//g" test.dat
    odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == 1 AND codetype == 11 AND varno == 1" |sed "s/'//g" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat 
    #sed -i '1s/^/#/' mbr${mem}_obs_1_11_1.dat
    cd -
done
