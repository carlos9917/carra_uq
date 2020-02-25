import pandas as pd
data0=pd.read_csv('obs_1_11_1.dat',sep=' ')
Rast=data['an_depar@body']*data['fg_depar@body']
import math
Rast_mean=Rast.mean()
error = math.sqrt(Rast_mean)
fg2=data['fg_depar@body']*data['fg_depar@body'] # (O - fg)^2
#note (O-fg)^2 = B_err^2 + obs_error^2
fg2m = fg2.mean()
obs_error_mean = data['obs_error@errstat'].mean()

mems=[str(i).zfill(3) for i in range(1,10)]
fg_ctrl_mean = data0['fg_depar@body'].mean()
for mem in mems:
    ifile=os.path.join('mbr'+mem+'/odb_ccma/CCMA/','mbr'+mem+'_obs_1_11_1.dat')
    data = pd.read_csv(ifile,sep=' ')
    fg_mem = data['fg_depar@body'].mean()
    fg_ctrl_mem = (fg_ctrl_mean - mean()*fg_mean)**2
