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


#--------------------------  Data 

#------------ Data upload
adversaire  = pd.read_csv("data/tab_Adversaire.csv")
entraineur = pd.read_csv("data/tab_Entraineur.csv")
clubs = pd.read_csv("data/tab_Clubs.csv")
pays = pd.read_csv("data/tab_Pays.csv")
clubLogo = pd.read_csv("data/tab_ClubLogoImage.csv")

#------------ Traitement de donnée ---------------------------------------

club_pays = "France"
division = " ligue 2"
nombre_competition= 16
nombre_premierPlace = 1
entraineur= "Roger Mila"





club = html.Div([
                       
  #html.Div([
   # html.H2("MY first App")
 # ])
 	#====================== Première ligne du dashboard ===============
 	#=========== DEDUT =======
	html.Div([ 
		# -----------Objet 1 image ---------
		html.Div([
   			html.Img(src=app.get_asset_url('soccer.jpg'),
				id='corona-image',
				style={'height':'100px',
                       'width':'50%',
                       'margin-bottom':'25px'})
   		],className='one-third column'),

		# -----------Objet 2 Titre du Dashboard ---------
		html.Div([
			html.H3(' FOOTBALL  DATA ', style={'margin-bottom':'0px','color':'white'}),
			html.H5('Visualisation des données des joeurs et des clubs',style={'margin-bottom':'0px','color':'white'})
		],className='one-half column',id='title',style={'color':'orange','margin-left':'0px'}),

		# -----------Objet 3 Place pour afficher la dernière mise à jour ---------
		html.Div([ 
				html.H6('Data source : ',
					style={'color':'orange','margin-right':'10px'}),
                    dcc.Link('for more info  ', href='https://fbref.com/fr/')
		],className='row flex-display',id='title1')
	#=========== FIN =======
	],id='header',className='row flex-display',style={'margin-bottom':'25px','margin-left':'0px','margin-top':'0px'}), 

	#====================== Deuxième ligne du dashboard ===============
	html.Div([

		# -----------Objet 1 les cas confirmé  ---------
		html.Div([



		],className='card_container three columns'),


		# -----------Objet 2 nombre cas déscès ---------
		html.Div([


		],className='card_container three columns'),


		# -----------Objet 3 le nombre de porteurs  (recovered) ---------
		html.Div([
	

		],className='card_container three columns'),


# -----------Objet 4 le nombre personnes malades  (active) ---------
		html.Div([


		],className='card_container three columns'),
		#=========== FIN =======
	]),

 	#====================== Troisième ligne du dashboard ===============
 	#dash html components : https://dash.plotly.com/dash-html-components
 	#=========== DEDUT =======
	html.Div([ 

#------------------ DEDUT Objet 1 ----------------------
		html.Div([

		
            
            dcc.Dropdown(id='input_club',
						multi= False,
						searchable=True,
						value='FK Kukësi',
						style={'color':'white' ,'width':'100%','font-size':'12px'},
						clearable=True,
						placeholder='choisir un club',
						options=[{'label':c,'value':c} for c in (clubs['NomDesClubs'].unique())],
						#optionHeight = 50,
						className='dcc_compon'
						),

			html.Br(),

             #-------------------ligne  Nom et logo du club -----------------------
            html.Div([ 

            html.Img(id= "output_Logo_du_club", style={'height':'70px', 'width':'auto', 'margin-right':'20px'}),
			html.B(id="output_Nom_du_club",className ='fix_label', style={'color':'#ffb41a', 'fontSize':17,'text-align':'center'}),
				
            ],className='row flex-display',style={'margin-bottom':'20px'} ),


            #--------------------ligne info club ---------------------------------
            # html.P(' PAYS : ',style={'margin-right':'20px','color':'#ffb41a','fontSize':10}),
            # html.B("club_pays" ,style={'margin-right':'20px','color':'#ffb41a','fontSize':10}), 
            #     ],className='row flex-display',style={'margin-bottom':'10px','fontSize':8}),
            
            html.Div([ 
            html.P(' DIVISION : ',style={'margin-right':'20px','color':'#ffb41a'}),
            html.B(id= "output_division_du_club" ,style={'margin-right':'20px','color':'#ffb41a'}), 
               ],className= 'row flex-display',style={'margin-bottom':'10px','fontSize':15}),

            html.Div([ 
                html.P(' NOMBRE DE COMPETITION : ',style={'margin-right':'10px','color':'#ffb41a'}),
                html.B(id="output_nombre_de_competition" ,style={'margin-right':'20px','color':'#ffb41a'}), 
            ],className='row flex-display',style={'margin-bottom':'10px','fontSize':15}),

            html.Div([ 
                html.P(' NOMBRE DE PREMIERE PLACE : ',style={'margin-right':'10px','color':'#ffb41a'}),
                html.B(id= "output_nombre_de_1place" ,style={'margin-right':'20px','color':'#ffb41a'}), 
            ],className='row flex-display',style={'margin-bottom':'10px','fontSize':15}),

            html.Div([ 
                html.P(' ENTRAINEUR DU CLUB : ',style={'margin-right':'20px','color':'#ffb41a'}),
                html.B(id = "output_entraineur" ,style={'margin-right':'20px','color':'#ffb41a'}), 
            ],className='row flex-display',style={'margin-bottom':'10px','fontSize':15}),

        html.P('Rapport nombre de victoir sur nombre de match pour la saison en cours',
				className='fix_label',
				style= {'color':'white', 'fontSize':15}),
        
        daq.Gauge( id='output_club_gauge',
            #label="performance du club (victoire/ nombre de match", 
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
           # size= 100,
            #units="MPH",
            value=6,
            max=20,
            min=0,	),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
    

		],className='create_container two columns',style={ 'height':'200%', 'width':'18%'}),





			
#------------------ DEDUT Objet 2 Pie chart ----------------------
#       
     html.Div([

#............................. line chart
        html.Div([

	        dcc.Graph( id='line_chart', config={'displayModeBar':'hover'})

		],className='create_container two columns',style={'height':'40%', 'width':'37%', 'margin-right':'0px'}),


		html.Div([

	        #dcc.Graph( id='pie_chart', config={'displayModeBar':'hover'})
             dcc.Dropdown(id='input_Adversaire_club',
						multi= False,
						searchable=True,
					#	value='FK Kukësi',
						style={'color':'white' ,'width':'100%','font-size':'12px'},
						clearable=True,
						placeholder='choisir un club',
					#	options=[ 'test1', 'test2'],
						#optionHeight = 50,
						className='dcc_compon'
						),

		],className='create_container two columns',style={'height':'40%', 'width':'25%', 'margin-right':'20px'}),

			
		
        html.Div([ 
        dcc.Graph( id='line_chartAnnee', config={'displayModeBar':'hover'})
        ],className='create_container seven columns',style={'height':'20%', 'width':'76%', 'margin-right':'0px','margin-left':'0px'})

    ]#,className='row flex-display',style={'margin-bottom':'10px','fontSize':15}  
      ),
   

	]#,className= 'row flex-display'
    ), #=========== FIN Troième ligne =======

  
	
],id='mainContener',style={'display':'flex','flex-direction':'column', 'background-color': '#441937'})




# """"""""" Début des callback """"""""""

#............Callback Nom du club  .............
@app.callback(Output('output_Nom_du_club','children'),
			  [Input('input_club','value')])
def update_nomClub(input_club):
	return  'Club de football de {}'.format(input_club)

#............Callback logo du club   .............
@app.callback(Output('output_Logo_du_club','srcSet'),
			  [Input('input_club','value')])
def update_logoClub(input_club):
	df_selectedClub = clubLogo[clubLogo['NomDesClubs']==input_club]
	linklogoImage = df_selectedClub["logoLinks"].iloc[0].replace('"',"")
	src = linklogoImage 
	return  src


#............Callback Division .......................
@app.callback(Output('output_division_du_club','children'),
			  [Input('input_club','value')])
def update_divisionClub(input_club):
	df_selectedClub = clubs[clubs['NomDesClubs']==input_club]
	return  df_selectedClub["divisionDuClub"].iloc[0]

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

#-------------Callback entraineur ------------------------------------
@app.callback(Output('output_entraineur','children'),
			  [Input('input_club','value')])
def update_entraineurClub(input_club):           
    df_selectedClub = entraineur[entraineur['NomDesClubs']==input_club]
    return df_selectedClub["Entraineurs"].iloc[0]

#------------Callback gauge ------------------------------------->>>>>>>>#########-----
@app.callback(Output('output_club_gauge','figure'),
			  [Input('input_club','value')])
def update_gaugeClub(input_club):
    df_selectedClub = clubs[clubs['NomDesClubs']==input_club]
    nombre_de_match = df_selectedClub["NombreDeCompetitionJoue"].iloc[0]
    nombre_de_victoire = df_selectedClub["nombreDePremierePlace"].iloc[0]

    if(nombre_de_match!=0):
        poucentage = (nombre_de_victoire/nombre_de_match)*100
    else:
        poucentage = 0
    
    return  poucentage


#------------Callback gauge ------------------------------------->>>>>>>>#########-----
#------------Callback gauge ------------------------------------->>>>>>>>#########-----

@app.callback(
    dash.dependencies.Output('input_Adversaire_club', 'options'),
    [dash.dependencies.Input('input_club', 'value')]
)
def update_date_dropdown(input_club):
    df_adverSelected = adversaire[adversaire['NomDesClubs']==input_club]
    
    return df_adverSelected
              
@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('input_Adversaire_club', 'options')])

def set_display_children(selected_value):
    df_selectedClub = adversaire[adversaire['NomDesClubs']==selected_value]
    return [{'label':c,'value':c} for c in (df_selectedClub['Nom_Adversaire'].unique())]
    # 'you have selected {} option'.format(selected_value)





layout_club  = html.Div([html.Br(),club], style={"text-align":"center", 'width': '100%', 'background-color': '#DCDCDC', "background-size": "cover", "background-position": "center"})
