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

#Function to calculate consumption cost
def calc_consump_cost(df_consump,x1,y1,x2,y2,consum_id):
    from helper.interpolate import cost_consump
    consump_cost = copy.deepcopy(df_consump)
    
    for key in Years:       
        consump_cost[key] = df_consump[key].applymap(lambda x: cost_consump(x,x1,y1,x2,y2))
        
    return consump_cost

#Function to calculate demand capacity of charging and discharging battery
def calc_capacity(df_cleaned,avg_consump):
#from helper.calc import *
    capacity = {'2010':{},'2011':{},'2012':{}}
    df_capacity = {}
    df_interval=calc_night_interval(df_cleaned)
    df_vol_dschg=calc_vol_dschg(df_cleaned)
    df_consump=calc_consump(df_cleaned)

    for key in Years:
        capacity[key]=df_consump[key].sum(axis=1)
        df_capacity[key] = pd.DataFrame({'Total Consumption' : capacity[key]})
        df_capacity[key]['Capacity'] = df_vol_dschg[key].apply(lambda x: x - avg_consump).sum(axis=1)
        df_capacity[key]['Demand at Night'] = df_cleaned['GC'][key].where(df_cleaned['GG'][key]==0).fillna(0).sum(axis=1)
        df_capacity[key]['Demand at Day'] = df_cleaned['GC'][key].where(df_cleaned['GG'][key]>0).fillna(0).sum(axis=1)
        df_capacity[key]['Periodic Demand at Night'] = df_capacity[key]['Demand at Night']/df_interval[key]['Night intervals'] 
        df_capacity[key]['Periodic Demand at Day'] = df_capacity[key]['Demand at Day']/df_interval[key]['Day intervals']
        df_capacity[key]=df_capacity[key].fillna(0)
        
    return df_capacity
