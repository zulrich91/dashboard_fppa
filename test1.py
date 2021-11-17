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
from app import app
from collections import OrderedDict
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import *


##### Nations Dataset ############
country_managers_df = pd.read_csv("./data/ManagerPlayerMatchesStat.csv")
country_passings_df = pd.read_csv('./data/AllPassingMatchesStat.csv')
#######################################
player_attack_df = pd.read_csv("./data/attaque.csv", header=0)
#player_stats_df = pd.read_csv("./data/player_stats2.csv", header=0)
player_stats_df = pd.read_csv("./data/joueurs_stats_pct.csv", header=0)
player_perso_df = pd.read_csv("./data/stats_perso.csv", header=0)
player_defense_df = pd.read_csv("./data/defense.csv", header=0)
player_keeper_df = pd.read_csv("./data/5_BIG_EUROPEAN_LEAGUES_KEEPERS.csv",header=0)
player_compare_comp_df=pd.read_csv("./data/player_compare_competition.csv", header=0)
player_compare_manager_df=pd.read_csv("./data/player_compare_manager.csv", header=0)
player_compare_captain_df = pd.read_csv("./data/player_compare_captain.csv", header=0)
player_compare_annee_comp_df = pd.read_csv("./data/player_compare_annee_competition.csv", header=0)

external_stylesheets = [dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout_joueur = html.Div(children=[

        dcc.Tabs(id='tabs',value='tab-1',children=[
            dcc.Tab(value='tab-1',label="Comparaison Joueurs", children=[
                html.Div([
                    html.Div([dcc.Dropdown(id='player1-dropdown', placeholder='Select Player', style=dict(width='100%'),
                            options=[{ "label":i, 'value':i} for i in player_stats_df[player_stats_df.columns[1]].unique()],
                            value=player_stats_df[player_stats_df.columns[1]].unique()[0],
                            )],style=dict(width='49%',marginTop=4,marginBottom=4)), 
                    html.Div([dcc.Dropdown(id='player2-dropdown',style=dict(width='100%'),
                                # options=[{ "label":i, 'value':i} for i in player_stats_df[player_stats_df.columns[1]].unique()],
                                #value=player_stats_df[player_stats_df.columns[1]].unique()[1],
                                value='Lionel-Messi',
                            )],style=dict(width='50%',marginTop=4,marginBottom=4,marginLeft=6, paddingRight=5,backgroundColor='white'))
                ], className='row flex-display',style=dict(marginLeft=1)),

                html.Div(id="player_polar_chart_div", 
                        style=dict(display="inline-block")),
            ]),
            dcc.Tab(value='tab-2',label="Exploration Joueurs", children=[
                dcc.Dropdown(id='select-player-to-explore-dropdown',
                        options=[{ "label":i, 'value':i} for i in player_compare_comp_df[player_compare_comp_df.columns[1]].unique()],
                        value=player_compare_comp_df[player_compare_comp_df.columns[1]].unique()[0],
                        style={'width':'200px',
                                "marginTop":"5px", 
                                "marginBottom":"5px",
                                'background-color':'white'}),
                # dcc.Dropdown(id='auto_dropdown',
                #             options = [{"label":i, 'value':i} for i in ['a', 'b', 'c']],
                #             value="a"),
                html.Div(id='player-explore-div',children=[]),
            ]),

        ######## TAB 3 ######################################
            dcc.Tab(value='tab-3', label='Les Nations',children=[
                dcc.Tabs([
                    dcc.Tab(value='tab-3-2',label='Joueur', children=[
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
                    dcc.Tab(value='tab-3-1', label='Nation', children=[
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
            ]),
        ########## End TAB 3 #################################
        ],style=dict(width='100%',margin=2))
])

######################## Nations Callbacks     ###########################

@app.callback(
    Output(component_id="country1-div", component_property="children"),
    [Input(component_id="country_player1-dropdown",component_property="value"),
    Input(component_id="country_country1-dropdown",component_property="value")]
)
def country_player1_stats(player,country):
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

    return [dcc.Graph(figure=fig,style=dict(margin='2px')),
            dcc.Graph(figure=fig2,style=dict(margin='2px')),
            dcc.Graph(figure=fig3,style=dict(margin='2px'))]


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
    return [dcc.Graph(figure=fig,style=dict(margin='2px')),
            dcc.Graph(figure=fig2,style=dict(margin='2px')),
            dcc.Graph(figure=fig3,style=dict(margin='2px'))]


######################## End    ###########################



@app.callback(
  Output(component_id='player2-dropdown', component_property='options'),
  Input(component_id='player1-dropdown', component_property='value')  
)
def update_dropdown_options(player1):
    position = player_stats_df[player_stats_df['Joueur']==player1]['Position'].values[0]
    dropdown_df = player_stats_df[player_stats_df["Position"]==position]
    return [{"label":i, 'value':i} for i in dropdown_df['Joueur'].unique()]


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
                   z=player_manager_df[player_manager_df.columns[4:12]].iloc[-10:,],
                   x=player_manager_df.columns[4:12],
                   y=player_manager_df[player_manager_df.columns[3]].iloc[-10:,].values.tolist(),
                   hoverongaps = False)
                ).update_layout(title=player+ " performance by manager")

    player_captain_df = player_compare_captain_df[player_compare_captain_df['player']==player]
    fig3 = go.Figure(data=go.Heatmap(
                   z=player_captain_df[player_captain_df.columns[3:]].iloc[-10:,],
                   x=player_captain_df.columns[3:],
                   y=player_captain_df[player_captain_df.columns[2]].iloc[-10:,].values.tolist(),
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
    
                html.Div(
                    [   html.Div([dcc.Graph(figure=fig3)],style=dict(margin=5,width='49%')),
                        html.Div([dcc.Graph(figure=fig4)],style=dict(margin=5,width='49%'))
                    ], className='row flex-diplay',style=dict(marginLeft=1)), 

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

    fields_of_interest = ['Joueur', 'Position', 'Taille', 'Poid', 'Lieu de naissance', 'Club','Pied fort', 'Age','Biographie']
    player1_image = player_perso_df[player_perso_df['Joueur']==player1]['url_de_image']
    player2_image = player_perso_df[player_perso_df['Joueur']==player2]['url_de_image']
    player1_info = player_perso_df[player_perso_df['Joueur']==player1][fields_of_interest]
    player2_info = player_perso_df[player_perso_df['Joueur']==player2][fields_of_interest]
    player1_bio = get_player_bio(player1_info)
    player2_bio = get_player_bio(player2_info)
    player1_position = get_player_position(player1_info)
    player2_position = get_player_position(player2_info)
    players_polar_fig = players_build_polar_chart(player_stats_df, player1, player2)
    player1_img = get_player_img(player1_image)
    player2_img = get_player_img(player2_image)
    player1_fig = get_player_figure(player1, player1_position,player_attack_df,player_defense_df)
    player2_fig = get_player_figure(player2, player2_position,player_attack_df,player_defense_df)
    fig = html.Div([
        html.Div([
            html.Div([
                    html.Div([
                        html.Img(src=player1_img, style=dict(width='100px',height='215px'))
                    ],className='card_container two columns',style=dict(marginRight=1,marginTop=2,width='120px',height='235px')),
                    
                    html.Div([html.P(children=[player1_bio])
                    ],className='card_container nine columns',style=dict(margin=1,width='520px',height='236.19px')),    
            ],style=dict(width='645px',height='236.19px')),
            
            html.Div([
                    html.Div([
                        html.Img(src=player2_img, style=dict(width='100px',height='215px'))
                    ],className='card_container two columns',style=dict(marginTop=2,width='120px',marginRight=1,marginLeft=1,height='235px')),
                    
                    html.Div([html.P(children=[player2_bio])
                    ],className='card_container nine columns',style=dict(margin=1,width='521px',height='236.19px')),    
            ],style=dict(width='646px',height='236.19px')),
        ],style=dict(marginBottom=10,marginLeft=3),className='row flex-display'),

        html.Div([  
            html.Div([dcc.Graph(id="player_polar_chart", figure=players_polar_fig,
                        style=dict(width='427px',margin="1px",height='454px'))]),

            html.Div([dcc.Graph(id="player1_bar_chart", figure=player1_fig, 
                        style=dict(width='427px',height='454px',margin="1px"))]),
            
            html.Div([dcc.Graph(id="player2_bar_chart",figure=player2_fig, 
                        style=dict(width='430px',margin="1px",height='454px'))], style={'border-radius':'10px'}), 
        ], className='row flex-display', style=dict(marginLeft='4px',marginRight='1px')),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([html.Label('Nom'),player1_info['Joueur'].values[0]],
                            className='card_container two columns',style=dict(margin=1, width='25%')),
                    html.Div([html.Label('Pays'),player1_info['Lieu de naissance'].values[0].split(",")[-1]],
                            className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Club'),player1_info['Club'].values[0]],
                            className='card_container two columns',style=dict(margin=1, width='25%')),
                    html.Div([html.Label('Age'),player1_info['Age'].values[0]],
                            className='card_container two columns',style=dict(margin=1)),
                    
                ], className='row flex-display', style=dict(marginLeft=4,width='100%')),
                html.Div([
                    html.Div([html.Label('Position'),player1_info['Position'].values[0]],className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Pied'),player1_info["Pied fort"].values[0]],className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Taille'),player1_info["Taille"].values[0]],className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Poids'),player1_info["Poid"].values[0]],className='card_container two columns',style=dict(margin=1)),
                ],className='row flex-display', style=dict(width='100%',marginLeft=4)),
            ],style=dict(width='646px')),

            html.Div([
                html.Div([
                    html.Div([html.Label('Nom'),player2_info['Joueur'].values[0]],
                            className='card_container two columns',style=dict(margin=1, width='25%')),
                    html.Div([html.Label('Pays'),player2_info['Lieu de naissance'].values[0].split(",")[-1]],
                            className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Club'),player2_info['Club'].values[0]],
                            className='card_container two columns',style=dict(margin=1, width='25%')),
                    html.Div([html.Label('Age'),player2_info['Age'].values[0]],
                            className='card_container two columns',style=dict(margin=1)),
                    
                ], className='row flex-display', style=dict(marginLeft=4,width='100%')),
                html.Div([
                    html.Div([html.Label('Position'),player2_info['Position'].values[0]],className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Pied'),player2_info["Pied fort"].values[0]],className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Taille'),player2_info["Taille"].values[0]],className='card_container two columns',style=dict(margin=1)),
                    html.Div([html.Label('Poids'),player2_info["Poid"].values[0]],className='card_container two columns',style=dict(margin=1)),
                ],className='row flex-display', style=dict(width='100%',marginLeft=4)),
            ],style=dict(width='646px')),
        ],className='row flex-display',style=dict(margin='2px')),
        

    ])
    return fig


app.layout=layout_joueur


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0',port=5002)