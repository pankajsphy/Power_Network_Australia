def interpol(xi,yi,x,order):
	from scipy.interpolate import InterpolatedUnivariateSpline

	s = InterpolatedUnivariateSpline(xi, yi, k=order)
	y = s(x)
	return y

#----------------------------------------------------------------------
#Function to calculate losses corresponding to consumption

def cost_consump(consump,df_peak,df_off_peak):
    if(consump >= 0.459):
        for i in range(0, len(df_peak)):
            if(df_peak["Peak_Consumption"][i] > consump):
                cost = df_peak["Loss"][i]
                return cost        
                break;

    elif(consump <= 0.309):
        for i in range(0, len(df_off_peak)):
            if(df_off_peak["Off_Peak_Consumption"][i] > consump):
                cost = df_off_peak["Loss"][i]
                return cost        
                break;
    
    return 0

#----------------------------------------------------------------------
