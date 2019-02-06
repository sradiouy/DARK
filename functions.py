from app import app
import pandas as pd 
import header
from collections import defaultdict
from clusters import dfgeneral, dfhhblits, generate_pubmed_dash_table, generate_pubmed_sub_dataframe, dfpubmed, dfspecies,dfgo,generate_go_dash_table,generate_go_sub_dataframe
from genes import make_dash_pretty_table, dfextra, dfkey

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


def RiteshKumar(l):#FIND DUPLICATED ITEMS IN LIST
    return list(set([x for x in l if l.count(x) > 1]))




def get_cluster_by_words(selected_dropdown_value,dfwords,union_intersection):
    clusters = []
    if selected_dropdown_value == []:
        return []
    elif union_intersection == "UNION" or len(selected_dropdown_value) == 1:
        for word in selected_dropdown_value:
            clusters += dfwords[dfwords["Word"] == word].Cluster.values[0].split(",")
        return list(set(clusters))
    elif union_intersection == "INTERSECTION":
        for word in selected_dropdown_value:
            clusters += dfwords[dfwords["Word"] == word].Cluster.values[0].split(",")
        return list(set(RiteshKumar(clusters)))
    


def generate_search_dash_table(nclust,dataframe):
    line = "#### " + str(nclust) + " clusters were found that possess that combination of words in their annotation"
    return html.Div([html.Div(
    [dcc.Markdown(line),
    dash_table.DataTable(
    id='search-sorting-filtering',
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
    ],className="twelve columns gene_table",style={"margin-top": "-44px"}),
    html.Div(children=[html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Cluster''')],style={"margin-bottom": "30px","margin-left": "30%"}),
    html.Div(
        children=[
            dcc.Dropdown(
                id='query-search-cluster-dropdown',
                options=[
                    {'label': i, 'value': i} for i in set(df_search["CLUSTER"])
                ],
                multi=False,
                searchable=True
            )
        ],style={"margin-right":"100px","width": "400px"}
    )]
),html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Information''')],style={"margin-bottom": "30px","margin-left": "30%"}),
    html.Div(
    children=[
    dcc.Dropdown(
        id='options-search-dropdown',
        options=[{'label': k, 'value': k} for k in ["ORGANISM","ANNOTATION","PUBLICATIONS","PRODUCT","COMMENTS",'EC NUMBER','TIGRRFAM','SUPERFAMILY','SMART','PROSITE','PIRSF','PFAM','INTERPRO','TM COUNT','SIGNAL P']],
        value=dfextra.columns[1]
    ),
    ],style={"width": "236px"},
    )
    ]
)],className=" four columns",style={"display":"flex","margin-bottom": "50px","margin-top": "50px","margin-left":"2%"}),
    html.Div(id="cluster-serach-table")
    ]
)



#MAIN

word_file = "data/words.txt"

words = [word.strip() for word in open(word_file,"r").readlines()]


words_by_cluster  = "data/term_cluster.tsv"

dfwords = pd.read_csv(words_by_cluster,sep="\t",header=0)


cluster_list = get_cluster_by_words(["calmodulin"],dfwords,"UNION")

df_search = dfgeneral[dfgeneral['CLUSTER'].isin(cluster_list)]

#LAYOUT 



words_dropdown = html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Keyword''')],style={"margin-bottom": "0px","margin-left": "47%"}),
    html.Div(id='term-dropdown-container',
        children=[
            dcc.Dropdown(
                id='term-dropdown',
                options = [{'label': w.upper(), 'value': w} for w in words],
                multi=True,
                searchable=True,
                value="" #Start query value
            ),
            dcc.Dropdown(
                id='union-intersection-dropdown',
                options=[
                    {'label': 'Union', 'value': 'UNION'},
                    {'label': 'Intersection', 'value': 'INTERSECTION'}
                ],
                value='UNION',
                searchable=False,
                clearable=False
            )
        ]
    )
    ]
)


layout = html.Div([
    header.layout_functions,
    words_dropdown,
    html.Div(id='search-table')
    ])



@app.callback(Output('search-table', 'children'), [Input('term-dropdown', 'value'), 
Input('union-intersection-dropdown', 'value')])
def load_graph(selected_dropdown_value, union_intersection):
    if len(selected_dropdown_value) > 0: #Cuando no tengo seleccion no hago nada. Para evitar que se generen vacios.
        cluster_list = get_cluster_by_words(selected_dropdown_value,dfwords,union_intersection)
        if cluster_list != []:
            if cluster_list is not None:
                global df_search
                df_search = dfgeneral[dfgeneral['CLUSTER'].isin(cluster_list)]
                return generate_search_dash_table(len(cluster_list),df_search)
            else:
                return html.Div(dcc.Markdown("#### 0 clusters were found that possess that combination of words in their annotation"))
        else:
            return html.Div(dcc.Markdown("#### 0 clusters were found that possess that combination of words in their annotation"))


@app.callback(
    Output('search-sorting-filtering', 'data'),
    [Input('search-sorting-filtering', 'pagination_settings'),
     Input('search-sorting-filtering', 'sorting_settings'),
     Input('search-sorting-filtering', 'filtering_settings')])
def update_graph(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = df_search
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            if col_name == "CLUSTER":
                dff = dff.loc[dff[col_name] == int(filter_value)]
            else:
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
    dash.dependencies.Output('cluster-serach-table', 'children'),
    [dash.dependencies.Input('query-search-cluster-dropdown', 'value'),
    dash.dependencies.Input('options-search-dropdown', 'value')])
def set_display_children(selected_value,selected_option):
    labels = []
    values = []
    if selected_value is not None and selected_option is not None and selected_option != "":
        if selected_option == "PRODUCT":
            labels = dfkey[dfkey["CLUSTER"]==selected_value].ID.tolist()
            values = dfkey[dfkey["CLUSTER"]==selected_value].fillna("-").PRODUCT.tolist()
        elif selected_option == "ORGANISM":
            labels = dfspecies[dfspecies["Cluster"]==selected_value].columns.tolist()
            values = dfspecies[dfspecies["Cluster"]==selected_value].fillna("-").values.tolist()[0]
        elif selected_option == "ANNOTATION":
            try:
                labels = dfhhblits[dfhhblits["Cluster"]==selected_value].columns.tolist()
                values = dfhhblits[dfhhblits["Cluster"]==selected_value].fillna("-").values.tolist()[0]
            except:
                labels = ['Cluster', 'HMM Length', 'PDB70 (1)', 'PDB70 (2)', 'PDB70 (3)', 'PFAM_A (1)', 'PFAM_A (2)', 'PFAM_A (3)', 'SCOP70 (1)', 'SCOP70 (2)', 'SCOP70 (3)', 'UNICLUST30 (1)', 'UNICLUST30 (2)', 'UNICLUST30 (3)']
                values =[str(selected_value)] + ["Not computed"]*13       
        elif selected_option == "COMMENTS":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").COMMENTS.tolist()
        elif selected_option == "PFAM":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").PFAM.tolist()
        elif selected_option == "INTERPRO":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").INTERPRO.tolist()
        elif selected_option == "EC NUMBER":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").EC_NUMBER.tolist()
        elif selected_option == "TIGRRFAM":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").TIGRRFAM.tolist()
        elif selected_option == "SUPERFAMILY":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").SUPERFAMILY.tolist()
        elif selected_option == "SMART":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").SMART.tolist()
        elif selected_option == "PROSITE":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").PROSITE.tolist()
        elif selected_option == "PIRSF":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").PIRSF.tolist()
        elif selected_option == "TM COUNT":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").TM_COUNT.tolist()
        elif selected_option == "SIGNAL P":
            labels = dfextra[dfextra["CLUSTER"]==selected_value].ID.tolist()
            values = dfextra[dfextra["CLUSTER"]==selected_value].fillna("-").SIGNAL_P.tolist()
        elif selected_option == "PUBLICATIONS":
            df_individual_pubmed = generate_pubmed_sub_dataframe(selected_value)
            return generate_pubmed_dash_table(df_individual_pubmed)
        elif selected_option == "GO":
            df_individual_go = generate_go_sub_dataframe(selected_value)
            return generate_go_dash_table(df_individual_go)
        dfcluster_species = pd.DataFrame({"label":labels,"value":values})
        return html.Div([
                    html.H6([""],
                            className="h6_gene_individual_table gs-header gs-table-header padded"
                            ),
                    html.Table(make_dash_pretty_table(dfcluster_species),className="gene_individual_table")
                ], className="twelve columns about_text")
    else:
        return html.Div()