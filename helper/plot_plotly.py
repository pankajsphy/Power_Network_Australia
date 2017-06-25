from shared_import import *
Months = ['July', 'August','September','October', 'November', 
          'December', 'January', 'February', 'March', 'April', 
          'May', 'June']

Years=['2010','2011','2012']

def plot_shaded(df,month,ytitle):
	
	Months = [	'July', 'August','September','October', 'November', 
          		'December', 'January', 'February', 'March', 'April', 
          		'May', 'June']

	month_ind = -1
	for i,e in enumerate(Months):
		if e == 'month':
			month_ind = i

	df_mean = df.resample('M').mean().transpose()
	df_std  = df.resample('M').std().transpose()
	
	y_upper = df_mean.iloc[:,month_ind] + df_std.iloc[:,month_ind]
	y_lower = df_mean.iloc[:,month_ind] - df_std.iloc[:,month_ind]    
	y_lower = y_lower[::-1]

	x = df_mean.index;
	x_rev = x[::-1]

	trace1 = go.Scatter(
	    x=x.append(x_rev),
	    y=y_upper.append(y_lower),
	    fill='tozerox',
	    fillcolor='rgba(51,153,255,0.2)',
	    line=go.Line(color='transparent'),
	    showlegend=True,
	    name='1sigma',
	)

	trace2 = go.Scatter(
	    x=x,
	    y=df_mean.iloc[:,month_ind],
	    line=go.Line(color='rgb(51,153,255)'),
	    mode='lines',
	    showlegend=True,
	    name='Mean',
	)

	layout = go.Layout(
	    	paper_bgcolor='rgb(255,255,255)',
	    	plot_bgcolor='rgb(229,229,229)',
			title=month,
	    	xaxis=dict(
	    	gridcolor='rgb(255,255,255)',
            range=[0,47],
	    	showgrid=True,
	   		showline=False,
        	showticklabels=True,
	        tickcolor='rgb(127,127,127)',
	        ticks='outside',
	        zeroline=False,
			title='Period',
#	        tickangle=45,
	    	),
    	yaxis=dict(
        	gridcolor='rgb(255,255,255)',
        	showgrid=True,
        	showline=False,
	        showticklabels=True,
        	tickcolor='rgb(127,127,127)',
	        ticks='outside',
	        zeroline=False,
			title=ytitle,
    		),
	)

	data = [trace1,trace2]
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.iplot(fig, filename= 'Mean_Variation_Filled')

#	py.image.save_as(fig, filename= './plots/Mean_Variation_Filled.png')
#	from IPython.display import Image
#	Image('./plots/Mean_Variation_Filled.png')


#-----------------------------------------------------------

#def plot_shad(data,ytitle,figname,month):
def plot_shad(data,ytitle,month):
	
	layout = go.Layout(
	    	paper_bgcolor='rgb(255,255,255)',
	    	plot_bgcolor='rgb(229,229,229)',
			title=month,
	    	xaxis=dict(
	    	gridcolor='rgb(255,255,255)',
            range=[0,47],
	    	showgrid=True,
	   		showline=False,
        	showticklabels=True,
	        tickcolor='rgb(127,127,127)',
	        ticks='outside',
	        zeroline=False,
			title='Period',
#	        tickangle=45,
	    	),
    	yaxis=dict(
        	gridcolor='rgb(255,255,255)',
        	showgrid=True,
        	showline=False,
	        showticklabels=True,
        	tickcolor='rgb(127,127,127)',
	        ticks='outside',
	        zeroline=False,
			title=ytitle,
    		),
	)

#	data = [trace1,trace2]
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.iplot(fig, filename= 'Mean_Variation_Filled')

#	py.image.save_as(fig, filename= figname)
#	from IPython.display import Image
#	Image(figname)

#----------------------------------------------------------------

#Function for plotting multplots in a 6x2 gird
def plot_multi(df,Title,Figname):

	data = {}
	for e in Months:
		data[e] = []

	Line_Color=['rgb(51,153,255)','rgb(255,51,53)','rgb(255,153,51)']
	Legend_Flag=[True,False,False,False,False,False,False,False,False,False,False,False]

	for i,e in enumerate(Months):
		for j,key in enumerate(Years):	
			df_mean = df[key].resample('M').mean().transpose()
			x = df_mean.index

			trace = go.Scatter(
			    x=x,
			    y=df_mean.iloc[:,i],
			    line=go.Line(color=Line_Color[j]),
			    mode='lines',
			    showlegend=Legend_Flag[i],
			    name=key,
				)

			data[e].append(trace)

	fig = tools.make_subplots(rows = 6, cols = 2, 
                          shared_xaxes = True, 
                          shared_yaxes = True,
                          horizontal_spacing = 0.015,
                          vertical_spacing = 0.025,
                          subplot_titles=(Months)
                         )
	fig['layout'].update(height=1200, width=1200,title=Title)

	for i,e in enumerate(Months):
		(j, i) = divmod(i,2)
		fig.append_trace(data[e][0], j + 1, i + 1)
		fig.append_trace(data[e][1], j + 1, i + 1)
		fig.append_trace(data[e][2], j + 1, i + 1)

	fig['layout']['xaxis1'].update(title='Period', 
		    	gridcolor='rgb(255,255,255)',
            	range=[0,47],
		    	showgrid=True,
			   	showline=False,
	        	showticklabels=True,
		        tickcolor='rgb(127,127,127)',
		        ticks='outside',
		        zeroline=False,
				)
    
	fig['layout']['xaxis2'].update(title='Period',gridcolor='rgb(255,255,255)',
            	range=[0,47],showgrid=True,showline=False,showticklabels=True,
		        tickcolor='rgb(127,127,127)',ticks='outside',zeroline=False)

	fig['layout']['yaxis1'].update(gridcolor='rgb(255,255,255)', showgrid=True, showline=False,
		        showticklabels=True, tickcolor='rgb(127,127,127)', ticks='outside', zeroline=False)    

	fig['layout']['yaxis2'].update(gridcolor='rgb(255,255,255)', showgrid=True, showline=False,
		        showticklabels=True, tickcolor='rgb(127,127,127)', ticks='outside', zeroline=False)    

	fig['layout']['yaxis3'].update(gridcolor='rgb(255,255,255)', showgrid=True, showline=False,
		        showticklabels=True, tickcolor='rgb(127,127,127)', ticks='outside', zeroline=False)    

	fig['layout']['yaxis4'].update(gridcolor='rgb(255,255,255)', showgrid=True, showline=False,
		        showticklabels=True, tickcolor='rgb(127,127,127)', ticks='outside', zeroline=False)    

	fig['layout']['yaxis5'].update(gridcolor='rgb(255,255,255)', showgrid=True, showline=False,
		        showticklabels=True, tickcolor='rgb(127,127,127)', ticks='outside', zeroline=False)    

	fig['layout']['yaxis6'].update(gridcolor='rgb(255,255,255)', showgrid=True, showline=False,
		        showticklabels=True, tickcolor='rgb(127,127,127)', ticks='outside', zeroline=False)    

	fig['layout'].update(paper_bgcolor='rgb(255,255,255)',
						 plot_bgcolor='rgb(229,229,229)')

#	plotly.offline.iplot(fig, filename='Mean_Variation_Year')

	py.image.save_as(fig, filename= Figname)
	from IPython.display import Image
	Image(Figname)

#----------------------------------------------------------------

def plot_bar_group(data,figname):

	layout = go.Layout(
    	xaxis=dict(
    	    tickangle=-45,
    	    titlefont = dict(
    	        size=16,
    	        color='rgb(107, 107, 107)'
    	        ),
    	    tickfont=dict(
    	        size=14,
    	        color='rgb(107, 107, 107)'
    	        )
    	    ),
        
    	barmode='group',
    	bargap=0.15,
    	bargroupgap=0.1,
    
    	yaxis=dict(
    	    title='Monthly Peak/Off-Peak Losses (AUD)',
    	    titlefont=dict(
    	        size=16,
    	        color='rgb(107, 107, 107)'
    	        ),
    	    tickfont=dict(
    	        size=14,
    	        color='rgb(107, 107, 107)'
    	        )
    	    ),
    
    	legend=dict(
    	    x=0.05,
    	    y=1.2,
    	    bgcolor='rgba(255, 255, 255, 0)',
    	    bordercolor='rgba(255, 255, 255, 0)'
    	    ),
    	)

	fig = go.Figure(data=data, layout=layout )

#	plotly.offline.iplot(fig, filename='Mean_Variation_Year')

	py.image.save_as(fig, filename= figname)
	from IPython.display import Image
	Image(figname)             

