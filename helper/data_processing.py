import pandas as pd
import numpy as np
import pickle
import gzip
import copy

def clean_data(fname,consum_id):

    Years=['2010','2011','2012']
    Category=['GG','GC']
    df={}
    df1={'GG':{},'GC':{},'CL':{}}
    pkl_path='/home/pankaj/Documents/Ashruf/data/pickles/'
    pkl_name='df_cleaned_%d.pklz'%consum_id
    
    cols=[x for x in range(2,52)]
    
    for key in Years:
    
	    df[key] = pd.read_csv(fname[key][consum_id], skiprows=2, header=None, usecols=cols, 
	                        dayfirst=True, parse_dates=[3],index_col=1).fillna(0.0)
	    df[key].index.names=['Date']
	    df[key] = df[key].rename(columns = {0:"Customer",1:"Generator_Capacity",2:'Consumption_Category',
	                                    3:'Date',4:'00:00',5:'00:30',6:'01:00',7:'01:30',8:'02:00', 
	                                    9:'02:30',10:'03:00',11:'03:30',12:'04:00',13:'04:30',14:'05:00',
	                                    15:'05:30',16:'06:00',17:'06:30',18:'07:00',19:'07:30',20:'08:00',
	                                    21:'08:30',22:'09:00',23:'09:30',24:'10:00',25:'10:30',26:'11:00',
	                                    27:'11:30',28:'12:00',29:'12:30',30:'13:00',31:'13:30',32:'14:00',
	                                    33:'14:30',34:'15:00',35:'15:30',36:'16:00',37:'16:30',38:'17:00',
	                                    39:'17:30',40:'18:00',41:'18:30',42:'19:00',43:'19:30',44:'20:00',
	                                    45:'20:30',46:'21:00',47:'21:30',48:'22:00',49:'22:30',50:'23:00',
	                                    51:'23:30'})
    
	    for cat in Category:
	        df1[cat][key]=df[key].loc[df[key].iloc[:,0]==cat]
	        df1[cat][key]=df1[cat][key].drop(['Consumption_Category'],axis=1)
	        df1[cat][key]=df1[cat][key].applymap(lambda x: float(x))

	    if df[key].iloc[1,0]=='CL':
	        df1['CL'][key]=df[key].loc[df[key].iloc[:,0]=='CL']
	        df1['CL'][key]=df1['CL'][key].drop(['Consumption_Category'],axis=1)
	        df1['CL'][key]=df1['CL'][key].applymap(lambda x: float(x))
	    else:
	        df1['CL'][key]=copy.deepcopy(df1['GC'][key])
	        df1['CL'][key]=df1['CL'][key].apply(lambda x: x*0.0)

    to_pklz(df1,pkl_path,pkl_name)
    return None

#---------------------------------------------------------------------------------
def make_clean_df_dict(consum_id):
    df_cleaned={'GG':{},'GC':{},'CL':{}}
    Category=['GG','GC','CL']
    Years=['2010','2011','2012']
    pkl_path='/home/pankaj/Documents/Ashruf/data/pickles/'

    for cat in Category:
        for key in Years:
            pkl_name=pkl_path + cat +'_' + key + '_' + str(consum_id) + '.pkl'
            df_cleaned[cat][key]=pd.read_pickle(pkl_name,compression="gzip")
    return df_cleaned
#----------------------------------------------------------------------------------
def to_pklz(df,pkl_path,pkl_name):
    f = gzip.open(pkl_path + pkl_name,'wb')
    pickle.dump(df,f)
    f.close()
#----------------------------------------------------------------------------------
def from_pklz(pkl_path,pkl_name):
	f = gzip.open(pkl_path+pkl_name,'rb')
	df = pickle.load(f)
	f.close()
	return df
