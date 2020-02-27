#Read data from all the ensemble members
#and calculate the differences
# (f - o)^2 using the first guest departures

import pandas as pd
import math
import os
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
def calc_one_init():
    data0=pd.read_csv('mbr000/odb_ccma/CCMA/obs_1_11_1.dat',sep=' ')
    mems=[str(i).zfill(3) for i in range(1,10)]
    fg_ctrl_mean = data0['fg_depar@body'].mean()
    for k,station in enumerate(data0['statid@hdr']):
        print("Going through station %d"%station)
        fg_ctrl = data0['fg_depar@body'].values[k]
        diff2_station = 0
        for mem in mems:
            ifile=os.path.join('mbr'+mem+'/odb_ccma/CCMA/','mbr'+mem+'_obs_1_11_1.dat')
            data = pd.read_csv(ifile,sep=' ')
            #select only the station in member which matches station in control run list
            mem_sel = data[data['statid@hdr'] == station]
            if not mem_sel.empty:
                print("Station found in member %s"%mem)
                #fg_mem_mean = mem_sel['fg_depar@body'].mean()
                fg_mem = mem_sel['fg_depar@body']
                diff2 = (fg_ctrl - fg_mem)**2
                diff2_station += diff2
                #print("Difference squared %g"%diff2)
                #diff2 = (fg_ctrl_mean - fg_mem_mean)**2
            #fg_ctrl_mem = (fg_ctrl_mean - mean()*fg_mean)**2
        diff_total = diff2_station/len(mems)    
        print("Total difference for station %d: %g"%(station,diff_total))
def calc_all_init():
    init_times=[str(i).zfill(2) for i in range(0,22,3)]
    for init in init_times:
        data0=pd.read_csv(os.path.join(init,'mbr000/odb_ccma/CCMA/mbr000_obs_1_11_1.dat'),sep=' ')
        mems=[str(i).zfill(3) for i in range(1,10)]
        fg_ctrl_mean = data0['fg_depar@body'].mean()
        for k,station in enumerate(data0['statid@hdr']):
            print("Going through station %d"%station)
            fg_ctrl = data0['fg_depar@body'].values[k]
            diff2_station = 0
            for mem in mems:
                ifile=os.path.join('mbr'+mem+'/odb_ccma/CCMA/','mbr'+mem+'_obs_1_11_1.dat')
                data = pd.read_csv(ifile,sep=' ')
                #select only the station in member which matches station in control run list
                mem_sel = data[data['statid@hdr'] == station]
                if not mem_sel.empty:
                    print("Station found in member %s"%mem)
                    fg_mem = mem_sel['fg_depar@body']
                    diff2 = (fg_ctrl - fg_mem)**2
                    diff2_station += diff2
            diff_total = diff2_station/len(mems)    
            print("Total difference for station %d: %g"%(station,diff_total))
def calc_all_init():

if __name__=='__main__':

