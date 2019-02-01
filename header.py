# coding=utf-8
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd


logo = "https://raw.githubusercontent.com/sradiouy/DARK/master/Images/Capa%200.png"




# row1
header = html.Div([
    html.Img(className="logo",src=logo),
], className='navbar navbar-default navbar-static-top',style={"background-color": "#cccccc75"})


# row2
tabs_values = html.Div(
        children=[       
            dcc.Link('GENES    ', href='/', className="tab first"),
            html.Br(),
            dcc.Link('CLUSTERS    ', href='/clusters', className="tab"),
            html.Br(),
            dcc.Link('FUNCTIONS    ', href='/functions', className="tab")
        ],
    className="twelve columns tabs_div",style={"margin-right": "0px","margin-left": "13px","display":"inline-flex"}
    )


#row3



general_info = html.Div([
                html.Div([
                    html.Br([]),
                    html.H6('Summary of DARK',
                            className="gs-header gs-table-header padded",style={"margin-top":"0px","text-align": "center","font-size":"17px"}),
                    html.Br([]),
                    html.P("\
                            As the industry’s first index fund for individual investors, \
                            the 500 Index Fund is a low-cost way to gain diversified exposure \
                            to the U.S. equity market. The fund offers exposure to 500 of the \
                            largest U.S. companies, which span many different industries and \
                            account for about three-fourths of the U.S. stock market’s value. \
                            The key risk for the fund is the volatility that comes with its full \
                            exposure to the stock market. Because the 500 Index Fund is broadly \
                            diversified within the large-capitalization market, it may be \
                            considered a core equity holding in a portfolio."),
                ], className="twelve columns about_text"),
                html.Div([
                    html.H6([""],
                            className="gs-header gs-table-header padded",style={"height": "22px"}),
                ], className="twelve columns about_text"),
            ], className="row ")

# Define layout
layout = html.Div([
    header,
    tabs_values,
    general_info])

