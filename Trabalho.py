import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

path = '/Users/JoaoMoraisCosta/Desktop/Projecto de Data Visualization Dash/Data Set Olimpiadas/'

data = pd.read_csv('athlete_events.csv')
total_presence = pd.read_csv(path + 'total_presence.csv')

stat_options = dcc.Dropdown(
    id='stat_drop',
    options=[dict(label='Weight',value='Weight'),
             dict(label='Height',value='Height'),
             dict(label='Age',value='Age')],
    value='Weight'
)
sex_options = dcc.RadioItems(
    id='sex_radio',
    options=[dict(label='Male' , value='M'),
             dict(label='Female' , value='F')],
    value='M'
)

season_options = dcc.RadioItems(
    id='season_radio',
    options=[dict(label='Summer', value='Summer'),
             dict(label='Winter', value='Winter')],
    value='Summer')

event_drop = dcc.Dropdown(
    id='event_drop',
    multi=True)

drop_continent = dcc.Dropdown(
        id = 'drop_continent',
        clearable=False,
        searchable=False,
        options=[{'label': 'World', 'value': 'world'},
                {'label': 'Europe', 'value': 'europe'},
                {'label': 'Asia', 'value': 'asia'},
                {'label': 'Africa', 'value': 'africa'},
                {'label': 'North america', 'value': 'north america'},
                {'label': 'South america', 'value': 'south america'}],
        value='world',
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})


# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.Div([html.Label('LOGO')],id='Logo',style={'width': '20%'}),
        html.Div([html.Label('Titulo')],id='Title',style={'width': '60%'}),
        html.Div([season_options],id='winter_summer',style={'width': '20%'})
    ],id='1_div',style={'display': 'flex','height':'10%'}),
    html.Div([
        html.Label('DIV DANILO')
        #DIV do DANILO
    ],id='2_div',style={'display': 'flex','height':'30%'}),
    html.Div([
        html.Div([html.Label('DIV TOMAS')],id='Barplot',style={'width': '50%'}),
        html.Div([
            html.Div([
            drop_continent,
            html.Br(),
            html.Br(),
            dcc.Graph(
                id='graph',
                #style={'width': '1200px', 'height': '700px', 'margin': 'auto'}

        )],style={'width': '50%'})
    ],id='3_div',style={'display': 'flex','height':'30%'}),
        ]),
    html.Div([
        html.Div([event_drop,
                  html.Br(),
                  sex_options,
                  html.Br(),
                  stat_options,
                  html.Br()],id='Button',style={'width': '20%','display': 'inline-block'}),
        html.Div([dcc.Graph(id = 'parallel_graph')],
                 id='Paralel',style={'width': '80%','display': 'inline-block'})
],id='4_div',style={'display': 'flex','height':'30%'})

    ],id= 'Main_Div')

@app.callback(
    [Output('event_drop', 'options'),
     Output('event_drop', 'value')],
    [Input('season_radio', 'value')]
)
def events(season):
    data_season = data.loc[(data['Season']==season) &  (data['Year'] >= 1950)]
    sports = data_season[['Sport', 'Year']].drop_duplicates().groupby(by='Sport').size()
    sports_to_use = sports[sports > 3]
    data_season = data_season.loc[data_season['Sport'].isin(sports_to_use.index)]
    events_options = [
            dict(label=event, value=event)
            for event in data_season['Sport'].unique()]

    return events_options, [events_options[0]['value']]

@app.callback(
    Output('Main_Div', 'style'),
    [Input('season_radio', 'value')]
)
def background(season):
    if season =='Summer':
        background = {'backgroundColor': '#f7dea6'}

    elif season=='Winter':
        background = {'backgroundColor': '#dbe8ff'}

    return background

@app.callback(
    Output('parallel_graph', 'figure'),
    [Input('stat_drop', 'value'),
     Input('sex_radio', 'value'),
     Input('season_radio', 'value'),
     Input('event_drop', 'value')]
)
def callback_1(stat, sex,season,sports):

    data_paralel = data.loc[(data['Sex'] == sex) & (data['Season'] == season)]
    data_paralel = data_paralel.loc[data_paralel['Year'] >= 1950]

    first = data_paralel[[stat, 'Year', 'Sport', 'Event']]
    first = first.loc[first['Sport'].isin(sports)]
    first['dec'] = first['Year'].map(lambda x: str(x)).str.slice(start=0, stop=3)

    min_val = first.groupby(by=['Sport', 'Event', 'dec'])[stat].mean().min()
    max_val = first.groupby(by=['Sport', 'Event', 'dec'])[stat].mean().max()
    data_group = first.groupby(by=['Sport', 'Event', 'dec'])[stat].mean().unstack().reset_index()
    data_group.fillna(0, inplace=True)
    data_group = data_group.sort_values(by=data_group.columns[2]).reset_index(drop=True)

    lencod = LabelEncoder()
    data_group['Sport_encod'] = lencod.fit_transform(data_group['Sport'])

    dimension = list([dict(range=[0, len(data_group['Event'])],
                           tickvals=pd.Series(list(data_group['Event'].index)),
                           ticktext=data_group['Event'],
                           label='Events',
                           values=pd.Series(list(data_group['Event'].index)))])
    for i in data_group.columns[2:-1]:
        dimension.append(dict(range=[min_val - 5, max_val + 5], label=i + '0', values=data_group[i]))
    if season == 'Summer':
        fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=data_group['Sport_encod'], colorscale='redor'),
            tickfont_size=15,labelfont_size=25, rangefont_size=15,
             dimensions=dimension   ) )
    else:
        fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=data_group['Sport_encod'], colorscale='teal'),
            tickfont_size=15,labelfont_size=25, rangefont_size=15,
             dimensions=dimension   ) )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

@app.callback(
        Output('graph', 'figure'),
        [Input('season_radio','value'),
         Input('drop_continent', 'value')])

def build_graph(value,drop_continent):
    if value == 'Summer':
        data_choropleth = dict(type='choropleth',
                       locations=total_presence['country_x'],
                       # There are three ways to 'merge' your data with the data pre embedded in the map
                       locationmode='country names',
                       z=total_presence['Summer_presences'],
                       text=total_presence['country_x'],
                       colorscale='reds',
                       colorbar_title="Number of Presences",
                       autocolorscale=False,
                       marker_line_color='rgba(0,0,0,0)',
                       hovertemplate = "%{text} <br>Number of Presences: %{z} <extra></extra>"


                       )

        layout_choropleth = dict(geo=dict(scope=drop_continent,  # default
                                  projection=dict(type='equirectangular'
                                                  ),
                                  # showland=True,   # default = True
                                  landcolor='darkgrey',
                                  lakecolor='azure',
                                  showocean=True,  # default = False
                                  oceancolor='white'
                                  ),

                         title=dict(text='Number of Summer Olympic Presences per Country',
                                    x=.5  # Title relative position according to the xaxis, range (0,1)
                                    )
                         )
        fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
        fig_choropleth.update_geos(showcoastlines=False, showsubunits=False, showframe=False)
        return fig_choropleth
    else:
        data_choropleth2 = dict(type='choropleth',
                       locations=total_presence['country_x'],
                       locationmode='country names',
                       z=total_presence['Winter_presences'],
                       text=total_presence['country_x'],
                       colorscale='blues',
                       colorbar_title="Number of Presences",
                       autocolorscale=False,
                       marker_line_color='rgba(0,0,0,0)',
                       hovertemplate = "%{text} <br>Number of Presences: %{z} <extra></extra>"


                       )

        layout_choropleth2 = dict(geo=dict(scope=drop_continent,
                                  projection=dict(type='equirectangular'
                                                  ),
                                  landcolor='darkgrey',
                                  lakecolor='azure',
                                  showocean=True,
                                  oceancolor='white'
                                  ),

                         title=dict(text='Number of winter Olympic Presences per Country',
                                    x=.5
                                    )
                         )
        fig_choropleth2 = go.Figure(data=data_choropleth2, layout=layout_choropleth2)
        fig_choropleth2.update_geos(showcoastlines=False, showsubunits=False, showframe=False)
        return fig_choropleth2


if __name__ == '__main__':
    app.run_server(debug=True)