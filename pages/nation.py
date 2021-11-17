from app import app
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
from collections import OrderedDict
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import *

##### Nations Dataset ############
country_managers_df = pd.read_csv("./data/ManagerPlayerMatchesStat.csv")
country_passings_df = pd.read_csv('./data/AllPassingMatchesStat.csv')
country_meteo_df = pd.read_csv("./data/weatherallcity.csv")

#######################################

######## Nations Layout ###############################
layout_nation = dcc.Tabs(value='tab-1',children=[
                    dcc.Tab(value='tab-1',label='Joueur', children=[
                        html.Div([
                            dcc.Dropdown(id='country_player1-dropdown',
                                        options = [{"label":i, 'value':i} for i in country_managers_df['Player'].unique()],
                                        value=country_managers_df['Player'].unique()[0],
                                        style=dict(width='645px',marginTop=4,marginBottom=4)),
                            dcc.Dropdown(id='country_player2-dropdown',
                                        options = [{"label":i, 'value':i} for i in country_managers_df['Player'].unique()],
                                        value=country_managers_df['Player'].unique()[10],
                                        style=dict(width='645px',marginTop=4,marginBottom=4)),
                        ],className='row flex-display',style=dict(width='100%',marginLeft='4px')),
                        html.Div([
                            html.Div(id='country1-div',style=dict(width='645px')),
                            html.Div(id='country2-div',style=dict(width='645px')),
                        ],className='row flex-display',style=dict(width='100%',marginLeft='4px')),
                    ]),
                    dcc.Tab(value='tab-2', label='Nation', children=[
                        html.Div([
                            dcc.Dropdown(id='country_country1-dropdown',
                                        options = [{"label":i, 'value':i} for i in country_managers_df['Country'].unique()],
                                        value=country_managers_df['Country'].unique()[0],
                                        style=dict(width='645px',marginTop=4,marginBottom=4)),
                            dcc.Dropdown(id='country_country2-dropdown',
                                        options = [{"label":i, 'value':i} for i in country_managers_df['Country'].unique()],
                                        value=country_managers_df['Country'].unique()[10],
                                        style=dict(width='645px',marginTop=4,marginBottom=4)),
                        ],className='row flex-display',style=dict(width='100%',marginLeft='4px')),
                        html.Div([
                            html.Div(id='country-country1-div',style=dict(width='645px')),
                            html.Div(id='country-country2-div',style=dict(width='645px')),
                        ],className='row flex-display',style=dict(width='100%',marginLeft='4px')),
                    ]),

                ]),
####################### End ###################################


######################## Nations Callbacks     ###########################

@app.callback(
    Output(component_id='country-country1-div',component_property='children'),
    Input(component_id='country_country1-dropdown',component_property='value')
)
def meteo_pays(country):
    global country_meteo_df
    country_meteo = country_meteo_df[country_meteo_df['Country']==country]
    try:
        country_meteo = country_meteo.groupby(['Country','Date'])['GF','temp','Result'].min().reset_index()
        fig = px.line(country_meteo.sort_values(by='temp'), 
                        x='temp', y='GF',color='Result',title='Meteo effects on Country: '+country).update_layout()
        graph = dcc.Graph(figure=fig)
    except Exception as e:
        print(e)
        graph = 'Donne Meteo Pas encore disponible pour : '+ country
    return graph


@app.callback(
    Output(component_id="country1-div", component_property="children"),
    Input(component_id="country_player1-dropdown",component_property="value")
)
def country_player1_stats(player):
    user_click = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    print(user_click)
    global country_managers_df

    df = country_managers_df[country_managers_df['Player']==player].\
                    groupby('Manager1').sum('Min').reset_index().sort_values(by='Min',ascending=False)
    top5 = df.iloc[:6,:]
    fig = px.bar(top5, x='Manager1',y='Min', title=player +": Top Temps de Jeu Par entraineur").\
            update_layout(yaxis={'title':'Temps de jeu (Minutes)'},
                                xaxis={'title':'Entraineur'})


    player_df = country_managers_df[country_managers_df['Player']==player]
    country = player_df['Country'].values[0]
    df = country_managers_df[country_managers_df['Country']==country].\
                groupby('Player').sum('Min').reset_index().sort_values(by='Min', ascending=False)
    df = df.reset_index(drop=True)
    index_player = df[df['Player'] == player].index[0]
    fig2 = px.bar(df.iloc[0:index_player+1], 
                    x='Player', y='Min',title=player+" ="+str(index_player+1)+": En terme de temps de jeu").\
                update_layout(yaxis={'title':'Temps de jeu (Minutes)'},
                                xaxis={'title':'Nom du Joueur'})

    player_passing_df = country_passings_df[country_passings_df['Player']==player]
    fig3 = px.bar(player_passing_df, x='Comp', y="Cmp%",title=player+': Pourcentage de passe reussi par competition').\
                    update_layout(xaxis={'title':"Competition"},yaxis={'title':"% Passe Reussi"})

    try:

        country_meteo_joueur = country_meteo_df[country_meteo_df['Player']==player]
        country_meteo_joueur = country_meteo_joueur.groupby(['Date'])['GF','temp','Result'].min().reset_index()
        fig4 = px.line (country_meteo_joueur.sort_values(by='temp'), x='temp', y='GF',color='Result'
                        ,title='Meteo effects on player: '+player )
        fig4 = dcc.Graph(figure=fig4,style=dict(margin='2px'))
    except Exception as e:
        fig4 = 'Donne Meteo Pas encore disponible pour : '+ player

    return [dcc.Graph(figure=fig,style=dict(margin='2px')),
            dcc.Graph(figure=fig2,style=dict(margin='2px')),
            dcc.Graph(figure=fig3,style=dict(margin='2px')),fig4]


@app.callback(
    Output(component_id="country2-div", component_property="children"),
    Input(component_id="country_player2-dropdown",component_property="value")
)
def country_player2_stats(player):
    global country_managers_df

    df = country_managers_df[country_managers_df['Player']==player].\
                    groupby('Manager1').sum('Min').reset_index().sort_values(by='Min',ascending=False)
    top5 = df.iloc[:6,:]
    fig = px.bar(top5, x='Manager1',y='Min', title=player +": Top Temps de Jeu Par entraineur").\
            update_layout(yaxis={'title':'Temps de jeu (Minutes)'},
                                xaxis={'title':'Entraineur'})


    player_df = country_managers_df[country_managers_df['Player']==player]
    country = player_df['Country'].values[0]
    df = country_managers_df[country_managers_df['Country']==country].\
                groupby('Player').sum('Min').reset_index().sort_values(by='Min', ascending=False)
    df = df.reset_index(drop=True)
    index_player = df[df['Player'] == player].index[0]
    fig2 = px.bar(df.iloc[0:index_player+1], 
                    x='Player', y='Min',title=player+" ="+str(index_player+1)+": En terme de temps de jeu").\
                update_layout(yaxis={'title':'Temps de jeu (Minutes)'},
                                xaxis={'title':'Nom du Joueur'})

    player_passing_df = country_passings_df[country_passings_df['Player']==player]
    fig3 = px.bar(player_passing_df, x='Comp', y="Cmp%",title=player+': Pourcentage de passe reussi par competition').\
                    update_layout(xaxis={'title':"Competition"},yaxis={'title':"% Passe Reussi"})

    try:
        country_meteo_joueur = country_meteo_df[country_meteo_df['Player']==player]
        country_meteo_joueur = country_meteo_joueur.groupby(['Date'])['GF','temp','Result'].min().reset_index()
        fig4 = px.line(country_meteo_joueur.sort_values(by='temp'), x='temp', y='GF',color='Result'
        ,title='Meteo effects on player: '+player )
        fig4 = dcc.Graph(figure=fig4,style=dict(margin='2px'))
    except Exception as e:
        fig4 = 'Donne Meteo Pas encore disponible pour : '+ str(player)

    return [dcc.Graph(figure=fig,style=dict(margin='2px')),
            dcc.Graph(figure=fig2,style=dict(margin='2px')),
            dcc.Graph(figure=fig3,style=dict(margin='2px')),fig4]


######################## End    ###########################