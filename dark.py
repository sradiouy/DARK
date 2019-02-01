import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import genes
import clusters
import functions

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
        return genes.layout
    elif pathname == '/clusters':
        return clusters.layout
    elif pathname == '/functions':
        return functions.layout
    else:
        return 'The page does not exist: 404 Error'



# external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#                "https://codepen.io/bcd/pen/YaXojL.js"]

# for js in external_js:
#     app.scripts.append_script({"external_url": js})

if __name__ == '__main__':
    app.run_server(debug=False)