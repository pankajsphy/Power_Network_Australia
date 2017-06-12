def plot_shad(df,Title):
	
	import pandas as pd
	import plotly
	import plotly.plotly as py
	import plotly.graph_objs as go
	from plotly import tools

	df_mean = df.resample('M').mean().transpose()
	df_std  = df.resample('M').std().transpose()

	Months = ['July', 'August','September','October', 'November', 
          'December', 'January', 'February', 'March', 'April', 
          'May', 'June']

	data = {}

	for i,e in enumerate(Months):
	
		y_upper = df_mean.iloc[:,i] + df_std.iloc[:,i]
		y_lower = df_mean.iloc[:,i] - df_std.iloc[:,i]    
		y_lower = y_lower[::-1]
	
		x = df_mean.index;
		x_rev = x[::-1]

		trace1 = go.Scatter(
		    x=x.append(x_rev),
		    y=y_upper.append(y_lower),
		    fill='tozerox',
		    fillcolor='rgba(51,153,255,0.2)',
		    line=go.Line(color='transparent'),
		    showlegend=False,
		    name='1sigma',
		)

		trace2 = go.Scatter(
		    x=x,
		    y=df_mean.iloc[:,i],
		    line=go.Line(color='rgb(51,153,255)'),
		    mode='lines',
		    showlegend=False,
		    name='Mean',
		)

		data[e] = [trace1,trace2]

	fig = tools.make_subplots(
                          rows = 6, 
                          cols = 2, 
                          shared_xaxes = True, 
                          shared_yaxes = True,
                          horizontal_spacing = 0.025,
                          vertical_spacing = 0.05,
                          subplot_titles=(Months)
                         )

	for i,e in enumerate(Months):
	    (j, i) = divmod(i,2)
   
	    fig.append_trace(data[e][0], j + 1, i + 1)
	    fig.append_trace(data[e][1], j + 1, i + 1)

	fig['layout'].update(height=1200, width=1200,title=Title)



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
    
	fig['layout']['xaxis2'].update(title='Period',
		    	gridcolor='rgb(255,255,255)',
            	range=[0,47],
		    	showgrid=True,
			   	showline=False,
	        	showticklabels=True,
		        tickcolor='rgb(127,127,127)',
		        ticks='outside',
		        zeroline=False,
				)

	fig['layout']['yaxis1'].update(    	    	
				gridcolor='rgb(255,255,255)',
    	    	showgrid=True,
    	    	showline=False,
		        showticklabels=True,
    	    	tickcolor='rgb(127,127,127)',
		        ticks='outside',
		        zeroline=False,
				)    

	fig['layout']['yaxis2'].update(
#				title='Mean Variation of discharge volume',    	    	
				gridcolor='rgb(255,255,255)',
    	    	showgrid=True,
    	    	showline=False,
		        showticklabels=True,
    	    	tickcolor='rgb(127,127,127)',
		        ticks='outside',
		        zeroline=False,
				)    
	fig['layout'].update(paper_bgcolor='rgb(255,255,255)',
						 plot_bgcolor='rgb(229,229,229)')

	plotly.offline.iplot(fig, filename='Mean_Variation_Year');
