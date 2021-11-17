#--------------- Package 



import pandas as pd
import numpy as np
from scipy.integrate import odeint
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
from app import app
import dash_table as dt

#-----------------------------------------------------------------------------------------------
#--------------------------  tabs styles --------------------------------------
tabs_styles = {
    'height': '30px', 'width':'1050px', "margin": "0 auto",'color': 'blue', #'border': '1px solid #d6d6d6' ,
}
tab_style = {
   # 'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius':'15px',
    'background-color':'#F2F2F2',
    'box-shadow':'4px 4px 4px lightgrey'
    
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#172763', ##119DFF
    'color': 'white',
    'padding': '6px',
    'border-radius':'15px'
}

#--------------------------------

styl_test_description_club = {'margin-left':'20px','color':'hsl(197, 87%, 64%)'}


#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

#------------ Data upload
adversaire  = pd.read_csv("data/tab_Adversaire.csv")
entraineur = pd.read_csv("data/tab_Entraineur.csv")
clubs = pd.read_csv("data/tab_Clubs.csv")
pays = pd.read_csv("data/tab_Pays.csv")
clubLogo = pd.read_csv("data/tab_ClubLogoImage.csv")
clubDetails = pd.read_csv("data/tab_all_details_club.csv")
elo = pd.read_csv("data/tab_Elo_club.csv")
statdata = pd.read_csv("data/tab_Stats_club_2010-2022.csv")
#------------ Traitement de donnée ---------------------------------------
# club avec info intégrale 125 
list_intersectClubs = list( set(list(clubDetails["NomDesClubs"]))     &   set(list(elo["NomDesClubs"])) )

# club avec info partiel les elo ok 
#list_intersectClubs = list( set(list(clubs["NomDesClubs"]))    &    set(list(elo["NomDesClubs"])) )

# data frame des intersect club
df_intersectClubs = clubDetails[clubDetails["NomDesClubs"].isin(list_intersectClubs)]
# Dropdown options
all_options = [{'label':c,'value':c} for c in (df_intersectClubs['NomDesClubs'].unique())]

###############-------------------------------------- oglet 2 ---------------------------------

all_options_onglet2 = [{'label':c,'value':c} for c in (clubLogo['NomDesClubs'].unique())]


# club_pays = "France"
# division = " ligue 2"
# nombre_competition= 16
# nombre_premierPlace = 1
# entraineur= "Roger Mila"



club = html.Div([
	html.Img(src=app.get_asset_url("banderole.png"),
	style={'height':'50%', 'width':'100%', 'margin-bottom':'0px'}),

	
	dcc.Tabs([
###################################################################################################################
######################################### TAB 1 ##############################################################
    dcc.Tab(label="Découverte des clubs", children=[ 

	html.Div([ 
		#------------------------- 1ere ligne ------------------------------------------

	
		html.Div([
			html.Div([
				dcc.Dropdown(id='input_club',
							multi= False,
							searchable=True,
							value='AFC Wimbledon',
							style={'color':'white' ,'width':'100%','font-size':'12px', 'backgroundColor': '#4bbdaa'},
							clearable=True,
							placeholder='choisir un club',
							options= all_options,
							#optionHeight = 50,
							className='dcc_compon',
							

						),
			],style={'margin-top':'20px','margin-bottom':'10px','fontSize':12}),

			html.Div([

				#html.H2("Information du club "),
				html.Br(),

				html.Div([

				html.Br(),
				html.P(' PAYS : ',style=styl_test_description_club),
        	    html.B(id= "output_club_pays" ,style=styl_test_description_club), 
                ],className='row flex-display',style={'margin-top':'20px','margin-bottom':'10px','fontSize':20}),
			

				html.Div([ 
					html.P(' Division : ',style = styl_test_description_club),
					html.B(id= "output_division_du_club" ,style = styl_test_description_club), 
               ],className= 'row flex-display',style={'margin-bottom':'10px','fontSize':20,}),

				html.Div([ 
					html.P(' Equipe  ',style = styl_test_description_club),
					html.B(id= "output_sex_du_club" ,style = styl_test_description_club), 
               ],className= 'row flex-display',style={'margin-bottom':'10px','fontSize':20,}),


				html.Div([ 
                html.P(' Nombre de cmpétition : ',style=styl_test_description_club),
                html.B(id="output_nombre_de_competition" ,style=styl_test_description_club), 
           	 ],className='row flex-display',style={'margin-bottom':'10px','fontSize':20}),

				html.Div([ 
					html.P(' Nombre de première place : ',style=styl_test_description_club),
					html.B(id= "output_nombre_de_1place" ,style=styl_test_description_club), 
				],className='row flex-display',style={'margin-bottom':'10px','fontSize':20}),


				html.Div([ 
					html.P(' Entraineur : ',style = styl_test_description_club),
					html.B(id= "output_coch_du_club" ,style = styl_test_description_club), 
               ],className= 'row flex-display',style={'margin-bottom':'10px','fontSize':20,}),


		
            html.Br(),
            html.Br(),
        

			html.P('Rapport nombre de victoir sur nombre de match pour la saison en cours',
					className='fix_label',
					style= {'color':'white', 'fontSize':15}),
			html.Br(),
            html.Br(),
        


						],#className='row flex-display',
						 style= {'width':'100%',
																'backgroundColor': '#1c3079',
																'border-radius':'15px',
																'border-color':'#1c3079',
																'borderTop': '#1c3079',
    															'borderBottom': '#1c3079'})
		
		] ,style={ 'width':'20%','backgroundColor':'#4bbdaa'}),



		html.Div([ 

			html.Br(),
			
			html.Div([ 
				
					html.H3(id="output_Nom_du_club",style= {'margin-left':'20px','margin-top':'30px','color':'hsl(197, 87%, 64%)'}),

					
					html.Div([ 
						html.H3(' ELO : ',style = {'margin-left':'20px','color':'hsl(197, 87%, 64%)'}),
						html.H3(id="output_Elo_du_club", style= {'margin-left':'20px','color':'hsl(197, 87%, 64%)'}),
               		],className= 'row flex-display',style={'margin-left':'130px','margin-bottom':'10px','margin-top':'10px','fontSize':20,}),
					


				#	html.Div([ 
					html.Img(id= "output_Logo_du_club", style={'height':'40%', 'width':'40%', 'margin-right':'20px','border-radius':'15px',}),
															],style= { 	'width':'35%',
																		'backgroundColor': '#1c3079',
																		'border-radius':'15px',
																		'border-color':'#1c3079',
																		'borderTop': '#1c3079',
																		'borderBottom': '#1c3079',
																		'margin-left':'20px',
																		'color':'hsl(197, 87%, 64%)'}),

			
			html.Div([
				
				
				html.H4(id = "output_graphe1_title",style= {'margin-left':'20px','color':'hsl(197, 87%, 64%)'}),
				dcc.Checklist(id= "chekListGrapheEvolution",
					options=[ 	{'label': 'Victoire', 'value': 'Victoire'},
								{'label': 'Defaite', 'value': 'Defaite'},
								{'label': 'Nul', 'value': 'Nul'},
								{'label': 'But marque', 'value': 'But_marque'},
								{'label': 'But encaisse', 'value': 'But_encaisse'}
																			],
							value= [ 'Victoire'],
							labelStyle={'display': 'inline-block', 'color':"white", 'width':'12%'}
   				 ),
				#html.Div([
	            	dcc.Graph( id='lineChart_evolution_du_club', config={'displayModeBar':'hover'})
															 ],style= { 'width':'62%',
																		'backgroundColor': '#1c3079',
																		'border-radius':'15px',
																		'border-color':'#1c3079',
																		'borderTop': '#1c3079',
																		'borderBottom': '#1c3079',
																		'margin-left':'20px'})


		],className='row flex-display',style={	'width':'80%',
												#'backgroundColor': 'red',
												'margin-top':'20px'})
		
		
		],className='row flex-display'	)



	],style=tab_style, selected_style=tab_selected_style),
#######################################################################################################################
######################################### TAB 2 LAYOUT ################################################################
#######################################################################################################################
	dcc.Tab(label=" clubs Vs adversaires", children=[ 
html.Div([ # bloc 1 et bloc2 ( colonne 2)
	html.Div([# tout le bloc 1
		html.Div([# deux dropdow + deux image 
			html.Div([ # dropdown et image 
					dcc.Dropdown(id='input_club_ogle2',
								multi= False,
								searchable=True,
								value='Aston Villa LFC',
								style={'color':'white' ,'width':'100%','font-size':'12px', 'backgroundColor': '#4bbdaa','margin-bottom':'20px'},
								clearable=True,
								placeholder='choisir un club',
								options= all_options_onglet2,
								#optionHeight = 50,
								className='dcc_compon',	),


					html.Img(id= "output_Logo_club_ongle2", style={'height':'auto', 'width':'auto', 'margin-right':'20px','border-radius':'15px',}),

				],style={'margin-top':'20px','margin-bottom':'15px','fontSize':12, 'width':'20%','backgroundColor':'#4bbdaa'}),

			#------------------------- Adversaire  dropdown -----------------------------------------------------------------

			html.Div([
					dcc.Dropdown(id='input_Adversaire_club',
								multi= False,
								searchable=True,
								#value='Aston Villa LFC',
								style={'color':'white' ,'width':'100%','font-size':'12px', 'backgroundColor': '#4bbdaa','margin-bottom':'20px'},
								clearable=True,
								placeholder='choisir un club',
							#	options= all_options,
								#optionHeight = 50,
								className='dcc_compon',	),


					html.Img(id= "output_Logo_club_advers", style={'height':'auto', 'width':'auto', 'margin-right':'20px','border-radius':'15px',})
					
			],style={'margin-left':'500px','margin-top':'20px','margin-bottom':'15px','fontSize':12, 'width':'20%','backgroundColor':'#4bbdaa'}),


		],className='row flex-display'),



	html.Div([     
		
		html.Div([ 
			html.H4(" Victoire - Match nul - Défaite "),
			dcc.Graph( id='pie_chartAdverse1', config={'displayModeBar':'hover'}) ,html.Br()],style= {
																							'margin-right':'6px',
																							'width':'47%',
																							'backgroundColor': '#1c3079',
																							'border-radius':'15px',
																							'border-color':'#1c3079',
																							'borderTop': '#1c3079',
																							'borderBottom': '#1c3079',
																							'margin-left':'20px'}),
		html.Div([
			html.H4(" But marqué - but encaissé "),
			dcc.Graph( id='pie_chartAdverse2', config={'displayModeBar':'hover'}), html.Br()],style= {
																							'margin-right':'6px',
																							'width':'47%',
																							'backgroundColor': '#1c3079',
																							'border-radius':'15px',
																							'border-color':'#1c3079',
																							'borderTop': '#1c3079',
																							'borderBottom': '#1c3079',
																							'margin-left':'20px'})



				], className= "row flex-display" , style = { 'margin-left':'2%', 'width':'100%' ,'margin-top':'0px'})

				],style={'width':'80%',}),# fin bloc 1 # 'backgroundColor': 'green' , 


				html.Div([
					html.H5("le ELO de tous les clubs ",style={ "margin-bottom":"10px"}),
					dcc.RangeSlider( id='range_slider',min=0, max=30, value=[10, 15], allowCross=False),
					html.Div([
					dt.DataTable(id= 'output_elo_table') ],  )# '#1c3079' # fin colonne 2
				],style={'backgroundColor': '#1c3079' , 'width':'20%', 'border-radius':'15px',} )

			],className= "row flex-display" ,style={'width':'100%',})# Fin bloc 1 et colonne 2
		
		],style=tab_style, selected_style=tab_selected_style) ## Fin  Tab 2

	], style=tabs_styles), html.Div(id='tabs-content-inline',),######## Fin des Tabs 

],id='mainContener' ,style={'backgroundColor': '#4bbdaa'} )##fcfdfd Tous les layout (tout le cadre)

#######################################################################################################
########################## Callback onglet 1 ##########################################################
#######################################################################################################


#............Callback Pays  du club  .............
@app.callback(Output('output_club_pays','children'),
			  [Input('input_club','value')])
def update_nomClub(input_club):
	df_selectedClub = clubDetails[clubDetails['NomDesClubs']==input_club]
	return  df_selectedClub["Pays"].iloc[0]


#............Callback Nom du club  .............
@app.callback(Output('output_Nom_du_club','children'),
			  [Input('input_club','value')])
def update_nomClub(input_club):
	return  'Club de football de {}'.format(input_club)

#............Callback Division .......................
@app.callback(Output('output_division_du_club','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	df_selectedClub = clubs[clubs['NomDesClubs']==input_club]
	return  df_selectedClub["divisionDuClub"].iloc[0]


#............Callback sexe du club  .......................
@app.callback(Output('output_sex_du_club','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	df_selectedClub = clubDetails[clubDetails['NomDesClubs']==input_club]
	sexe = df_selectedClub["Sex"].iloc[0]
	if(sexe=="H"):
		sexe=" masculine "
	else: sexe=" féminine "
	return  sexe


#............Callback Nombre de compétion .......................
@app.callback(Output('output_nombre_de_competition','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	df_selectedClub = clubs[clubs['NomDesClubs']==input_club]
	return  df_selectedClub["NombreDeCompetitionJoue"].iloc[0]

#............Callback Nombre de première place .......................
@app.callback(Output('output_nombre_de_1place','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	df_selectedClub = clubs[clubs['NomDesClubs']==input_club]
	return  df_selectedClub["nombreDePremierePlace"].iloc[0]

#............Callback Entraineur du club .......................
@app.callback(Output('output_coch_du_club','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	df_selectedClub = clubDetails[clubDetails['NomDesClubs']==input_club]
	return  df_selectedClub["Coach"].iloc[0]



#-------------------------------------------------------------------------------------
#------------Callback  colonne  2------------------------------->>>>>>>>#########-----

@app.callback(Output('output_Elo_du_club','children'),
			  [Input('input_club','value')])
def update_nomClub(input_club):
	df_selectedClub = elo[elo['NomDesClubs']==input_club]
	return  round(df_selectedClub["Elo"].iloc[0],0)

#............Callback logo du club   .............
@app.callback(Output('output_Logo_du_club','srcSet'),
			  [Input('input_club','value')])
def update_logoClub(input_club):
	df_selectedClub = clubLogo[clubLogo['NomDesClubs']==input_club]
	linklogoImage = df_selectedClub["logoLinks"].iloc[0].replace('"',"")
	src = linklogoImage 
	return  src

#-------------------------------------------------------------------------------------
#------------Callback  colonne  2------------------------------->>>>>>>>#########-----

@app.callback(Output('output_graphe1_title','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	return  "Evolution de la performance de {} dans le temps ".format(input_club)




#............Callback graph d'évolution du club en fonction du temps   .............

@app.callback(Output('lineChart_evolution_du_club','figure'),
			  [Input('input_club','value')],
			  [Input('chekListGrapheEvolution','value')])
def update_graph(input_club, chekListGrapheEvolution):

	selected_statdata = statdata[statdata["NomDesClubs"]==input_club]
	x_annee = list(selected_statdata["Annee"])
	list_choix= chekListGrapheEvolution
	size_listchoix = len(list_choix)
	if (size_listchoix==1):
		y_choix = list(selected_statdata[list_choix[0]])

	# 
	# y_Victoire = list(selected_statdata["Victoire"])
	# y_Defaite = list(selected_statdata["Defaite"])
	# y_Nul = list(selected_statdata["Nul"])
	# y_But_marque = list(selected_statdata["But marque"])
	# y_But_encaisse = list(selected_statdata["But marque"])

	return{
		'data': [go.Scatter(
			x=x_annee,
			y=y_choix,
			name='cas confirmés au quotidien',
			line= dict(width=3,color='#19AAE1'),
			marker=dict(color='white',size=10,symbol='circle'),
			hoverinfo='text',
			# hovertext='<b>Date</b>:' + covid_data3['date'].tail(30).astype(str) + '<br>' +
			# '<b>cas confirmés quotidien</b>:' + [f'{x:,.0f}' for x in covid_data3['daily confirmed'].tail(30)] + '<br>' +
			#  '<b>pays</b>:' + covid_data3['Country/Region'].tail(30).astype(str) + '<br>'
			 )],
		'layout': go.Layout(

				title={'text': 'Evolution du  club {} en fonction du temps'.format(input_club),
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				titlefont={'color':'white', 'size':20},
				font=dict(family='sans-serif', 
							color = 'white',
							 size= 12),
				hovermode='closest',
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',
				legend={'orientation':'h',
				'bgcolor':'#1f2c56','xanchor':'center','x':0.5,'y':-0.7},
				xaxis=dict(title= '<b>Date</b>',
					color='white',
					showline= True,
					showgrid= True),
				yaxis=dict(title= '<b>Cas confirmé au quotidien </b>',
					color='white',
					showline= True,
					showgrid= True)

			)

	}





#------------Callback gauge ------------------------------------->>>>>>>>#########-----

# @app.callback(
#     dash.dependencies.Output('input_Adversaire_club', 'options'),
#     [dash.dependencies.Input('input_club', 'value')]
# )
# def update_date_dropdown(input_club):
#     df_adverSelected = adversaire[adversaire['NomDesClubs']==input_club]
    
#     return df_adverSelected
              
# @app.callback(
#     dash.dependencies.Output('display-selected-values', 'children'),
#     [dash.dependencies.Input('input_Adversaire_club', 'options')])

# def set_display_children(selected_value):
#     df_selectedClub = adversaire[adversaire['NomDesClubs']==selected_value]
#     return [{'label':c,'value':c} for c in (df_selectedClub['Nom_Adversaire'].unique())]
    # 'you have selected {} option'.format(selected_value)

#######################################################################################################
########################## Callback onglet 2 ##########################################################
#######################################################################################################

#-------------------------- callback dropdown adverssaire 
@app.callback(
    dash.dependencies.Output('input_Adversaire_club', 'options'),
    [dash.dependencies.Input('input_club_ogle2', 'value')])
def update_drowAdvers(inputCub):
	seleted_club = adversaire[adversaire["NomDesClubs"]==inputCub]
	Advers_option = [{'label':c,'value':c} for c in (seleted_club['Nom_Adversaire'].unique())]

	return Advers_option

#----------------------- callback logo du club onglet 2
 
@app.callback(Output('output_Logo_club_ongle2','srcSet'),
			  [Input('input_club_ogle2','value')])
def update_logoClub(input_club_ogle2):
	df_selectedClub = clubLogo[clubLogo['NomDesClubs']==input_club_ogle2]
	linklogoImage = df_selectedClub["logoLinks"].iloc[0].replace('"',"")
	src = linklogoImage 
	return  src

#------------------------ callback logo adverser club onglet 2
@app.callback(Output('output_Logo_club_advers','srcSet'),
			  [Input('input_Adversaire_club','value')])
def update_logoClub(input_Adversaire_club):
	df_selectedClub = clubLogo[clubLogo['NomDesClubs']==input_Adversaire_club]
	linklogoImage = df_selectedClub["logoLinks"].iloc[0].replace('"',"")
	src = linklogoImage 
	return  src

#------------------------- callback pie chart  (victoire - Match nul -Défaite ) -------------------------

@app.callback(Output('pie_chartAdverse1','figure'),
			  [Input('input_club_ogle2','value'),
              Input('input_Adversaire_club','value')
              ])
def update_graph(input_club_ogle2, input_Adversaire_club):
    df_ClubAdversSelected = adversaire[(adversaire['NomDesClubs']==input_club_ogle2) & (adversaire['Nom_Adversaire']==input_Adversaire_club)]
    selectVar = df_ClubAdversSelected[["Victoire","Match_nul","Défaite"]]

    labels = list(selectVar.columns[0:])
    values = list(selectVar.values[0])
    colors = [' hsl(199, 97%, 47%)','hsl(249, 95%, 31%) ','hsl(305, 54%, 27%)']#['orange', '#dd1e35','green', 'darkorchid']
			#['hsl(249, 95%, 31%) ','hsl(305, 54%, 27%)',  ' hsl(199, 97%, 47%)']
    return{
		'data': [go.Pie(
			labels= labels,
			values=  values,
			marker=dict(colors=colors),
			hoverinfo='label+value+percent',
			textinfo='label+value',
			#hole=.7, # Pour changer la forme du cercle
			rotation=45,
			#insidetextorientation='radial'
			)],
		'layout':go.Layout(

				title={'text':  'Résultat des rencontres de <b>{}</b> contre  <b>{}</b>'.format(input_club_ogle2,input_Adversaire_club),
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				titlefont={'color':'white', 'size':15},
				font=dict(family='sans-serif', 
							color = 'white',
							 size= 12),
				hovermode='closest',
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',
				legend={'orientation':'h',
				'bgcolor':'#1f2c56','xanchor':'center','x':0.5,'y':-0.7
						}

			)

	}
#------------------------- callback pie chart2  (but marqué  - but encaissé ) -------------------------
@app.callback(Output('pie_chartAdverse2','figure'),
			  [Input('input_club_ogle2','value'),
              Input('input_Adversaire_club','value')
              ])
def update_graph(input_club_ogle2, input_Adversaire_club):
    df_ClubAdversSelected = adversaire[(adversaire['NomDesClubs']==input_club_ogle2) & (adversaire['Nom_Adversaire']==input_Adversaire_club)]
    selectVar = df_ClubAdversSelected[["But_marque","But_encaisse"]]

    labels = list(selectVar.columns[0:])
    values = list(selectVar.values[0])
    colors = [ ' hsl(199, 97%, 47%)','hsl(305, 54%, 27%)' ]#'hsl(249, 95%, 31%)'

    return{
		'data': [go.Pie(
			labels= labels,
			values=  values,
			marker=dict(colors=colors),
			hoverinfo='label+value+percent',
			textinfo='label+value',
			#hole=.7, # Pour changer la forme du cercle
			rotation=45,
			#insidetextorientation='radial'
			)],
		'layout':go.Layout(

				title={'text': '',# 'Résultat des rencontres de <b>{}</b> contre  <b>{}</b>'#.format(input_club_ogle2,input_Adversaire_club),
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				titlefont={'color':'white', 'size':15},
				font=dict(family='sans-serif', 
							color = 'white',
							 size= 12),
				hovermode='closest',
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',
				legend={'orientation':'h',
				'bgcolor':'#1f2c56','xanchor':'center','x':0.5,'y':-0.7
						}

			)

	}

#------------------------------------------  callback elo table
 
@app.callback(Output('output_elo_table','data'),
			  [Input('range_slider','value')])
def update_elo_tab(range_slider):
	
	min= range_slider[0]
	max= range_slider[1]
	tab = elo.iloc[min:max,1:]
	return  tab





layout_club  = html.Div([html.Br(),club], style={"text-align":"center", 'width': '100%', 'background-color': '#DCDCDC', "background-size": "cover", "background-position": "center"})
