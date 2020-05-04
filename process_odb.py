#Read data from all the ensemble members
#and calculate the differences
# (f - o)^2 using the first guest departures

import pandas as pd
import math
import os
from collections import OrderedDict
#data for control run
#some extra calcs 
#Rast=data['an_depar@body']*data['fg_depar@body']
#Rast_mean=Rast.mean()
#error = math.sqrt(Rast_mean)
#fg2=data['fg_depar@body']*data['fg_depar@body'] # (O - fg)^2
#note (O-fg)^2 = B_err^2 + obs_error^2
#fg2m = fg2.mean()
#obs_error_mean = data['obs_error@errstat'].mean()

#print(data0.columns)
#header of the form:
#statid@hdr varno@body vertco_reference_1@body obsvalue@body an_depar@body fg_depar@body obs_error@errstat
#statid@hdr
def calc_one_init(fdate):
    '''NOTE: this function needs to be updated
       to reflect changes in output names. See calc_all_init below.
       Currently not using
    '''
    yyyymmddii='/'.join([fdate,'00'])
    data0=pd.read_csv(os.path.join(yyyymmddii,'mbr000/odb_ccma/CCMA/mbr000_obs_1_11_1.dat'),sep=' ')
    mems=[str(i).zfill(3) for i in range(1,10)]
    fg_ctrl_mean = data0['fg_depar@body'].mean()
    for k,station in enumerate(data0['statid@hdr']):
        #print("Going through station %d"%station)
        fg_ctrl = data0['fg_depar@body'].values[k]
        diff2_station = 0
        for mem in mems:
            ifile=os.path.join('mbr'+mem+'/odb_ccma/CCMA/','mbr'+mem+'_obs_1_11_1.dat')
            data = pd.read_csv(ifile,sep=' ')
            #select only the station in member which matches station in control run list
            mem_sel = data[data['statid@hdr'] == station]
            if not mem_sel.empty:
                #print("Station found in member %s"%mem)
                #fg_mem_mean = mem_sel['fg_depar@body'].mean()
                fg_mem = mem_sel['fg_depar@body']
                diff2 = (fg_ctrl - fg_mem)**2
                diff2_station += diff2
                #print("Difference squared %g"%diff2)
                #diff2 = (fg_ctrl_mean - fg_mem_mean)**2
            #fg_ctrl_mem = (fg_ctrl_mean - mean()*fg_mean)**2
        diff_total = diff2_station/len(mems)    
        print("Ensemble mean of (fg_ctrl - fg_mem)^2 for station %d and init 00: %g"%(station,diff_total))

def calc_all_init(fdate,obstype,codetype,varno,dom):
    obsCodeVar='_'.join([obstype,codetype,varno])
    init_times=[str(i).zfill(2) for i in range(0,22,3)]
    mems=[str(i).zfill(3) for i in range(1,10)]
    sdir="/scratch/ms/dk/nhd/carra_uq/"+dom
    count=0
    save_init=[];save_stations=[];save_diff2=[]
    save_fg_dep2=[];save_an_fg=[]
    for init in init_times:
        yyyymmddii='/'.join([fdate,init])
        check_file=os.path.join(sdir,yyyymmddii+'/mbr000/odb_ccma/CCMA/mbr000_'+obsCodeVar+'.dat')
        if os.path.isfile(check_file):
            print("Reading %s for init %s"%(check_file,init))
            data_ref=pd.read_csv(check_file,sep=' ')   
        else:
            print("Skipping %s for init %s, since file does not exist"%(check_file,init))
            continue
            
        for k,station in enumerate(data_ref['statid@hdr']):
            diff2_station=0
            fg_ctrl = data_ref['fg_depar@body'].values[k]
            an_fg_dep_ctrl = data_ref['an_depar@body'].values[k]*fg_ctrl
            for mem in mems:
                ifile=os.path.join(yyyymmddii,'mbr'+mem+'/odb_ccma/CCMA/mbr'+mem+'_'+obsCodeVar+'.dat')
                data = pd.read_csv(ifile,sep=' ')
                #select only the station in member which matches station in control run list
                mem_sel = data[data['statid@hdr'] == station]
                if not mem_sel.empty:
                    #print("Station %d found in member %s %s"%(station,yyyymmddii,mem))
                    fg_mem = mem_sel['fg_depar@body'].values[0]
                    diff2_station += (fg_ctrl - fg_mem)**2
                else:
                    print("Warning: NO data found for station in member %s %s"%(yyyymmddii,mem))
            save_init.append(init)    
            save_stations.append(station)
            save_diff2.append(diff2_station/len(mems))
            save_fg_dep2.append(fg_ctrl**2)
            save_an_fg.append(an_fg_dep_ctrl)
    diff2_init=pd.DataFrame({'station':save_stations,'init':save_init,'diff2':save_diff2})            
    fg_dep2_ctrl=pd.DataFrame({'station':save_stations,'init':save_init, 'fg_dep2':save_fg_dep2})
    an_fg_ctrl=pd.DataFrame({'station':save_stations,'init':save_init,'an_fg_dep':save_an_fg})
    if not diff2_init.empty and not fg_dep2_ctrl.empty and not an_fg_ctrl.empty:

        #Finally calculate mean of all init times for all stations that 
        #are present during the whole set of init times
        diff2_total=OrderedDict()
        total=0
        for station in diff2_init['station']:
            diff2_total[station] = diff2_init[diff2_init['station']==station]['diff2'].mean()
            #print(diff2_total[station]['diff2'])
            print("Ensemble mean of (fg_ctrl - fg_mem)^2 for station %s for all init times: %g"%(station,diff2_total[station]))
            total+=diff2_total[station] #not using this anywhere...
        print("mean of (fg_ctrl - fg_mem)^2 over all stations: %g"%diff2_init.diff2.mean())
        print("mean of fg_dep^2 for control run over all stations: %g"%fg_dep2_ctrl.fg_dep2.mean())
        print("mean of an_dep*fg_dep for control run over all stations: %g"%an_fg_ctrl.an_fg_dep.mean())
        #dg_dep2_ctrl[str(station)+'_'+init] = fg_ctrl**2
        print("-----------------")
        print("Stations summary ")
        print("total :%d"%diff2_init['station'].shape[0])
        print("-----------------")
        print("station        init  ")
        for k,station in enumerate(diff2_init['station']):
            print("%s %s"%(station,diff2_init['init'].values[k]))
    else:
        print("-------------------------")
        print("<---- NO DATA for %s ---->"%obsCodeVar)
        print("-------------------------")
    

def loop_ocv(oct_comb):
    '''
    Loop through all obstype,codetype and varno cobminations
    '''
    pass

if __name__=='__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description=''' Example usage: python3 process_odb.py -d 2019/03/26 ''',formatter_class=RawTextHelpFormatter)

    #default starting date is first day of simulations
    parser.add_argument('-d','--date',metavar='Date to process (YYYY/MM/DD)',
                        type=str,
                        default=None,
                        required=True)

    parser.add_argument('-ot','--obstype',metavar='Obstype grib code',
                        type=str,
                        default='1',
                        required=False)

    parser.add_argument('-ct','--codetype',metavar='Codetype grib code',
                        type=str,
                        default='11',
                        required=False)

    parser.add_argument('-vn','--varno',metavar='Variable grib code',
                        type=str,
                        default='1',
                        required=False)

    parser.add_argument('-dom','--domain',metavar='Domain',
                        type=str,
                        default='West',
                        required=False)

    args = parser.parse_args()
    codetype=args.codetype


    #print("----------------------------------------------------------------------------------------")
    #print("Calculating means for obstype == 1 AND codetype == 11 AND varno == 1 and init=00")
    #print("----------------------------------------------------------------------------------------")
    #calc_one_init(args.date) #'2012/07/01')

    print("----------------------------------------------------------------------------------------")
    print("Calculating means for obstype == %s AND codetype == %s AND varno == %s and all init times"%(args.obstype,args.codetype,args.varno))
    print("----------------------------------------------------------------------------------------")
    calc_all_init(args.date,args.obstype,args.codetype,args.varno,args.domain) #'2012/07/01')
    print("----- Done -----")
