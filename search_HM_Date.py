#Crude script to generate the sql commands to call
#all different variables available in the HM_Date files
import sys
import os
from itertools import islice
import numpy as np
from collections import OrderedDict
import pandas as pd

def search_all_init(fdate):
    '''
    Search in all the HM_Date* file for this date
    '''
    init_times=[str(i).zfill(2) for i in range(0,22,3)]
    obs_types={} #store obs_types for each file
    all_data = OrderedDict() #store all data
    for init in init_times:
        yyyymmddii='/'.join([fdate,init])
        print("searching %s"%yyyymmddii)
        fname=os.path.join(yyyymmddii,"HM_Date_"+yyyymmddii.replace('/','')+".html")
        obs_types[yyyymmddii],all_data[yyyymmddii]=search_single(fname)
    return obs_types,all_data

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
    #this line indicates the end of a section with usable data
    end_line='----------   ---------------------------   --------'
    #all text should be searched between these two:
    beg_string="Diagnostic JO-table (JOT) MINIMISATION JOB"
    end_string="Jo Global :"
    #begin and end of a section containing Variables information:
    var_head = "Variable"
    var_tail = "Codetype"
    obs_types={}
    all_data=OrderedDict()
    stringsAvoid=['Variable','Codetype', 'Obstype',end_line]
    #Will attempt to store all variables here
    for var in ['Obstype','Codetype', 'Variable']: #, 'DataCount', 'Jo_Costfunction', 'JO/n', 'ObsErr','BgErr']:
        all_data[var]=np.array([])

    searchfile = open(sfile,"r") #"./uq_data/HM_Date_2012070100.html", "r")
    inRecordingMode = False
    relevantSection = False
    saveVar = False
    lines_saved=[]
    for line in searchfile:
        #Include only the variables found in this section
        if beg_string in line:
            relevantSection = True
            #print("Begin section search")
            #print(line)
        elif end_string in line:
            relevantSection = False
            #print("End section search")
            #print(line)

        #save all vars in relevant section
        if relevantSection and var_head in line:
            saveVar = True
        elif var_tail in line:
            saveVar = False
        if ('Obstype     ') in line and relevantSection:
            #print(line)
            obstype = line.split()[1]
            next_two=list(islice(searchfile,2))
            #print(next_two)
            if 'Codetype' in next_two[1]:
                #print("creating array")
                #save the next lines until it hits the end_line
                inRecordingMode=True
                lines_saved=[]
        elif end_line in line:
            inRecordingMode=False

        if inRecordingMode and relevantSection:
            #if saveVar and 'Variable' not in line and 'Codetype' not in line and end_line not in line:
            if saveVar and not any(string in line for string in stringsAvoid):
                all_data['Obstype'] = np.append(all_data['Obstype'],obstype)
                all_data['Codetype'] = np.append(all_data['Codetype'],next_two[1].split()[1])
                output = [s.strip() for s in line.split('  ') if s]
                all_data['Variable'] = np.append(all_data['Variable'],output[0])
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
                    #all_data['Obstype']=np.append(all_data['Obstype'], obstype)
                elif 'Codetype' in l:  #store the Codetype(s) for this Obstype
                    #print(l)
                    codetype=l.split()[1]
                    obs_types[obstype]=np.append(obs_types[obstype],codetype)
                    #all_data['Codetype']=np.append(all_data['Codetype'], codetype)
                #else:
                #    all_data['Codetype']=np.append(all_data['Codetype'] = codetype)
                #    all_data['Obstype']=np.append(all_data['Obstype'] = obstype)
                #    print("check what comes next")
                #    print(l)
    searchfile.close()
    return obs_types,all_data

#commands to call
def run_sql(data,key_date):
    '''
    fnction assumes script sitting in top path of form YYYY/MM/DD/HH
    given by key_date
    '''
    import subprocess
    mems=[str(i).zfill(3) for i in range(1,10)]
    var_codes={'Z':1,'U':3,'T':2,'Q':7}
    cdir=os.getcwd()
    for mem in mems:
        os.chdir(os.path.join(key_date,"mbr"+mem))
        for k in data['Obstype'].index:
            obstype=str(data['Obstype'].loc[k])
            codetype=str(data['Codetype'].loc[k])
            varno=str(var_codes[data['Variable'].loc[k]])
            fstring='_'.join([obstype,codetype,varno])+'.dat'
            cmd='''odbsql -q "SELECT statid,varno,vertco_reference_1,obsvalue,an_depar,fg_depar,obs_error FROM hdr,body,errstat WHERE obstype == '''+obstype+''' AND codetype == '''+codetype+''' AND varno == '''+varno+ '''" |sed "s/'//g" | awk '{$2=$2};1' >& mbr'''+mem+fstring   #'''_obs_1_11_1.dat'''
            ret=subprocess(cmd,shell=True)
        os.chdir(cdir)

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
    #short test to carry out locally 
    #obs_types = search_single("uq_data/HM_Date_2012070100.html")
    #grab the observation codesarg for all files in this date
    obs_types,all_data = search_all_init(args.date)
    print("Obstype/Codetype pairs found in each file")
    for key in obs_types.keys():
        print(key)
        for ot_key in obs_types[key].keys():
            for ct in obs_types[key][ot_key][:]:
                print("Obstype: %s Codetype: %s"%(ot_key,ct))
        #print(obs_types[key])
    print("---------------------------")     
    print("Check all Obstype,Codetype,Variable combinations")
    for key in all_data.keys():
        #print only unique keys for this YYYYMMDDHH
        data=pd.DataFrame(all_data[key])
        data=data.drop_duplicates()
        print(data)
        print("Commands for %s"%key)
        run_sql(data,key)


