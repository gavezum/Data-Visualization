import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import LabelEncoder
import dash_bootstrap_components as dbc

path = 'https://raw.githubusercontent.com/gavezum/Data-Visualization/main/data/'

data = pd.read_csv(path+'athlete_events.csv')
total_presence = pd.read_csv(path+'total_presence.csv')
total_medals=pd.read_csv(path+'total_medals.csv')

## Parte Danilo

data["City Games"] = np.where((data["Season"] == "Summer") & (data["Year"] == 1956), "Melbourne", data["City"])

## Parte Tomas

min_year_summer=total_medals.loc[total_medals['Season']=='Summer'].Year.min()
min_year_winter=total_medals.loc[total_medals['Season']=='Winter'].Year.min()

######################################################Interactive Components############################################

var_options = [{'label': 'Number of Events', 'value': 'Event'},
               {'label': 'Number of Athletes', 'value': 'Name'},
               {'label': 'Number of Nationalities', 'value': 'NOC'},
               {'label': 'Number of  Sports', 'value': 'Sport'}]

var_dropdown = dcc.Dropdown(
    id='drop_var',
    options=var_options,
    value='Name'
)

stat_options = dcc.Dropdown(
    id='stat_drop',
    options=[dict(label='Weight',value='Weight'),
             dict(label='Height',value='Height'),
             dict(label='Age',value='Age')],
    value='Weight'
)
sex_options = dbc.RadioItems(
    id='sex_radio',
    options=[dict(label='Male' , value='M'),
             dict(label='Female' , value='F')],
    value='M'
)

season_options = dcc.RadioItems(
    id='season_radio',
    className='radio',
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

slider_year = dcc.Slider(
    id='year_slider',
    min=total_medals['Year'].min(),  # min value in the range slider
    max=total_medals['Year'].max(),  # max value in the range slider
    step=30,
    value=total_medals['Year'].min(),
    marks={str(i): {'label': str(i),
                    'style': {'writing-mode': 'vertical-lr', 'font-size': '15px'}} for i in total_medals.Year.unique()},
    dots=False,
)


##################################################APP###################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.Div([html.Img(src=app.get_asset_url('logo.png'),
                           style={'width': '100%', 'position': 'relative', 'opacity': '80%'})
                  ], id='Logo', style={'width': '20%'}),
        html.Div([html.Label('Evolution of the Olympics')
                  ],  id='Title', style={'width': '60%'}),
        html.Div([html.Br(), html.Br(), season_options
                  ], id='winter_summer', style={'width': '20%'})
    ], id='1_div', style={'display': 'flex', 'height': '8%'}),

    html.Div([
        html.Div([
            html.Label('Choose a variable:'),
            var_dropdown,

            html.Div([
                dcc.Markdown(id='comment')
                    ]),

                ],id='filter', style={'width': '35%', 'display': 'inline-block', 'float': 'left'}),

        html.Div([
            dcc.Graph(id='example-graph'),
                ],id='line_plot', style={'width': '65%' , 'display': 'inline-block'}),
            ],id='2_div',style={'display': 'flex','height':'30%'}),

    html.Div([
        html.Div([
            html.Div([html.Label('Countries with Most Medals Along History')
                  ], className='h2',style={'height':'5%'}),

            html.Div([dcc.Graph(id='stackedbarchart',style={'height':'100%'}),
            ],style={'height':'65%'}),

            html.Div([slider_year
            ],style={'height':'10%'}),

            html.Div([html.Br(),
                html.Label('''The graph displays the cumulative country podiums along the olympics history. The criteria to decide the podium on each olympics event has been based 
                                 solely on the number of gold medals won. \n
                                 As reference, looking at the summer olympics 2016, USA has won 17 times, been second 8 times and third 3 times, based on the 
                                 criteria referred and considering all the summer olympics disputed until the one mentioned.'''),
            ],style={'height':'20%'}),
        ],id='Barplot',style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    html.Label(id='title_map',className='h3', style={'front-size': 'medium'}),
                ], style={'width': '80%'}),
                html.Div([
                    drop_continent,
                    html.Br(),
                ], style={'width': '20%'}),
            ], className='row', style={'display': 'flex'}),
            dcc.Graph(
                id='graph')
        ], id='Map', style={'width': '50%', 'display': 'inline-block'})
    ], id='3_div', style={'display': 'flex', 'height': '30%'}),

    html.Div([
        html.Div([html.Div([html.Label('Choose a Sex:'),
                            sex_options],style={'width': '10%', 'display': 'inline-block'}),
                  html.Div([html.Label('Choose an Event:'),
                            event_drop],style={'width': '60%', 'display': 'inline-block'}),
                  html.Div([html.Label('Choose a Statistic:'),
                            stat_options], style={'width': '30%', 'display': 'inline-block'})
                  ],id='Button',style={'height': '15%','display': 'flex',}),
        html.Div([
                  html.Div([dcc.Graph(id = 'parallel_graph')],style={'width': '88%', 'display': 'inline-block'} ),
                  html.Div([html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Label('''The vertical lines are the mean of the statistic in the decade and the horizontal line shows the evolution of each event along the time.
                                           When a sports do not has an appearance the line will go down and disappear and only return when the event happen''')
                            ],style={'width': '12%', 'display': 'inline-block'} )
                  ],id='Paralel',style={'display': 'flex','height': '85%'})
            ],id='4_div',style={'height':'25%'}),

    html.Div([
        html.Div([html.P(['Group 6', html.Br(),'Danilo Arfelli (20211296), Diogo Tomás Peixoto (20210993), Gabriel Avezum (20210663), João Morais Costa(20211005)'], style={'font-size':'12px'})
                  ],style={'width': '60%'}),
        html.Div([
            html.P(['Sources:', html.Br(),
                    html.A('Olympic games history', href='https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results', target='_blank')], style={'font-size': '12px'})
        ], style={'width': '40%'}),

            ],id='5_div',style={'display': 'flex','height':'2%'})
    ],id= 'Main_Div')

######################################################Callbacks#########################################################

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
    [Output('Title', 'className'),
     Output('4_div', 'className'),
     Output('Map', 'className'),
     Output('Barplot', 'className'),
     Output('2_div', 'className'),
     Output('comment', 'className'),
     Output('5_div', 'className')],
    [Input('season_radio', 'value')]
)
def background(season):
    if season =='Summer':
        title = 'h1_summer'
        class_name = 'box_summer'
    elif season=='Winter':
        title = 'h1_winter'
        class_name = 'box_winter'

    return title, class_name, class_name, class_name, class_name, class_name, class_name

## Gráfico Gabriel

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

    min_val = round(first.groupby(by=['Sport', 'Event', 'dec'])[stat].mean().min(),2)
    max_val = round(first.groupby(by=['Sport', 'Event', 'dec'])[stat].mean().max(),2)
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
        dimension.append(dict(range=[min_val-5,max_val+5],label=i + '0', values=data_group[i]))
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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',width=1300, height=400,margin=dict(l=400, r=60, t=60, b=40)
    )

    return fig







## Gráfico Tomás

@app.callback(
    Output('stackedbarchart', 'figure'),
    [Input('year_slider', 'value'),
     Input('season_radio', 'value')]
)

def update_graph(year,season):
    if ((year>=min_year_summer) and (season=='Summer')):
        filtered_by_olympics_season = total_medals[(total_medals['Season'] == season)]
        filtered_by_olympics_season_year = filtered_by_olympics_season[(filtered_by_olympics_season['Year'] <= year)]
        filtered_by_olympics_season_year = filtered_by_olympics_season_year.groupby(['NOC','Podium']).count().reset_index()
        filtered_by_olympics_season_year = pd.pivot_table(filtered_by_olympics_season_year, values='Medal', index=['NOC'],
                             columns=['Podium'], aggfunc=np.sum, fill_value=0, margins=True)
        filtered_by_olympics_season_year=filtered_by_olympics_season_year.sort_values(by=["All", 1.0, 2.0, 3.0], ascending=True).iloc[-11:-1,:]

        x_bar_g = list(filtered_by_olympics_season_year[1.0].values)
        y_bar_g = list(filtered_by_olympics_season_year.index)
        x_bar_s = list(filtered_by_olympics_season_year[2.0].values)
        y_bar_s = list(filtered_by_olympics_season_year.index)
        x_bar_b = list(filtered_by_olympics_season_year[3.0].values)
        y_bar_b = list(filtered_by_olympics_season_year.index)

        data_gold = dict(type='bar', x=x_bar_g, y=y_bar_g, name='1st Place', marker=dict(color='yellow'), orientation='h')
        data_silver = dict(type='bar', x=x_bar_s, y=y_bar_s, name='2nd Place ', marker=dict(color='gray'), orientation='h')
        data_bronze = dict(type='bar', x=x_bar_b, y=y_bar_b, name='3rd Place', marker=dict(color='brown'), orientation='h')

        data = [data_gold, data_silver, data_bronze]
        bar_data = []

        bar_data.append(data)

        bar_layout = dict(xaxis=dict(title='Count'),
                          yaxis=dict(title='NOC')
                          )
        fig = go.Figure(data=data, layout=bar_layout)

        fig.update_traces(marker_line_width=1.0, opacity=1)
        fig.update_layout(barmode='stack',legend={'traceorder':'normal'})
        fig.update_xaxes(dtick=1)

        return fig

    elif((year >= min_year_winter) and (season == 'Winter')):
        filtered_by_olympics_season=total_medals[(total_medals['Season'] == season)]
        filtered_by_olympics_season_year =  filtered_by_olympics_season[( filtered_by_olympics_season['Year'] <= year)]
        filtered_by_olympics_season_year = filtered_by_olympics_season_year.groupby(
            ['NOC', 'Podium']).count().reset_index()
        filtered_by_olympics_season_year = pd.pivot_table(filtered_by_olympics_season_year, values='Medal',
                                                          index=['NOC'],
                                                          columns=['Podium'], aggfunc=np.sum, fill_value=0,
                                                          margins=True)
        filtered_by_olympics_season_year = filtered_by_olympics_season_year.sort_values(by=["All", 1.0, 2.0, 3.0],
                                                                                        ascending=True).iloc[-11:-1, :]

        x_bar_g = list(filtered_by_olympics_season_year[1.0].values)
        y_bar_g = list(filtered_by_olympics_season_year.index)
        x_bar_s = list(filtered_by_olympics_season_year[2.0].values)
        y_bar_s = list(filtered_by_olympics_season_year.index)
        x_bar_b = list(filtered_by_olympics_season_year[3.0].values)
        y_bar_b = list(filtered_by_olympics_season_year.index)

        data_gold = dict(type='bar', x=x_bar_g, y=y_bar_g, name='1st Place', marker=dict(color='yellow'),
                         orientation='h')
        data_silver = dict(type='bar', x=x_bar_s, y=y_bar_s, name='2nd Place ', marker=dict(color='gray'),
                           orientation='h')
        data_bronze = dict(type='bar', x=x_bar_b, y=y_bar_b, name='3rd Place', marker=dict(color='brown'),
                           orientation='h')

        data = [data_gold, data_silver, data_bronze]
        bar_data = []

        bar_data.append(data)

        bar_layout = dict(xaxis=dict(title='Count'),
                          yaxis=dict(title='NOC')
                          )
        fig = go.Figure(data=data, layout=bar_layout)

        fig.update_traces(marker_line_width=1.0, opacity=1)
        fig.update_layout(barmode='stack', legend={'traceorder': 'normal'})
        fig.update_xaxes(dtick=1)

        return fig

    else:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No Olympic Games disputed this year",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }









## Gráfico João

@app.callback(
        [Output('graph', 'figure'),
         Output('title_map', 'children')],
        [Input('season_radio','value'),
         Input('drop_continent', 'value')])

def build_graph(value,drop_continent):
    title = 'Number of ' + str(value) + ' Olympic presences per country'

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

                         #title=dict(text='Number of Summer Olympic Presences per Country',
                                   # x=.5  # Title relative position according to the xaxis, range (0,1)
                                   # )
                         )
        fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
        fig_choropleth.update_geos(showcoastlines=False, showsubunits=False, showframe=False)
        fig_choropleth.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',width=700, height=400,margin=dict(l=0, r=0, t=0, b=0) )
        return fig_choropleth, title
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

                         #title=dict(text='Number of winter Olympic Presences per Country',
                         #          x=.5
                         #          )
                         )
        fig_choropleth2 = go.Figure(data=data_choropleth2, layout=layout_choropleth2)
        fig_choropleth2.update_geos(showcoastlines=False, showsubunits=False, showframe=False)
        fig_choropleth2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)' )
        return fig_choropleth2, title

## Gráfico Danilo

@app.callback(
    [
        Output(component_id='example-graph', component_property='figure'),
        Output('comment', 'children'),
    ],
    [Input(component_id='season_radio', component_property='value'),
     Input(component_id='drop_var', component_property='value'),
     ]
)
def callback_1(input_value, input_value2):
    df_bar = data.loc[(data['Season'] == input_value)]
    df_bar = pd.pivot_table(df_bar, values=[input_value2],
                            index=["Year", "City Games"],
                            aggfunc='nunique', fill_value=0).reset_index()

    if input_value2 == "NOC":
        nome_graph = "Nationalities"
    elif input_value2 == "Event":
        nome_graph = "Events"
    elif input_value2 == "Name":
        nome_graph = "Athletes"
    elif input_value2 == "Sport":
        nome_graph = "Sports"

    fig1 = px.line(data_frame=df_bar,
                   x="Year",
                   y=input_value2,
                   markers=True,
                   title=('Evolution of ' + nome_graph + " Over time"),
                   custom_data=['City Games']
                   )

    fig1.update_layout(
        title=dict(font=dict(size=25) ),
        title_x=0.5,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis_title="Olympic Year",
        yaxis_title="Quantity of " + nome_graph,
        yaxis=dict(showline=True, linecolor='black', linewidth=1),
        xaxis=dict(showline=True, linecolor='black', linewidth=1),
    )


    aux_y1 = df_bar.iloc[:, 2].max()
    if input_value == "Summer":
        fig1.update_traces(marker=dict(color='firebrick', size=10),
                           line=dict(color='firebrick', width=3),
                           hovertemplate="Local: %{customdata[0]} <br>" +
                                         "Year: %{x} <br>" +
                                         "Quantity %{y} <br>")

        fig1.add_shape(type="line", y0=aux_y1, y1=aux_y1,
                       x0=1914, x1=1918,
                       line=dict(color="coral", width=5)
                       )
        fig1.add_annotation(  # add a text callout with arrow
            text="World War I", x=1914 + ((1918 - 1914) / 2), y=aux_y1, arrowhead=1, showarrow=True
        )

        fig1.add_shape(type="line", y0=aux_y1, y1=aux_y1, x0=1939, x1=1945,
                       line=dict(color="coral", width=5)
                       )
        fig1.add_annotation(  # add a text callout with arrow
            text="World War II", x=1939 + ((1945 - 1939) / 2), y=aux_y1, arrowhead=1, showarrow=True
        )

    if input_value != "Summer":

        fig1.update_traces(marker=dict(color='DarkBlue', size=10),
                           line=dict(color='DarkBlue', width=3),
                           hovertemplate="Local: %{customdata[0]} <br>" +
                                         "Year: %{x} <br>" +
                                         "Quantity %{y} <br>")

        fig1.add_shape(type="line", y0=aux_y1, y1=aux_y1,
                       x0=1939, x1=1945,
                       line=dict(color="LightSalmon", width=5)
                       )
        fig1.add_annotation(  # add a text callout with arrow
            text="World War II", x=1939 + ((1945 - 1939) / 2), y=aux_y1, arrowhead=1, showarrow=True
        )
    if input_value == "Summer":
        comment = [''' During the world war I and II the olympics were  
                    canceled (1916, 1940, 1944).
                   '''
                   ]
        if input_value2 == "Event":
            comment = [''' 
            During the world war I and II the olympics were canceled (1916, 1940, 1944). \n
            Tendency of increase the number of events over the years.
            '''
                       ]
        if input_value2 == "NOC":
            comment = [''' 
            During the world war I and II the olympics were canceled (1916, 1940, 1944). \n
            Tendency of increase the number of nations over the years but in 1976 and 1980 decreases because:\n
            **1976:** In protest against the ongoing All Blacks tour of apartheid-era South Africa, the African 
            nations demanded that the exclusion of New Zealand from Olympics. After the IOCs refusal, 28 nations
            responded with a boycott. \n
            **1980:** the United States led a boycott Olympic Games  to protest the late 1979 Soviet invasion of 
            Afghanistan. In total,  65 nations refused to participate in the games.
            '''
                       ]

            fig1.add_shape(type="circle", y0=60, y1=110, x0=1973, x1=1983,
                            xref="x", yref="y",
                           opacity=0.2,
                           fillcolor="orange",
                           line_color="orange"
                           )

        if input_value2 == "Name":
            comment = ['''
            During the world war I and II the olympics were canceled (1916, 1940, 1944). \n
            Tendency of increase the number of athletes over the years but we observe that decrease in 4 years
            1932,1956 and 1980. \n
            **1932:** The poor participation was the result of the worldwide economic depression and the expense 
            of traveling to California. \n
            **1956:** were affected by a number of boycotts due to the Suez Crisis (Egypt, Iraq, Lebanon - out), 
            Hungarian Revolution (Netherlands, Spain, Switzerland- out) and China chose to boycott the event 
            because Taiwan.\n 
            **1980:** the United States led a boycott Olympic Games  to protest the late 1979 Soviet invasion of 
            Afghanistan. In total, 65 nations refused to participate in the games. '''
                       ]
            fig1.add_shape(type="circle", y0=1322, y1=2522, x0=1929, x1=1935,
                           xref="x", yref="y",
                           opacity=0.2,
                           fillcolor="orange",
                           line_color="orange"
                           )

            fig1.add_shape(type="circle", y0=2746, y1=3946, x0=1953, x1=1959,
                           xref="x", yref="y",
                           opacity=0.2,
                           fillcolor="orange",
                           line_color="orange"
                           )

            fig1.add_shape(type="circle", y0=4652, y1=5852, x0=1977 , x1=1983,
                           xref="x", yref="y",
                           opacity=0.2,
                           fillcolor="orange",
                           line_color="orange"
                           )

        if input_value2 == "Sport":
            comment = ['''
            During the world war I and II the olympics were canceled (1916, 1940, 1944). \n
            Tendency of increase the number of sports starting after world war II. \n
            In the beginning of the Olympics games we can se a high variation of sports some of the the old
            sports disappeared completely from the Olympic schedule such as: Tug of War, Ballooning, Korfball,
            pelota and live pigeon shooting.
            '''
                       ]

    if input_value != "Summer":
        fig1.add_vrect(
            x0=1992, x1=1994 ,
            fillcolor="lightsteelblue", opacity=0.5,
            layer="below", line_width=0,
        ),

        comment =  ['''
        During the world war II the olympics were canceled (1940, 1944).    \n
        Tendency of increase over the years.         \n   
        The Winter and Summer Olympic Games were held in the same years until 1992,
        after a 1986 decision by the International Olympic Committee (IOC) to place the 
        Summer and Winter Games on separate four-year cycles in alternating even-numbered years. 
        Because of the change, the next Winter Olympics after 1992 were in 1994.         
                     '''
                     ]

    return fig1, comment

if __name__ == '__main__':
    app.run_server(debug=True)