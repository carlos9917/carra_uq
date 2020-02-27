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

def calc_all_init(fdate):

    init_times=[str(i).zfill(2) for i in range(0,22,3)]
    mems=[str(i).zfill(3) for i in range(1,10)]

    #for k,station in enumerate(data_ref['statid@hdr']):
    #    print("Going through station %d"%station)
    #    diff2_station = 0
    #for init in init_times:
    #diff2_init={} #store all the differences for a particular init time
    #diff2_save={}
    count=0
    save_init=[];save_stations=[];save_diff2=[]
    save_fg_dep2=[];save_an_fg=[]
    #fg_dep2_ctrl={}
    for init in init_times:
        yyyymmddii='/'.join([fdate,init])
        data_ref=pd.read_csv(os.path.join(yyyymmddii,'mbr000/odb_ccma/CCMA/mbr000_obs_1_11_1.dat'),sep=' ')   
        for k,station in enumerate(data_ref['statid@hdr']):
            diff2_station=0
            fg_ctrl = data_ref['fg_depar@body'].values[k]
            an_fg_dep_ctrl = data_ref['an_depar@body'].values[k]*fg_ctrl
            #diff2_save[str(station)]=fg_ctrl**2
            #if k==0 and init=='00':
            #    fg_dep2_ctrl=pd.DataFrame({'station':station,'init':init,'fg_dep2':fg_ctrl**2},index=[count])
            #    an_fg_ctrl=pd.DataFrame({'station':station,'init':init,'an_fg_dep':an_fg_dep_ctrl},index=[count])
            #else:        
            #    count+=1
            #    add_data=pd.DataFrame({'station':station,'init':init,'fg_dep2':fg_ctrl**2},index=[count])
            #    fg_dep2_ctrl=fg_dep2_ctrl.append(add_data,ignore_index=True)
            #    add_data=pd.DataFrame({'station':station,'init':init,'an_fg_dep':an_fg_dep_ctrl},index=[count])
            #    an_fg_ctrl=an_fg_ctrl.append(add_data,ignore_index=True)
            for mem in mems:
                ifile=os.path.join(yyyymmddii,'mbr'+mem+'/odb_ccma/CCMA/mbr'+mem+'_obs_1_11_1.dat')
                data = pd.read_csv(ifile,sep=' ')
                #select only the station in member which matches station in control run list
                mem_sel = data[data['statid@hdr'] == station]
                if not mem_sel.empty:
                    #print("Station %d found in member %s %s"%(station,yyyymmddii,mem))
                    fg_mem = mem_sel['fg_depar@body'].values[0]
                    diff2_station += (fg_ctrl - fg_mem)**2
                else:
                    print("Warning: NO data found for station in member %s %s"%(yyyymmddii,mem))
            #diff2_init[station+'_'+init] = diff2_station/len(mems)    
            #if init == '00' and k==0: # create dataframe
            #    print("First data frame created (this should only happen once!!!)")
            #    diff2_init=pd.DataFrame({'station':station,'init':init,'diff2':diff2_station/len(mems)})
            #else:
            #    add_data=pd.DataFrame({'station':station,'init':init,'diff2':diff2_station/len(mems)})
            #    diff2_init = diff2_init.append(add_data,ignore_index=True)
            save_init.append(init)    
            save_stations.append(station)
            save_diff2.append(diff2_station/len(mems))
            save_fg_dep2.append(fg_ctrl**2)
            save_an_fg.append(an_fg_dep_ctrl)
    diff2_init=pd.DataFrame({'station':save_stations,'init':save_init,'diff2':save_diff2})            
    fg_dep2_ctrl=pd.DataFrame({'station':save_stations,'init':save_init, 'fg_dep2':save_fg_dep2})
    an_fg_ctrl=pd.DataFrame({'station':save_stations,'init':save_init,'an_fg_dep':save_an_fg})
    #print("Total difference for station %d at init time %s: %g"%(station,init,diff_total))
    #finally calculate mean of all init times for all stations that 
    #are present during the whole set of init times
    #fp_dep2_ctrl=pd.DataFrame({'station':data_ref['statid@hdr'],
    #                           'init':
    diff2_total=OrderedDict()
    total=0
    for station in diff2_init['station']:
        diff2_total[station] = diff2_init[diff2_init['station']==station]['diff2'].mean()
        #print(diff2_total[station]['diff2'])
        print("Ensemble mean of (fg_ctrl - fg_mem)^2 for station %d for all init times: %g"%(int(station),diff2_total[station]))
        total+=diff2_total[station]
    print("mean of (fg_ctrl - fg_mem)^2 over all stations: %g"%diff2_init.diff2.mean())
    print("mean of fg_dep^2 for control run over all stations: %g"%fg_dep2_ctrl.fg_dep2.mean())
    print("mean of an_dep*fg_dep for control run over all stations: %g"%an_fg_ctrl.an_fg_dep.mean())
    #dg_dep2_ctrl[str(station)+'_'+init] = fg_ctrl**2
if __name__=='__main__':
    print("----------------------------------------------------------------------------------------")
    print("Calculating means for obstype == 1 AND codetype == 11 AND varno == 1 and init=00")
    print("----------------------------------------------------------------------------------------")
    calc_one_init('2012/07/01')
    print("----------------------------------------------------------------------------------------")
    print("Calculating means for obstype == 1 AND codetype == 11 AND varno == 1 and all init times")
    print("----------------------------------------------------------------------------------------")
    calc_all_init('2012/07/01')
