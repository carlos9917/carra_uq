import sys
from itertools import islice

obs_code={}
searchfile = open("./uq_data/HM_Date_2012070100.html", "r")
for line in searchfile:
    if ('Obstype     ') in line: 
        #the following line will store the next two lines in a list
        #the first element will be the line ------
        next_two=list(islice(searchfile, 2))
        obstype = line.split()[1]
        if 'Codetype' in next_two[1]:
            #print(line)
            #print(next_two[1])
            #print(next_two[1].split())
            codetype=next_two[1].split()[1]
            #print("Obstype: %s Codetype: %s"%(obstype,codetype))
            obs_code[obstype]=codetype
        #print(list(islice(searchfile, 2))[1])
        #print(list(islice(searchfile, 4))[-1])
        #sys.exit()
        #for _ in range(2):
        #    print(searchfile.readline())
searchfile.close()
#print(obs_code)

#commands to call
import subprocess
for oc in obs_code.keys():
    cmd='''odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == '''+oc+''' AND codetype == '''+obs_code[oc]+''' AND varno == 1" |sed "s/'//g" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat'''
    #ret=subprocess(cmd,shell=True)
    print(cmd)
