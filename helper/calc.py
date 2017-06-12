#Function to calculate volume discharge
def dch_vol(df_GC,df_CL,df_GG,x):
    return df_GC[x] + df_CL[x] - df_GG[x] 

#Function to calculate volume discharge
def consump(df_GC,df_CL,x):
    return df_GC[x] + df_CL[x]  

#Function to evaluate staus whether peak, off-peak or average
def status(disch_vol):
    Avg_Consumption = [0.35, 0.45]; #in kWh 

    if discharge_volume > Avg_Consumption[1]:
        State = 'Peak'       
    elif discharge_volume < Avg_Consumption[0]:    
        State = 'Off-Peak'
    elif discharge_volume > Avg_Consumption[0] and discharge_volume < Avg_Consumption[1]:
        State = 'Average'
    return State    
