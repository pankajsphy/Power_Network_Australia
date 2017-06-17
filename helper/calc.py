import pandas as pd
import copy
import pickle

Years=['2010','2011','2012']

#Function to calculate volume discharge
def calc_vol_dschg(df_cleaned):
    df_vol_dschg = {}
    for key in Years:
        df_vol_dschg[key] =   df_cleaned['GC'][key].iloc[:,:] \
                            + df_cleaned['CL'][key].iloc[:,:] \
                            - df_cleaned['GG'][key].iloc[:,:]
    return df_vol_dschg

#Function to calculate consumption
def calc_consump(df_cleaned):
    df_consump = {}
    for key in Years:
        df_consump[key] = df_cleaned['GC'][key].iloc[:,:] + df_cleaned['CL'][key].iloc[:,:]
    return df_consump

#Function to calculate Night intervals
def calc_night_interval(df_cleaned):
    Night_interval={'2010':{},'2011':{},'2012':{}}
    df_interval={}

    for key in Years:
        for i,day in enumerate(df_cleaned['GG'][key].index):
            Night_interval[key][day] = df_cleaned['GG'][key].iloc[i,:].value_counts()[0]
        df_interval[key] = pd.DataFrame({'Night intervals' : Night_interval[key]})  
        df_interval[key]['Day intervals'] = df_interval[key].apply(lambda x: 48 - df_interval[key]['Night intervals'])
    return df_interval

def calc_consump_cost(df_consump,df_loss_peak,df_loss_off_peak,df_loss_peak_geom,consum_id):
    from helper.interpolate import cost_consump
    consump_cost = copy.deepcopy(df_consump)
    consump_cost_geom = copy.deepcopy(df_consump)
    pkl_path='/home/pankaj/Documents/Ashruf/data/pickles/'
    
    for key in Years:
        pkl_name=pkl_path + 'cost_' + key + '_' + str(consum_id) + '.pkl'        
#        pkl_name_2=pkl_path + 'cost_geom_' + key + '_' + str(consum_id) + '.pkl'        
        
        consump_cost[key] = df_consump[key].applymap(lambda x: cost_consump(x,df_loss_peak,df_loss_off_peak))
#        consump_cost_geom[key] = df_consump[key].applymap(lambda x: cost_consump(x,df_loss_peak_geom,df_loss_off_peak))
        
        consump_cost[key].to_pickle(pkl_path+'cost_1.pkl',compression="gzip")        

#        consump_cost_geom[key].to_pickle('cost_geom_1.pkl',compression="gzip")                
    return None


