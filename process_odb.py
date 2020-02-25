import pandas as pd
import math
#data for control run
data0=pd.read_csv('mbr000/odb_ccma/CCMA/obs_1_11_1.dat',sep=' ')
Rast=data['an_depar@body']*data['fg_depar@body']
Rast_mean=Rast.mean()
error = math.sqrt(Rast_mean)
fg2=data['fg_depar@body']*data['fg_depar@body'] # (O - fg)^2
#note (O-fg)^2 = B_err^2 + obs_error^2
fg2m = fg2.mean()
obs_error_mean = data['obs_error@errstat'].mean()

mems=[str(i).zfill(3) for i in range(1,10)]
fg_ctrl_mean = data0['fg_depar@body'].mean()
#statid@hdr varno@body vertco_reference_1@body obsvalue@body an_depar@body fg_depar@body obs_error@errstat

#varno@body vertco_reference_1@body obsvalue@body an_depar@body fg_depar@body obs_error@errstat

for station in 
for mem in mems:
    ifile=os.path.join('mbr'+mem+'/odb_ccma/CCMA/','mbr'+mem+'_obs_1_11_1.dat')
    data = pd.read_csv(ifile,sep=' ')
    fg_mem = data['fg_depar@body'].mean()
    fg_ctrl_mem = (fg_ctrl_mean - mean()*fg_mean)**2
