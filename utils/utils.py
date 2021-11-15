import plotly.graph_objects as go
import unidecode
import dash_table
import plotly.express as px

def unidecodePlayersName(name):
    players_name = unidecode.unidecode(name)
    return players_name


def get_selected_players(df, player1, player2):
    selected_player1 = df[df[df.columns[1]] == player1]
    selected_player2 = df[df[df.columns[1]] == player2]
    selected_player1 = get_years_of_interest(selected_player1, "-2021")
    selected_player2 = get_years_of_interest(selected_player2, "-2021")
    return selected_player1, selected_player2

def get_years_of_interest(df, year_str='-2021'):
    df = df[df['Annees'].str.contains(year_str, na=False)]
    return df.values.tolist()[0][4:]

def players_build_polar_chart(df,player1,player2):
    categories = df.columns[4:]
    selected_player1, selected_player2 = get_selected_players(df,player1,player2)
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=selected_player1,
        theta=categories,
        fill='toself',
        name=player1
    ))

    fig.add_trace(go.Scatterpolar(
        r=selected_player2,
        theta=categories,
        fill='toself',
        name=player2
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            )),
        showlegend=True)
    return fig

def get_player_figure(player, player_position, player_attack_df, player_defense_df):
    if "FW" in player_position.upper():
        player_fig =  px.line(player_attack_df[player_attack_df['Joueur']==player], 
                                x='Annees', y='Decisives', title=player+" Attacking stats")
    elif "MF" in player_position.upper():
        player_fig =  px.line(player_defense_df[player_defense_df['Joueur']==player], 
                                x='Annees', y='Balles recuperees', title=player+" Balles recuperees")
    elif "DF" in player_position.upper():
        player_fig = px.line(player_defense_df[player_defense_df['Joueur']==player], 
                                x='Annees', y='Tirs arretes',title=player+ " Tirs arretes")
    elif "GK" in player_position.upper():
        player_fig = px.line(player_defense_df[player_defense_df['Joueur']==player], 
                                x='Annees', y='Tirs arretes',title=player+ " Tirs arretes") 
    else:
        player_fig = "Undefined Position: "+ player_position + ": for "+player
    return player_fig

def get_player_position(player_info):
    try:
        player_position = player_info['Position'].values[0]
    except Exception as e:
        player_position = "FW"
    return player_position

def get_player_bio(player_info):
    try:
        player_bio = player_info['Biographie'].values[0].split('.')
        player_bio = " ".join(player_bio[:3])
    except Exception as e:
        player_bio = "Bio unavailable"
    return player_bio
def get_player_img(player_img):

    if isinstance(player_img,float):
        player_img = "https://dash.gallery/dash-fifa-dashboard/assets/player_1.png"
    else:
        try: 
            player_img = "https:"+player_img.values[0]
        except Exception as e:
           player_img = "https://dash.gallery/dash-fifa-dashboard/assets/player_1.png" 
    return player_img

def generate_players_data_table1(player_info):
    table = dash_table.DataTable(data=player_info[player_info.columns[:5]].to_dict('records'),
                                columns=[{'name': i, 'id': i} for i in player_info.columns[:5]],
                                #fill_width=False,
                                style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'},
                                style_data_conditional=[{
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'}],
                                style_cell={'textAlign': 'left',
                                            "height":"auto",
                                            'whiteSpace': 'normal',
                                            "width":"40px"})
    return table

def generate_players_data_table2(player_info):
    table = dash_table.DataTable(data=player_info[player_info.columns[5:8]].to_dict('records'),
                                columns=[{'name': i, 'id': i} for i in player_info.columns[5:8]],
                                style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'},
                                style_data_conditional=[{
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'}],
                                style_cell={'textAlign': 'left',
                                            "height":"auto",
                                            'whiteSpace': 'normal' ,
                                            "width":"40px"})
    return table



                        # html.P(["Player: ", player1_info['Joueur'].values[0]]),
                        # html.P(["Nationality: ", player1_info['Lieu de naissance'].values[0].split(",")[-1]]),
                        # html.P(["Nationality: ", player1_info['Lieu de naissance'].values[0].split(",")[-1]]),
                        # html.P(['Club: ', player1_info['Club'].values[0]]),
                        # html.P(['Age: ', player1_info['Age'].values[0]]),
                        # html.P(["Position: ", player1_info['Position'].values[0]]),
                        # html.P(["Prefered Leg: ", player1_info["Pied fort"].values[0]]),
                        # html.P(['Height: ', player1_info["Taille"].values[0]]),
                        # html.P(['Weight: ', player1_info["Poid"].values[0]]),
