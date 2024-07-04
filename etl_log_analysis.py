import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re 

from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc




figure_no = 0

df_2022 = pd.read_excel("etl_log(20240619)-2 (2022).xlsx",sheet_name = "Export Worksheet",header = 0)
df_2023 = pd.read_excel("etl_log(20240619)-2 (2023).xlsx",sheet_name = "Export Worksheet",header = 0)

df_2023.set_index(pd.Series([i for i in range(len(df_2022),len(df_2022)+len(df_2023))]), inplace=True)

df_2022 = pd.concat([df_2022,df_2023],axis=0)


df_2022_HKMA = df_2022[(df_2022["CONTEXT"]=="HKMA")].reset_index() #add condition to filter out non-required hours (see if it can detect the datetime)


for i in range(len(df_2022_HKMA["TASK_START"])):
    temp = re.search("..:..:..",str(df_2022_HKMA["TASK_START"][i]))
    df_2022_HKMA.loc[i:i,'TASK_START':'TASK_START']= temp.group(0)
    temp = re.search("..:..:..",str(df_2022_HKMA["TASK_END"][i]))
    df_2022_HKMA.loc[i:i,'TASK_END':'TASK_END']= temp.group(0)
    temp = re.search("..:..:...*",str(df_2022_HKMA["DURATION"][i]))
    df_2022_HKMA.loc[i:i,'DURATION':'DURATION']= temp.group(0)



df_2022_HKMA_PR = df_2022[(df_2022["CONTEXT"]=="HKMA_PR")].reset_index() #add condition to filter out non-required hours (see if it can detect the datetime)


#for i in range(df_2022_HKMA_PR.index.values[0],len(df_2022)):
for i in range(len(df_2022_HKMA_PR["TASK_START"])): 
    temp = re.search("..:..:..",str(df_2022_HKMA_PR["TASK_START"][i]))
    df_2022_HKMA_PR.loc[i:i,'TASK_START':'TASK_START']= temp.group(0)
    temp = re.search("..:..:..",str(df_2022_HKMA_PR["TASK_END"][i]))
    df_2022_HKMA_PR.loc[i:i,'TASK_END':'TASK_END']= temp.group(0)
    temp = re.search("..:..:...*",str(df_2022_HKMA_PR["DURATION"][i]))
    df_2022_HKMA_PR.loc[i:i,'DURATION':'DURATION']= temp.group(0)
    

excepted_dates = pd.Series(["17-OCT-23 00.00.00","06-OCT-23 00.00.00","21-SEP-23 00.00.00","30-AUG-23 00.00.00","13-NOV-22 00.00.00","26-SEP-22 00.00.00","27-AUG-22 00.00.00","05-AUG-22 00.00.00"]) #except that later

df_2022_HKMA = df_2022_HKMA[(df_2022_HKMA["TASK_START"]>='04:00:00')&(df_2022_HKMA["TASK_END"]<='06:00:00')]
df_2022_HKMA_PR = df_2022_HKMA_PR[(df_2022_HKMA_PR["TASK_START"]>='02:00:00')&(df_2022_HKMA_PR["TASK_END"]<='04:00:00')]


df_2022_HKMA = df_2022_HKMA[~df_2022_HKMA['ETL_DATE'].isin(excepted_dates)]
df_2022_HKMA_PR = df_2022_HKMA_PR[~df_2022_HKMA_PR['ETL_DATE'].isin(excepted_dates)]


df_2022_HKMA = df_2022_HKMA[~df_2022_HKMA.index.isin(excepted_dates)]
df_2022_HKMA_PR = df_2022_HKMA_PR[~df_2022_HKMA_PR.index.isin(excepted_dates)]


df_2022_HKMA_groupByDate = df_2022_HKMA.groupby(["ETL_DATE"])
df_2022_HKMA_PR_groupByDate = df_2022_HKMA_PR.groupby(["ETL_DATE"])


df_2022_HKMA_min_start_time = df_2022_HKMA_groupByDate["TASK_START"].min().sort_values()
df_2022_HKMA_max_end_time = df_2022_HKMA_groupByDate["TASK_END"].max().sort_values()
df_2022_HKMA_PR_min_start_time = df_2022_HKMA_PR_groupByDate["TASK_START"].min().sort_values()
df_2022_HKMA_PR_max_end_time = df_2022_HKMA_PR_groupByDate["TASK_END"].max().sort_values()


Total_duration_2022_HKMA = pd.concat([df_2022_HKMA_min_start_time,df_2022_HKMA_max_end_time],axis=1)
Total_duration_2022_HKMA["total_duration"] = (pd.to_datetime(Total_duration_2022_HKMA["TASK_END"]) - pd.to_datetime(Total_duration_2022_HKMA["TASK_START"])).dt.total_seconds()

Total_duration_2022_HKMA["FINAL_DATE"]= pd.to_datetime(Total_duration_2022_HKMA.index.values, format='%d-%b-%y %H.%M.%S')


Total_duration_2022_HKMA = Total_duration_2022_HKMA.sort_values("FINAL_DATE")






Total_duration_2022_HKMA_PR = pd.concat([df_2022_HKMA_PR_min_start_time,df_2022_HKMA_PR_max_end_time],axis=1)
Total_duration_2022_HKMA_PR["total_duration"] = (pd.to_datetime(Total_duration_2022_HKMA_PR["TASK_END"]) - pd.to_datetime(Total_duration_2022_HKMA_PR["TASK_START"])).dt.total_seconds()

Total_duration_2022_HKMA_PR["FINAL_DATE"]= pd.to_datetime(Total_duration_2022_HKMA_PR.index.values, format='%d-%b-%y %H.%M.%S')


Total_duration_2022_HKMA_PR = Total_duration_2022_HKMA_PR.sort_values("FINAL_DATE")


df_2022_HKMA["ETL_DATE"]= pd.to_datetime(df_2022_HKMA["ETL_DATE"], format='%d-%b-%y %H.%M.%S')
df_2022_HKMA_PR["ETL_DATE"]= pd.to_datetime(df_2022_HKMA_PR["ETL_DATE"], format='%d-%b-%y %H.%M.%S')


#turn to xxx_1, xxx_2, ...


def condition(x):
    return x+"_2"
def condition2(x):
    return x+"_3"
def condition3(x):
    return x+"_4"

df_2022_HKMA.groupby(["ETL_DATE", "ETL_TASK"]).nth(0)["ETL_TASK"]
one = pd.DataFrame(df_2022_HKMA.groupby(["ETL_DATE", "ETL_TASK"]).nth(1)["ETL_TASK"].apply(condition),columns = ["ETL_TASK"])
two = pd.DataFrame(df_2022_HKMA.groupby(["ETL_DATE", "ETL_TASK"]).nth(2)["ETL_TASK"].apply(condition2),columns = ["ETL_TASK"])
three = pd.DataFrame(df_2022_HKMA.groupby(["ETL_DATE", "ETL_TASK"]).nth(3)["ETL_TASK"].apply(condition3),columns = ["ETL_TASK"])
df_2022_HKMA.update(one)
df_2022_HKMA.update(two)
df_2022_HKMA.update(three)

df_2022_HKMA_PR.groupby(["ETL_DATE", "ETL_TASK"]).nth(0)["ETL_TASK"]
one = pd.DataFrame(df_2022_HKMA_PR.groupby(["ETL_DATE", "ETL_TASK"]).nth(1)["ETL_TASK"].apply(condition),columns = ["ETL_TASK"])
two = pd.DataFrame(df_2022_HKMA_PR.groupby(["ETL_DATE", "ETL_TASK"]).nth(2)["ETL_TASK"].apply(condition2),columns = ["ETL_TASK"])
three = pd.DataFrame(df_2022_HKMA_PR.groupby(["ETL_DATE", "ETL_TASK"]).nth(3)["ETL_TASK"].apply(condition3),columns = ["ETL_TASK"])
df_2022_HKMA_PR.update(one)
df_2022_HKMA_PR.update(two)
df_2022_HKMA_PR.update(three)


final_df = pd.DataFrame(columns=['ETL_DATE', 'DURATION', 'CONTEXT','ETL_TASK'])

#Testing plot all unique ETL TASKS
for y in df_2022_HKMA["ETL_TASK"].unique():
    newdf = pd.DataFrame()
    newdf["ETL_DATE"] = df_2022_HKMA[df_2022_HKMA["ETL_TASK"]==y]["ETL_DATE"]
    newdf["DURATION"] = (pd.to_datetime(df_2022_HKMA[df_2022_HKMA["ETL_TASK"]==y]["DURATION"],format='%H:%M:%S.%f')-pd.to_datetime("00:00:00.000000",format='%H:%M:%S.%f')).dt.total_seconds()
    newdf["CONTEXT"] = "HKMA"
    newdf["ETL_TASK"]= y
    final_df = pd.concat([final_df,newdf],axis=0)



for y in df_2022_HKMA_PR["ETL_TASK"].unique():
    newdf = pd.DataFrame()
    newdf["ETL_DATE"] = df_2022_HKMA_PR[df_2022_HKMA_PR["ETL_TASK"]==y]["ETL_DATE"]
    newdf["DURATION"] = (pd.to_datetime(df_2022_HKMA_PR[df_2022_HKMA_PR["ETL_TASK"]==y]["DURATION"],format='%H:%M:%S.%f')-pd.to_datetime("00:00:00.000000",format='%H:%M:%S.%f')).dt.total_seconds()
    newdf["CONTEXT"] = "HKMA_PR"
    newdf["ETL_TASK"]= y
    final_df = pd.concat([final_df,newdf],axis=0)

newdf = pd.DataFrame()
newdf["ETL_DATE"] = Total_duration_2022_HKMA["FINAL_DATE"]
newdf["DURATION"] = Total_duration_2022_HKMA["total_duration"]
newdf["CONTEXT"] = "HKMA"
newdf["ETL_TASK"]= "TOTAL_DURATION"
final_df = pd.concat([final_df,newdf],axis=0)

newdf = pd.DataFrame()
newdf["ETL_DATE"] = Total_duration_2022_HKMA_PR["FINAL_DATE"]
newdf["DURATION"] = Total_duration_2022_HKMA_PR["total_duration"]
newdf["CONTEXT"] = "HKMA_PR"
newdf["ETL_TASK"]= "TOTAL_DURATION"
final_df = pd.concat([final_df,newdf],axis=0)


#dash app
'''
fig = px.scatter(Total_duration_2022_HKMA, x='FINAL_DATE', y='total_duration', title='Scatter Plot Example')
fig.update_traces(marker=dict(size=10, color='red', symbol='circle'))
fig.update_layout(plot_bgcolor='lightgray')
fig.update_layout(xaxis_title='X Axis Label', yaxis_title='Y Axis Label', title_text='Custom Title')
'''

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('ETL Time Trend Analysis'),
    dbc.Row([dbc.Col(dcc.Dropdown(options = sorted(final_df["CONTEXT"].unique()), value = 'HKMA', id='context-dropdown')),dcc.Dropdown(options = sorted(final_df["ETL_TASK"].unique()), value = 'TOTAL_DURATION', id='task-dropdown')]), #not side by side but I think it is fine
    dbc.Row([dcc.Graph(id='overview_graph', figure={}, style ={'width':'45vw', 'height':'45vw', 'display': 'inline-block'}),dcc.Graph(id='task_graph', figure={}, style ={'width':'45vw', 'height':'45vw','display': 'inline-block'})])
])

@app.callback(
    Output('task_graph','figure'),
    Output('overview_graph','figure'),
    Input('context-dropdown','value'),
    Input('task-dropdown','value'),
)
def plot_data(context,task):
    fig = px.scatter(final_df[(final_df['CONTEXT']==context)&(final_df['ETL_TASK']==task)], x='ETL_DATE', y='DURATION', title='Time Required for specific task')
    fig.update_traces(marker=dict(size=10, color='red', symbol='circle'))
    fig.update_layout(plot_bgcolor='lightgray')
    fig.update_layout(xaxis_title='Date', yaxis_title='Time (s)', title_text='Time Required for specific task')

    overview_fig = px.scatter(final_df[(final_df['CONTEXT']==context)&(final_df['ETL_TASK']=="TOTAL_DURATION")], x='ETL_DATE', y='DURATION', title='Total Time Required')
    overview_fig.update_traces(marker=dict(size=10, color='blue', symbol='circle'))
    overview_fig.update_layout(plot_bgcolor='lightgray')
    overview_fig.update_layout(xaxis_title='Date', yaxis_title='Time (s)', title_text='Total Time Required')
    return fig, overview_fig




app.run_server(debug=False,host='0.0.0.0', ssl_context = 'adhoc')
