#Import Libraries
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

#Get your own mapbox token
mapbox_access_token='put your mapbox token here'


#Read data and add a color column for crimes
df=pd.read_csv('c:\\users\\hp\\Documents\\Dashcsv\\New_York_City_Restaurant_Inspection_Results.csv')
df.count()
df.isnull().sum()
df.dropna(inplace=True)
df.count()
df.isnull().sum()
df['CUISINE']=df['CUISINE DESCRIPTION']
df=df[(df.CUISINE.isin(['African','Asian','Barbacue','Chinese','French','Indian','Italian','Korean','Latin','Pizza','Seafood','Vegeterian']))]
df=df[(df.GRADE.isin(['A','B','C']))]

#Create color column for different cuisine type
df['Colors']='red'
df['Colors'][df['CUISINE']=='Asian']='blue'
df['Colors'][df['CUISINE']=='Barbacue']='green'
df['Colors'][df['CUISINE']=='Chinese']='orange'
df['Colors'][df['CUISINE']=='French']='aqua'
df['Colors'][df['CUISINE']=='Indian']='khaki'
df['Colors'][df['CUISINE']=='Italian']='purple'
df['Colors'][df['CUISINE']=='Korean']='darksalmon'
df['Colors'][df['CUISINE']=='Latin']='brown'
df['Colors'][df['CUISINE']=='Pizza']='maroon'
df['Colors'][df['CUISINE']=='Seafood']='coral'
df['Colors'][df['CUISINE']=='Vegeterian']='olive'
blackbold={'color':'black','font-weight':'bold'}

app=dash.Dash(__name__)

#Dash component
app.layout=html.Div([
    html.Div([
        html.Div([           
         
            #Borough_checklist
            html.Label(children=['Borough:'],style=blackbold),
            dcc.Checklist(id='boro_name',
                          options=[{'label':str(b),'value':b} for b in sorted(df['BORO'].unique())],
                          value=[b for b in sorted(df['BORO'].unique())],
                
                ),
            
            #Cuisine_checklist
            html.Label(children=['Cuisine:'],style=blackbold),
            dcc.Checklist(id='cuisine_name',
                          options=[{'label':str(b),'value':b} for b in sorted(df['CUISINE'].unique())],
                          value=[b for b in sorted(df['CUISINE'].unique())],
                
                ),
             #Grade_checklist
            html.Label(children=['Grade:'],style=blackbold),
            dcc.Checklist(id='grade_name',
                          options=[{'label':str(b),'value':b} for b in sorted(df['GRADE'].unique())],
                          value=[b for b in sorted(df['GRADE'].unique())],
                          )
            
            ]),
        
        #Plotly graphs
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                      style={'padding-bottom':'2px','padding-left':'2px','height':'90vh'} 
                )
            ]),
        
        ]),
     
    ])

#Callback 
@app.callback(Output('graph','figure'),
              [Input('boro_name','value'),
               Input('cuisine_name','value'),
               Input('grade_name','value')]) 


def update_figure(boro_name,cuisine_name,grade_name):
    dff=df[(df['BORO'].isin(boro_name))&
           (df['CUISINE'].isin(cuisine_name))&
           (df['GRADE'].isin(grade_name))]
    
    #create figure
    locations=[go.Scattermapbox(
                    lon = dff['Longitude'],
                    lat = dff['Latitude'],
                    mode='markers',
                    marker={'color' : dff['Colors']},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=dff[['BUILDING','STREET','ZIPCODE','CUISINE']]
                    
                    )]
    
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo',
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            title=dict(text="New York Restaurents",font=dict(size=40, color='teal')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='light',
                center=dict(
                    lat=40.8010,
                    lon=-73.945155
                ),
                pitch=50,
                zoom=11
            ),
        )
    }


if __name__ == '__main__':
    app.run_server()