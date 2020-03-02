#Crude script to generate the sql commands to call
#all different variables available in the HM_Date files
import sys
import os
from itertools import islice
import numpy as np

def search_all_init(fdate):
    '''
    Search in all the HM_Date* file for this date
    '''
    init_times=[str(i).zfill(2) for i in range(0,22,3)]
    obs_types={} #store obs_types for each file
    for init in init_times:
        yyyymmddii='/'.join([fdate,init])
        print("searching %s"%yyyymmddii)
        fname=os.path.join(yyyymmddii,"HM_Date_"+yyyymmddii.replace('/','')+".html")
        searchfile = open(fname, "r")
        obs_types[fname.replace(".html","")]=search_single(fname)
    return obs_types

def search_all_init_old(fdate):
    '''
    Search all Obstype/Codetype pairs in the HM_Date* file for this date.
    Print only non-repeated values
    '''
    init_times=[str(i).zfill(2) for i in range(0,22,3)]
    obs_code={}
    for init in init_times:
        yyyymmddii='/'.join([fdate,init])
        print("Date %s"%yyyymmddii)

        searchfile = open(os.path.join(yyyymmddii,"HM_Date_"+yyyymmddii.replace('/','')+".html"), "r")
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
    uniqueKeys = set(obs_code.keys())
    obs_code_clean={}
    for key in uniqueKeys:
        obs_code_clean[key] = obs_code[key]

    return obs_code_clean

def search_single_old():
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
    return obs_code

def search_single(sfile):
    end_line='----------   ---------------------------   --------'
    obs_types={}
    searchfile = open(sfile,"r") #"./uq_data/HM_Date_2012070100.html", "r")
    inRecordingMode=False
    lines_saved=[]
    for line in searchfile:
        if ('Obstype     ') in line:
            #print("found one")
            next_two=list(islice(searchfile,2))
            #print(next_two)
            if 'Codetype' in next_two[1]:
                #print("creating array")
                #save the next lines until it hits the end_line
                inRecordingMode=True
                lines_saved=[]
        elif end_line in line:
            inRecordingMode=False

        if inRecordingMode:
            #print("recording")
            lines_saved.append(line)
            if len(lines_saved) == 1:
                lines_saved.append(next_two[0])
                lines_saved.append(next_two[1])
            #the following line will store the next two lines in a list
            #the first element will be the line ------
        if not inRecordingMode and len(lines_saved) > 0:
            #print("checking lines")
            for l in lines_saved:
                if 'Obstype' in l: # create array to store all Codetype(s) for this Obstype
                    obstype=l.split()[1]
                    obs_types[obstype] = np.array([])
                if 'Codetype' in l:  #store the Codetype(s) for this Obstype
                    codetype=l.split()[1]
                    obs_types[obstype]=np.append(obs_types[obstype],codetype)
    searchfile.close()
    return obs_types

#commands to call
def run_sql():
    import subprocess
    for oc in obs_code.keys():
        cmd='''odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == '''+oc+''' AND codetype == '''+obs_code[oc]+''' AND varno == 1" |sed "s/'//g" | awk '{$2=$2};1' >& mbr${mem}_obs_1_11_1.dat'''
        ret=subprocess(cmd,shell=True)
        #print(cmd)

if __name__=='__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description=''' Example usage: python3 process_odb.py -d 2019/03/26 ''',formatter_class=RawTextHelpFormatter)

    #default starting date is first day of simulations
    parser.add_argument('-d','--date',metavar='Date to process (YYYY/MM/DD)',
                        type=str,
                        default=None,
                        required=True)

    args = parser.parse_args()
    #grab the observation codesarg for all files in this date
    obs_types = search_all_init(args.date)
    print("Obstype/Codetype pairs found in each file")
    for key in obs_types.keys():
        print(obs_types[key])

