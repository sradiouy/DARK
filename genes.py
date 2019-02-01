import header
from app import app
import pandas as pd 

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


gene_file = "data/gene_info.tsv"

df = pd.read_table(gene_file,sep="\t",header=0)




key_info = ['primary_key', 'organism', 'protein_length', 'gene_product','cluster']
extra_info =  ['primary_key','cluster','gene_product','user_comment', 'ec_numbers_derived', 'tigrfam_description', 'superfamily_description','smart_description', 'prositeprofiles_description', 'pirsf_description','pfam_description', 'interpro_description','tm_count', 'signalp_scores']

dfkey = df[key_info]

dfextra = df[extra_info]

dfkey.columns = ['ID', 'ORGANISM', 'LENGTH', 'PRODUCT','CLUSTER']

dfextra.columns = ['ID','CLUSTER', 'PRODUCT','COMMENTS','EC_NUMBER','TIGRRFAM','SUPERFAMILY','SMART','PROSITE','PIRSF','PFAM','INTERPRO','TM_COUNT','SIGNAL_P']




def make_dash_pretty_table(dataframe):
    ''' Return a dash definition of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in dataframe.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def generate_dash_table(dataframe):
    return html.Div([dash_table.DataTable(
    id='table-sorting-filtering',
    columns=[{"name": i, "id": i} for i in dataframe.columns],
    pagination_settings={
        'current_page': 0,
        'page_size': 10,
    },
    pagination_mode='be',
    sorting='be',
    sorting_type='multi',
    sorting_settings=[],
    filtering='be',
    filtering_settings='',    
    style_table={'overflowX': 'scroll'},
    style_header={
        'backgroundColor': 'rgb(21, 45, 66)',
        'color':'white',
        'font-family': 'Dosis',
        'textAlign': 'center',
        'font-size': '18'
    },
    style_cell={
        'backgroundColor': '#FAFAFA',
        'minWidth': '0px', 'maxWidth': '300px',
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textAlign': 'center',
        'padding': '5px',
        'font-size': '15'
    }
    )
    ],className="twelve columns gene_table"
)



org_dropdown = html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Organsim''')],style={"margin-bottom": "30px","margin-left": "30%"}),
    html.Div(
        children=[
            dcc.Dropdown(
                id='query-org-dropdown',
                options=[
                    {'label': i.title(), 'value': i} for i in set(dfkey["ORGANISM"])
                ],
                multi=False,
                value=dfkey["ORGANISM"].iloc[0] #Start query value
            )
        ],style={"margin-right":"100px","width": "400px"}
    )]
)



gene_dropdown = html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Gene''')],style={"margin-bottom": "30px","margin-left": "30%"}),
    html.Div(
        id='gene-dropdown-container',
        children=[
            dcc.Dropdown(
                id='query-gene-dropdown',
                multi=False
            )
        ],style={"width": "236px"}
    )]
)





keyinfo_table = generate_dash_table(dfkey)
extrainfo_table = generate_dash_table(dfextra)

layout= html.Div(
    children=[
    header.layout,
    keyinfo_table,
    html.Div(children=[org_dropdown,gene_dropdown],className=" four columns",style={"display":"flex","margin-bottom": "50px","margin-left":"2%"}),
    html.Div(id='gene-table')
    ]
    )


@app.callback(
    Output('table-sorting-filtering', 'data'),
    [Input('table-sorting-filtering', 'pagination_settings'),
     Input('table-sorting-filtering', 'sorting_settings'),
     Input('table-sorting-filtering', 'filtering_settings')])
def update_graph(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = dfkey
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0]
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0]
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    if len(sorting_settings):
        dff = dff.sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1) *
        pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(
    dash.dependencies.Output('query-gene-dropdown', 'options'),
    [dash.dependencies.Input('query-org-dropdown', 'value')]
)
def update_date_dropdown(organism):
    return [{'label': i, 'value': i} for i in set(dfkey[dfkey["ORGANISM"]==organism]["ID"])]


@app.callback(
    dash.dependencies.Output('gene-table', 'children'),
    [dash.dependencies.Input('query-gene-dropdown', 'value')])
def set_display_children(selected_value):
    print(selected_value)
    if selected_value is not None:
        labels = dfextra[dfextra["ID"]==selected_value].columns.tolist()
        values = dfextra[dfextra["ID"]==selected_value].fillna("-").values.tolist()[0]
        dfgene = pd.DataFrame({"label":labels,"value":values})
        return html.Div([
                    html.H6([""],
                            className="h6_gene_individual_table gs-header gs-table-header padded"
                            ),
                    html.Table(make_dash_pretty_table(dfgene),className="gene_individual_table")
                ], className="twelve columns about_text")