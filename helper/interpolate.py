def interpol(xi,yi,x,order):
	from scipy.interpolate import InterpolatedUnivariateSpline

	s = InterpolatedUnivariateSpline(xi, yi, k=order)
	y = s(x)
	return y

#----------------------------------------------------------------------
#Function to calculate losses corresponding to consumption

def cost_consump(consump,x_OP,y_OP,x_P,y_P):
    from helper.interpolate import interpol

    if(consump >= 0.459):
        return interpol(x_P,y_P,consump,1)
    elif(consump <= 0.309):
        return interpol(x_OP,y_OP,consump,1)    
    return 0


