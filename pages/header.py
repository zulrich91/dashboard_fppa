import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

LOGO = "https://www.formasup-npc.org/wp-content/uploads/2018/05/ILIS_UnivLille2018.jpg"

navbar = dbc.Navbar(
    [
        html.A(
            # Alignement vertical de l'image et de l'acceuil
            dbc.Row(
                [   #logo
                    # dbc.Col(html.Img(src=LOGO, height="40px")),
                    # #Navlink Acceuil
                    # dbc.NavLink("Worldwide", href="/covidworld",style={'color':'white'}),
                    # #Navlink Worldwide
                    # dbc.NavLink("France", href="/covidfrance",style={'color':'white'}),
                    # #Navlink France
                    # dbc.NavLink("SEAIRD modelisation", href="/modelisation",style={'color':'white'}),
                    dbc.NavLink("Acceuil", href="/home",style={'color':'white'}),
                    dbc.NavLink("Joueur", href="/joueur",style={'color':'white'}),
                    dbc.NavLink("Club", href="/club",style={'color':'white'}),
                    dbc.NavLink("Equipe Nationale", href="/nation",style={'color':'white'}),
                ],
                align="center",
                no_gutters=True,
            ),
        ),
        # dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="#4bbdaa",
    # dark=True,
    # style=dict(width='100%'),

    # style={'width':'200%'}
)
