import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages.header import navbar

from pages.joueur import layout_joueur
from pages.club import layout_club
from pages.nation import layout_nation
from pages.home import layout_home
from app import app,server


#layout rendu par l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content')
])

#callback pour mettre à jour les pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname=='/home' or pathname=='/':
        return layout_home
    elif pathname=='/joueur':
        return layout_joueur
    elif pathname=='/club':
        return layout_club
    elif pathname=='/nation':
       return layout_nation


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0',port=5002)