
# coding: utf-8

# ## Importing python packages for the analysis of data.
# 
# ### In this analysis, I will be using following packages:
# 1. Python v3.0
# 2. Numpy v1.12.1
# 3. Pandas v0.20.1
# 4. Plotly v2.0.8
# 5. Cufflinks v0.8.2
# 

# In[1]:


import pandas as pd
import numpy as np
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from calc import *
#import cufflinks as cf

plotly.offline.init_notebook_mode() # run at the start of every notebook
#plotly.tools.set_credentials_file(username='pankajs.phy', api_key='e0zYzuRpN5PC3GZV4zYC')
#plotly.tools.set_config_file(world_readable=True)


# ### First I am importing the Excel data into the workspace in panda. The imported data will be stored in a pandas dataframe.
# ### In the next step, all the column headings will be renamed. Basically, the whitespaces in the headings are replaced with an underscore.

# In[2]:


xl = pd.ExcelFile("./data/Consumer_1_profile_2010-2011.xlsx",index=False)
df = xl.parse("Sheet1",index=False)
df=df.rename(columns={"Customer no." : "Customer_No", 'Consumption Category' : 'Consumption_Category','Period 1':'00:00','Period 2':'00:30','Period 3':'01:00','Period 4':'01:30','Period 5':'02:00','Period 6':'02:30','Period 7':'03:00','Period 8':'03:30','Period 9':'04:00','Period 10':'04:30','Period 11':'05:00','Period 12':'05:30','Period 13':'06:00','Period 14':'06:30','Period 15':'07:00','Period 16':'07:30','Period 17':'08:00','Period 18':'08:30','Period 19':'09:00','Period 20':'09:30','Period 21':'10:00','Period 22':'10:30','Period 23':'11:00','Period 24':'11:30','Period 25':'12:00','Period 26':'12:30','Period 27':'13:00','Period 28':'13:30','Period 29':'14:00','Period 30':'14:30','Period 31':'15:00','Period 32':'15:30','Period 33':'16:00','Period 34':'16:30','Period 35':'17:00','Period 36':'17:30','Period 37':'18:00','Period 38':'18:30','Period 39':'19:00','Period 40':'19:30','Period 41':'20:00','Period 42':'20:30','Period 43':'21:00','Period 44':'21:30','Period 45':'22:00','Period 46':'22:30','Period 47':'23:00','Period 48':'23:30'})
df.head();


# ### In the following code, the dataframe is splitted into three dataframes according to consumption category i.e., df_GG, df_CL and df_GC.
# 

# In[3]:


df_GG=df[df.Consumption_Category=='GG']
df_CL=df[df.Consumption_Category=='CL']
df_GC=df[df.Consumption_Category=='GC']


# In[4]:


df_GG.to_csv('./data/Consumer_1_2010-2011_GG.csv', encoding='utf-8',index=False)
df_CL.to_csv('./data/Consumer_1_2010-2011_CL.csv', encoding='utf-8',index=False)
df_GC.to_csv('./data/Consumer_1_2010-2011_GC.csv', encoding='utf-8',index=False)


# In[5]:


df_GG = pd.read_csv('./data/Consumer_1_2010-2011_GG.csv',
                    parse_dates={'Date': [2,3,4]}, 
                    date_parser=lambda x: pd.datetime.strptime(x, '%d %m %Y'))


df_CL = pd.read_csv('./data/Consumer_1_2010-2011_CL.csv',
                    parse_dates={'Date': [2,3,4]}, 
                    date_parser=lambda x: pd.datetime.strptime(x, '%d %m %Y'))


df_GC = pd.read_csv('./data/Consumer_1_2010-2011_GC.csv',
                    parse_dates={'Date': [2,3,4]}, 
                    date_parser=lambda x: pd.datetime.strptime(x, '%d %m %Y'))


# ### Here we create a new dataframe which contains the volume of discharge needed in each period for consumer1.

# In[6]:


start = datetime.datetime(2010, 7, 1) #Start of the year
end   = datetime.datetime(2011, 6, 30)#End of the year
Dates = pd.date_range(start, end)#Series of the dates in the year 2010-2011

df_vol_dschg = pd.DataFrame() #New dataframe for volme discharge
df_vol_dschg['Date'] = Dates # Creating first column with dates

df_consump = pd.DataFrame() #New dataframe for volme discharge
df_consump['Date'] = Dates # Creating first column with dates

#df_vol_dschg.head()

for i in range(0,48): #Function to create new columns corresponding to volume discharge    
    if(i%2 == 0):
        if (i/2 <= 9):
            key = '0'+str(int(i/2))+':00'
        elif (i/2 >=10):
            key = str(int(i/2))+':00'
    elif(i%2 == 1):
        if (i/2 < 10):
            key = '0'+str(int(i/2))+':30'
        elif (i/2 >=10):
            key = str(int(i/2))+':30'
            
    df_vol_dschg[key] = dch_vol(df_GC,df_CL,df_GG,key); #Calling the function dch_vol to provide values to Period_1 to Period_48            
    df_consump[key] = consump(df_GC,df_CL,key); #Calling the function consump to provide values to Period_1 to Period_48                

# Converting Date column as datetime data type    
df_vol_dschg['Date'] = pd.to_datetime(Dates) 
df_vol_dschg.index = df_vol_dschg['Date']
#df_vol_dschg["Total"] = df_vol_dschg.iloc[:,1:49].sum(axis=1)

# Writing the new dataframe into csv file
df_vol_dschg.to_csv('./data/Consumer_1_2010-2011_discharge.csv', encoding='utf-8',index=False);
df_vol_dschg.head();

# Converting Date column as datetime data type    
df_consump['Date'] = pd.to_datetime(Dates) 
df_consump.index = df_consump['Date']
#df_consump["Total"] = df_consump.iloc[:,1:49].sum(axis=1)
# Writing the new dataframe into csv file
df_consump.to_csv('./data/Consumer_1_2010-2011_consumption.csv', encoding='utf-8',index=False);
df_consump.head(30)


# In[7]:


Monthly_std_discharge = df_vol_dschg.resample('M').std()
Monthly_mean_discharge = df_vol_dschg.resample('M').mean()
Monthly_min_discharge  = df_vol_dschg.resample('M').min()
Monthly_max_discharge  = df_vol_dschg.resample('M').max()

Monthly_mean_discharge.describe();
Monthly_std_discharge.iloc[:,1:10];


# In[8]:


data_mean = [go.Scatter(
                        x = Monthly_mean_discharge.index, 
                        y = Monthly_mean_discharge['00:30']
                        )
            ]
#plotly.offline.iplot(data_mean, filename='basic-line-plot');


# In[9]:


Trans_Monthly_mean = Monthly_mean_discharge.transpose();
Trans_Monthly_min  = Monthly_min_discharge.transpose();
Trans_Monthly_max  = Monthly_max_discharge.transpose();
Trans_Monthly_std  = Monthly_std_discharge.transpose();


# In[10]:


data_mean = go.Scatter(
                        x = Monthly_mean_discharge.transpose().index, 
                        y = Monthly_mean_discharge.transpose().iloc[0:48,0],
                        name = 'Mean'
                        )
            
data_min = go.Scatter(
                        x = Monthly_mean_discharge.transpose().index, 
                        y = Monthly_std_discharge.transpose().iloc[0:48,0] 
                          - Monthly_std_discharge.transpose().iloc[0:48,0],
                        name = 'Mean - 1 sigma'
                        )

data_max = go.Scatter(
                        x = Monthly_mean_discharge.transpose().index, 
                        y = Monthly_std_discharge.transpose().iloc[0:48,0] 
                          + Monthly_std_discharge.transpose().iloc[0:48,0],
                        name = 'Mean + 1 sigma'
                        )

text = go.Scatter( x = '05:00', y = 2.0, text = 'July', mode = 'text',
                  textfont=dict(
                        family='sans serif',
                        size=18,
                        color='#7f7f7f'
                    ),
                      showlegend=False,
                 )

data = [data_mean, data_min, data_max, text]

layout = {
    'xaxis': 
        {
#        'range': [0, 7],
        'title': 'Period',
        'showgrid': False,
        },
    'yaxis': 
        {
        'title': 'Average discharge volume/half-hourly/month',
        'range': [-1, 2.5]
        },
#    'font':{'family': 'Courier New, monospace', 'size' : 18, 'color' :'#7f7f7f'},
    'shapes': 
        [   
        # filled Rectangle
        {
         'type': 'rect',
         'x0': 0,
         'y0': 0.35,
         'x1': 48,
         'y1': 0.45,
         'line': 
            {
                'color': 'rgba(128, 0, 128, 0.4)',
                'width': 2,
            },
                'fillcolor': 'rgba(128, 0, 128, 0.4)',
        },
        ]
    }
fig = {'data': data, 'layout': layout}
plotly.offline.iplot(fig, filename='Mean_variation_July')


# In[11]:



plotly.offline.iplot([{
    'x': Trans_Monthly_mean.index[0:48],
    'y': Trans_Monthly_mean[col],
    'name': col
}  for col in Trans_Monthly_mean.columns])


# In[12]:


Months = ['July', 'August','September','October', 'November', 
          'December', 'January', 'February', 'March', 'April', 
          'May', 'June']

data = {}

for i,e in enumerate(Months):
    
    Trace_1 = go.Scatter(
                        x = Trans_Monthly_mean.index, 
                        y = Trans_Monthly_mean.iloc[0:48,i],
                        name = 'Mean',
#                        showlegend = True 
                        )
            
    Trace_2 = go.Scatter(
                        x = Trans_Monthly_mean.index, 
                        y = Trans_Monthly_mean.iloc[0:48,i] 
                          - Trans_Monthly_std.iloc[0:48,i],
                        name = 'Mean - 1 sigma',
#                        showlegend = False,
                        )

    Trace_3 = go.Scatter(
                        x = Trans_Monthly_mean.index, 
                        y = Trans_Monthly_mean.iloc[0:48,i]
                          + Trans_Monthly_std.iloc[0:48,i],
                        name = 'Mean + 1 sigma',
#                        showlegend = False,        
                        )

    data[e] = [Trace_1, Trace_2, Trace_3]  


# In[13]:


fig = tools.make_subplots(
                          rows = 6, 
                          cols = 2, 
                          shared_xaxes = True, 
                          shared_yaxes = True,
                          horizontal_spacing = 0.025,
                          vertical_spacing = 0.025,
                          subplot_titles=(Months)
                         )

for i,e in enumerate(Months):
    (j, i) = divmod(i,2)
    
    fig.append_trace(data[e][0], j + 1, i + 1)
    fig.append_trace(data[e][1], j + 1, i + 1)
    fig.append_trace(data[e][2], j + 1, i + 1)

    fig['layout'].update(height=1200, width=1600,
                     title='Mean variation of discharge volume across a financial year')

fig['layout']['xaxis1'].update(title='Period')    
fig['layout']['xaxis2'].update(title='Period')    
fig['layout']['yaxis1'].update(title='Mean Variation of discharge volume')    

plotly.offline.iplot(fig, filename='Mean_Variation_Year');


# In[14]:


df1 = df_vol_dschg


df1_mean = df1.resample('M').mean().transpose()
df1_std  = df1.resample('M').std().transpose()

y_upper = df1_mean.iloc[:,0] + df1_std.iloc[:,0]
y_lower = df1_mean.iloc[:,0] - df1_std.iloc[:,0]    
y_lower = y_lower[::-1]

x = df1_mean.index;
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
    y=df1_mean.iloc[:,0],
    line=go.Line(color='rgb(51,153,255)'),
    mode='lines',
    showlegend=True,
    name='Mean',
)
layout = go.Layout(
    paper_bgcolor='rgb(255,255,255)',
    plot_bgcolor='rgb(229,229,229)',
    xaxis=dict(
        gridcolor='rgb(255,255,255)',
        range=[0,47],
        showgrid=True,
        showline=False,
        showticklabels=True,
        tickcolor='rgb(127,127,127)',
        ticks='outside',
        zeroline=False,
#        tickangle=45,
    ),
    yaxis=dict(
        gridcolor='rgb(255,255,255)',
#        range=[-1,3],
        showgrid=True,
        showline=False,
        showticklabels=True,
        tickcolor='rgb(127,127,127)',
        ticks='outside',
        zeroline=False
    ),
)

data = go.Data([trace1,trace2])
fig = go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig, filename= 'Mean_Variation_Filled');


# In[15]:


from plot_plotly import plot_shaded

plot_shaded(df_vol_dschg)


# In[16]:


from interpolate import interpol

#First Off-Peak Losses

order = 1

yi=[16.76,10.89,6.36,4.41,3.10,2.17,1.48,0.99,0.67,0.30]
xi=[0.03,0.06,0.09,0.11,0.14,0.17,0.20,0.23,0.26,0.29]
x=np.linspace(0,0.309,2000)

df_loss_off_peak = pd.DataFrame({})
df_loss_off_peak["Off_Peak_Consumption"]=x
df_loss_off_peak["Loss"]=interpol(xi,yi,x,order)
df_loss_off_peak["Loss"][0]=0.0

#Now Peak Consumption Losses

yi = [1.79,2.92,3.55,4.24]
xi = [0.46,0.49,0.51,0.54]
x  = np.linspace(0.46,2.5,2000)

df_loss_peak_geom = pd.DataFrame({})
df_loss_peak_geom["Peak_Consumption"]=x
df_loss_peak_geom["Loss"]=interpol(xi,yi,x,order)

#Now Peak Consumption Losses with extrapolation
yi = [1.79,2.92,3.55,4.24]
xi = [0.46,0.49,0.51,0.54]
x  = np.linspace(0.45,0.54,1000)
y = interpol(xi,yi,x,order)

x = np.append(x, np.array(np.linspace(0.540001,2.5,1000)))
y = np.append(y, [4.24 for i in range(0,1000)])

df_loss_peak = pd.DataFrame({})
df_loss_peak["Peak_Consumption"]=x
df_loss_peak["Loss"]=y


# In[ ]:





# In[17]:


Monthly_std_consump  = df_consump.resample('M').std()
Monthly_mean_consump = df_consump.resample('M').mean()
Monthly_min_consump  = df_consump.resample('M').min()
Monthly_max_consump  = df_consump.resample('M').max()

Monthly_mean_consump.describe();
Monthly_std_consump.transpose().iloc[:,1:10];


# In[18]:


df_loss_peak.head()
df_loss_off_peak.head()


# In[19]:


from interpolate import cost_consump
Monthly_mean_cost_geom = pd.DataFrame.copy(Monthly_mean_consump,deep=True)

#for i in range(0,48):
#    for j in range(0,12):
#        mean_consump = Monthly_mean_consump.transpose().iloc[i,j]
#        Monthly_mean_cost.transpose().iloc[i,j] = cost_consump(mean_consump)

Monthly_mean_cost_geom = Monthly_mean_consump.transpose().applymap(cost_consump(**df_loss_peak,**df_loss_off_peak))
Monthly_mean_cost_geom.head()


# In[ ]:





# In[ ]:


def cost_consump(mean_consump):
    if(mean_consump >= 0.45):
        for i in range(0, len(df_loss_peak)):
            if(df_loss_peak["Peak_Consumption"][i] > mean_consump):
                cost = df_loss_peak["Loss"][i-1]
                return cost        
                break;

    elif(mean_consump <= 0.309):
        for i in range(0, len(df_loss_off_peak)):
            if(df_loss_off_peak["Off_Peak_Consumption"][i] > mean_consump):
                cost = df_loss_off_peak["Loss"][i-1]
                return cost        
                break;
    
    return 0

Monthly_mean_cost = pd.DataFrame.copy(Monthly_mean_consump,deep=True)
Monthly_mean_cost = pd.DataFrame.copy(Monthly_mean_consump,deep=True)

Monthly_mean_cost = Monthly_mean_consump.transpose().applymap(cost_consump)


# In[ ]:


Monthly_mean_cost_geom.transpose().head()


# In[ ]:


Monthly_mean_consump['00.00']


# In[ ]:




