import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import genes
import clusters
import functions
import home
import gene_list

#####


# loads different apps on different urls

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/genes':
        return genes.layout
    elif pathname == '/clusters':
        return clusters.layout
    elif pathname == '/functions':
        return functions.layout
    elif pathname == '/gene_list':
        return gene_list.layout
    else:
        return 'The page does not exist: 404 Error'


if __name__ == '__main__':
    app.run_server(debug=False)