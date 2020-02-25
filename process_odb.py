#Read data from all the ensemble members
#and calculate the differences
# (f - o)^2 using the first guest departures

import pandas as pd
import math
#data for control run
data0=pd.read_csv('mbr000/odb_ccma/CCMA/obs_1_11_1.dat',sep=' ')
#some extra calcs 
#Rast=data['an_depar@body']*data['fg_depar@body']
#Rast_mean=Rast.mean()
#error = math.sqrt(Rast_mean)
#fg2=data['fg_depar@body']*data['fg_depar@body'] # (O - fg)^2
#note (O-fg)^2 = B_err^2 + obs_error^2
#fg2m = fg2.mean()
#obs_error_mean = data['obs_error@errstat'].mean()

mems=[str(i).zfill(3) for i in range(1,10)]
fg_ctrl_mean = data0['fg_depar@body'].mean()
#header of the form:
#statid@hdr varno@body vertco_reference_1@body obsvalue@body an_depar@body fg_depar@body obs_error@errstat

for station in data0['statid@hdr'].values:
    print("Going through station %d"%station)
    for mem in mems:
        ifile=os.path.join('mbr'+mem+'/odb_ccma/CCMA/','mbr'+mem+'_obs_1_11_1.dat')
        data = pd.read_csv(ifile,sep=' ')
        mem_sel = data[data['statid@hdr'] == station]
        if not mem_sel.empty:
            print("Station found in member %d"%mem)
            fg_mem_mean = mem_sel['fg_depar@body'].mean()
            diff2 = (fg_ctrl_mean - fg_mem_mean)**2
        #fg_ctrl_mem = (fg_ctrl_mean - mean()*fg_mean)**2
