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

player_attack_df = pd.read_csv("./data/attaque.csv", header=0)
player_stats_df = pd.read_csv("./data/player_stats2.csv", header=0)
player_perso_df = pd.read_csv("./data/stats_perso.csv", header=0)
player_defense_df = pd.read_csv("./data/defense.csv", header=0)
player_compare_comp_df=pd.read_csv("./data/player_compare_competition.csv", header=0)
player_compare_manager_df=pd.read_csv("./data/player_compare_manager.csv", header=0)
player_compare_captain_df = pd.read_csv("./data/player_compare_captain.csv", header=0)
player_compare_annee_comp_df = pd.read_csv("./data/player_compare_annee_competition.csv", header=0)

layout_joueur = html.Div(children=[

        dcc.Tabs(id='tabs',value='tab-1',children=[
            dcc.Tab(value='tab-1',label="Compare Players", children=[
                html.Div([
                    html.Div([dcc.Dropdown(id='player1-dropdown', placeholder='Select Player', style=dict(width='100%'),
                            options=[{ "label":i, 'value':i} for i in player_stats_df[player_stats_df.columns[1]].unique()],
                            value=player_stats_df[player_stats_df.columns[1]].unique()[0],
                            )],style=dict(width='49%',marginTop=4,marginBottom=4)), 
                    html.Div([dcc.Dropdown(id='player2-dropdown',style=dict(width='100%'),
                                options=[{ "label":i, 'value':i} for i in player_stats_df[player_stats_df.columns[1]].unique()],
                                value=player_stats_df[player_stats_df.columns[1]].unique()[1],
                            )],style=dict(width='50%',marginTop=4,marginBottom=4,marginLeft=6, paddingRight=5))
                ], className='row flex-display',style=dict(marginLeft=1)),

                html.Div(id="player_polar_chart_div", 
                        style=dict(display="inline-block")),
            ]),
            dcc.Tab(value='tab-2',label="Explore Players", children=[
                # html.Div([
                    dcc.Dropdown(id='select-player-to-explore-dropdown',
                            options=[{ "label":i, 'value':i} for i in player_compare_comp_df[player_compare_comp_df.columns[1]].unique()],
                            value=player_compare_comp_df[player_compare_comp_df.columns[1]].unique()[0],
                            
                            style={
                                    'width':'200px',
                                    "marginTop":"5px", 
                                    "marginBottom":"5px",
                                    'background-color':'white'}),
                    # ]),
                    dcc.Dropdown(id='auto_dropdown',
                                options = [{"label":i, 'value':i} for i in ['a', 'b', 'c']],
                                value="a"        
                    ),
                html.Div(id='player-explore-div',children=[]),
            ])
        ],style=dict(width='100%',margin=2))
])

@app.callback(
  Output(component_id='auto_dropdown', component_property='options'),
  Input(component_id='select-player-to-explore-dropdown', component_property='value')  
)
def update_dropdown_options(dropdown1):

    return [{"label":i, 'value':i} for i in ['x', 'y', 'z', dropdown1]]


@app.callback(
    Output(component_id='player-explore-div', component_property='children'),
    Input(component_id='select-player-to-explore-dropdown', component_property='value')
)
def player_exploration(player):
    global player_compare_comp_df
    global player_compare_manager_df

    player_comp_df = player_compare_comp_df[player_compare_comp_df['player']==player]
    fig1 = px.bar(player_comp_df,
                    x='comp', 
                    y=player_comp_df.columns[3:],
                    title=player+' performance by competition',
                    )

    player_manager_df = player_compare_manager_df[player_compare_manager_df['player']==player]
    fig2 = go.Figure(data=go.Heatmap(
                   z=player_manager_df[player_manager_df.columns[3:]],
                   x=player_manager_df.columns[3:],
                   y=player_manager_df[player_manager_df.columns[2]].values.tolist(),
                   hoverongaps = False)
                ).update_layout(title=player+ " performance by manager")

    player_captain_df = player_compare_captain_df[player_compare_captain_df['player']==player]
    fig3 = go.Figure(data=go.Heatmap(
                   z=player_captain_df[player_captain_df.columns[3:]],
                   x=player_captain_df.columns[3:],
                   y=player_captain_df[player_captain_df.columns[2]].values.tolist(),
                   hoverongaps = True)
                ).update_layout(title=player+" performance by captain")

    player_annee_comp_df = player_compare_annee_comp_df[player_compare_annee_comp_df['player']==player]
    fig4 = px.bar(player_annee_comp_df, 
                    x='year', 
                    y='average point by temp',
                    color='comp',
                    title=player+' performance by year and competition').update_layout(xaxis=dict(title="year",
                                                            linecolor="#BCCCDC",  # Sets color of X-axis line
                                                            showgrid=False  # Removes X-axis grid lines
                                                        ),
                                                yaxis=dict(
                                                    linecolor="#BCCCDC",  # Sets color of Y-axis line
                                                    showgrid=False,  # Removes Y-axis grid lines
                                               
    ))
    all_divs = html.Div(children=[

                html.Div(
                    [   html.Div([dcc.Graph(figure=fig1)],style=dict(margin=5,width='49%')),
                        html.Div([dcc.Graph(figure=fig2)],style=dict(margin=5,width='49%'))
                    ], className='row flex-diplay', style=dict(marginLeft=1)),

                # html.Div([dcc.Graph(figure=fig2,style=dict(width="50%"))]),
    
                html.Div(
                    [   html.Div([dcc.Graph(figure=fig3)],style=dict(margin=5,width='49%')),
                        html.Div([dcc.Graph(figure=fig4)],style=dict(margin=5,width='49%'))
                    ], className='row flex-diplay',style=dict(marginLeft=1)), 

                # html.Div([dcc.Graph(figure=fig4,style=dict(width=600))],style=dict(float='right'))
            ])
    return all_divs

@app.callback(
    Output(component_id="player_polar_chart_div", component_property='children'),
    Input(component_id='player2-dropdown', component_property='value'),
    [State(component_id='player1-dropdown', component_property='value')]
)
def player_performance(player2, player1):
    global player_stats_df
    global player_perso_df
    players_polar_fig = players_build_polar_chart(player_stats_df, player1, player2)
    fields_of_interest = ['Joueur', 'Position', 'Taille', 'Poid', 'Lieu de naissance', 'Club','Pied fort', 'Age','Biographie']
    player1_image = player_perso_df[player_perso_df['Joueur']==player1]['url_de_image']
    player2_image = player_perso_df[player_perso_df['Joueur']==player2]['url_de_image']
    player1_info = player_perso_df[player_perso_df['Joueur']==player1][fields_of_interest]
    player2_info = player_perso_df[player_perso_df['Joueur']==player2][fields_of_interest]
    player1_bio = get_player_bio(player1_info)
    player2_bio = get_player_bio(player2_info)
    player1_position = get_player_position(player1_info)
    player2_position = get_player_position(player2_info)
    player1_img = get_player_img(player1_image)
    player2_img = get_player_img(player2_image)
    player1_fig = get_player_figure(player1, player1_position,player_attack_df,player_defense_df)
    player2_fig = get_player_figure(player2, player2_position,player_attack_df,player_defense_df)
    fig = html.Div([

        html.Div([dcc.Graph(id="player_polar_chart", 
                    figure=players_polar_fig,
                    )
        ]),

        html.Div([
            html.Div([
                    html.Div([
                        html.Img(src=player1_img, style=dict(width=100))
                    ],className='card_container two columns',style=dict(marginRight=1,marginTop=2,width='25%')),
                    
                    html.Div([html.P(children=[player1_bio])
                    ],className='card_container nine columns',style=dict(margin=1,width='72%')),    
            ],style=dict(width='50%')),
            
            html.Div([
                    html.Div([
                        html.Img(src=player2_img, style=dict(width=100))
                    ],className='card_container two columns',style=dict(marginTop=2,width='25%')),
                    
                    html.Div([html.P(children=[player2_bio])
                    ],className='card_container nine columns',style=dict(margin=1,width='70%')),    
            ],style=dict(width='50%')),
        ],style=dict(marginBottom=10,marginLeft=3,width='100%'),className='row flex-display'),

        html.Div([        
            html.Div(id="player1_details_div",children=[
                html.Div(style=dict(),children=[
                        generate_players_data_table1(player1_info)]),
                html.Div(style=dict(marginTop='10px'),children=[
                        generate_players_data_table2(player1_info)]),
                html.Div(style=dict(marginTop=5),children=[
                    # html.P(["Nationality: ", player1_info['Lieu de naissance'].values[0].split(",")[-1]]),
                    dcc.Graph(id="player1_bar_chart", 
                            figure=player1_fig)]),
            ],style=dict(marginLeft=6)),
            

            html.Div(id="player2_details_div", children=[
                
                html.Div(style=dict(),children=[
                    generate_players_data_table1(player2_info)]),
                html.Div(style=dict(marginTop='10px'),children=[
                    generate_players_data_table2(player2_info)]),
                html.Div(style=dict(marginTop=5),children=[
                    # html.P(["Player: ", player2_info['Joueur'].values[0]]),
                    dcc.Graph(id="player2_bar_chart", 
                                figure=player2_fig)])
            ],style=dict(margin=4))
        ],className='row flex-display',style=dict(marginTop=20)),
    ])
    return fig
