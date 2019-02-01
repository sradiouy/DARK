from app import app
import pandas as pd 
import header
from collections import defaultdict
from genes import generate_dash_table, dfkey, dfextra, make_dash_pretty_table


import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


def generate_pubmed_sub_dataframe(cluster):
    list_results = dfpubmed[dfpubmed["Cluster"] == cluster].values.tolist()
    if list_results == []:
        list_results = [[cluster] + ["Not Computed"]*4]
    df = pd.DataFrame(list_results,columns=["Cluster","Id","Title","Journal","Year"])
    return df


def generate_cluster_dash_table(dataframe):
    return html.Div([dash_table.DataTable(
    id='cluster-sorting-filtering',
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


def generate_pubmed_dash_table(dataframe):
    return html.Div([
    html.H6([""], className="h6_gene_individual_table gs-header gs-table-header padded"),
    dash_table.DataTable(
    id='pubmed-sorting-filtering',
    columns=[{"name": i, "id": i} for i in dataframe.columns],
    data=dataframe.to_dict("rows"),
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
        'overflow': 'scroll',
        'textAlign': 'center',
        'padding': '5px',
        'font-size': '15'
    }
    )
    ],className="twelve columns gene_table"
)


file_cluster = "data/cluster_info.tsv"

df = pd.read_table(file_cluster,sep="\t",header=0)


dfgeneral = df[['Cluster', 'Size', 'Trypanosoma', 'Leishmaniinae', 'Blechomonas','Paratrypanosoma']]

dfgeneral.columns = ['CLUSTER','SIZE','TRYPANOSOMA','LEISHMANIINAE','BLECHOMONAS','PARATRYPANOSOMA']

species = ['Cluster', 'Size', 'Trypanosoma', 'Leishmaniinae', 'Blechomonas','Paratrypanosoma','Trypanosoma_vivax', 'Trypanosoma_cruzi','Trypanosoma_congolense', 'Trypanosoma_brucei', 'Trypanosoma_rangeli','Trypanosoma_theileri', 'Trypanosoma_evansi', 'Trypanosoma_grayi','Leishmania_aethiopica', 'Leishmania_tropica', 'Leishmania_panamensis','Leishmania_braziliensis', 'Leishmania_sp', 'Leishmania_major','Leishmania_infantum', 'Leishmania_mexicana', 'Leishmania_donovani','Leishmania_amazonensis', 'Leishmania_arabica', 'Leishmania_enriettii','Leishmania_gerbilli', 'Leishmania_tarentolae', 'Leishmania_turanica','Crithidia_fasciculata', 'Endotrypanum_monterogeii','Leptomonas_pyrrhocoris', 'Leptomonas_seymouri','Paratrypanosoma_confusum', 'Blechomonas_ayalai']

dfspecies = df[species]

file_annot = "data/cluster_annotations.tsv"

dfhhblits = pd.read_table(file_annot,sep="\t",header=0)

dfhhblits.columns = ['Cluster', 'HMM Length', 'PDB70 (1)', 'PDB70 (2)', 'PDB70 (3)', 'PFAM_A (1)', 'PFAM_A (2)', 'PFAM_A (3)', 'SCOP70 (1)', 'SCOP70 (2)', 'SCOP70 (3)', 'UNICLUST30 (1)', 'UNICLUST30 (2)', 'UNICLUST30 (3)']

dfhhblits = dfhhblits[['Cluster', 'HMM Length', 'UNICLUST30 (1)', 'UNICLUST30 (2)', 'UNICLUST30 (3)', 'PFAM_A (1)', 'PFAM_A (2)', 'PFAM_A (3)', 'PDB70 (1)', 'PDB70 (2)', 'PDB70 (3)', 'SCOP70 (1)', 'SCOP70 (2)', 'SCOP70 (3)']]


pubmed_file ="data/pubmed_cluster.tsv"

dfpubmed = pd.read_table(pubmed_file,sep="\t",header=None,names=["Cluster","Id","Title","Journal","Year"])



cluster_dropdown = html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Cluster''')],style={"margin-bottom": "30px","margin-left": "30%"}),
    html.Div(
        children=[
            dcc.Dropdown(
                id='query-cluster-dropdown',
                options=[
                    {'label': i, 'value': i} for i in set(dfgeneral["CLUSTER"])
                ],
                multi=False,
                searchable=True,
                value=dfgeneral["CLUSTER"].iloc[0] #Start query value
            )
        ],style={"margin-right":"100px","width": "400px"}
    )]
)



info_dropdown = html.Div([
    html.Hr(),
    html.Div([dcc.Markdown('''### Information''')],style={"margin-bottom": "30px","margin-left": "30%"}),
    html.Div(
    children=[
    dcc.Dropdown(
        id='options-dropdown',
        options=[{'label': k, 'value': k} for k in ["ORGANISM","ANNOTATION","PUBLICATIONS","PRODUCT","COMMENTS",'EC NUMBER','TIGRRFAM','SUPERFAMILY','SMART','PROSITE','PIRSF','PFAM','INTERPRO','TM COUNT','SIGNAL P']],
        value=dfextra.columns[1]
    ),
    ],style={"width": "236px"},
    )]
)


layout = html.Div([
    header.layout,
    generate_cluster_dash_table(dfgeneral),
    html.Div(children=[cluster_dropdown,info_dropdown],className=" four columns",style={"display":"flex","margin-bottom": "50px","margin-left":"2%"}),
    html.Div(id='cluster-table')
])

@app.callback(
    Output('cluster-sorting-filtering', 'data'),
    [Input('cluster-sorting-filtering', 'pagination_settings'),
     Input('cluster-sorting-filtering', 'sorting_settings'),
     Input('cluster-sorting-filtering', 'filtering_settings')])
def update_graph(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = dfgeneral
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            print(col_name,filter_value)
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


# @app.callback(
#     Output('pubmed-sorting-filtering', 'data'),
#     [Input('pubmed-sorting-filtering', 'pagination_settings'),
#      Input('pubmed-sorting-filtering', 'sorting_settings'),
#      Input('pubmed-sorting-filtering', 'filtering_settings')])
# def update_graph(pagination_settings, sorting_settings, filtering_settings):
#     filtering_expressions = filtering_settings.split(' && ')
#     dff = df_individual_pubmed
#     for filter in filtering_expressions:
#         if ' eq ' in filter:
#             col_name = filter.split(' eq ')[0]
#             filter_value = filter.split(' eq ')[1]
#             print(col_name,filter_value)
#             if col_name == "CLUSTER":
#                 dff = dff.loc[dff[col_name] == int(filter_value)]
#             else:
#                 dff = dff.loc[dff[col_name] == filter_value]
#         if ' > ' in filter:
#             col_name = filter.split(' > ')[0]
#             filter_value = float(filter.split(' > ')[1])
#             dff = dff.loc[dff[col_name] > filter_value]
#         if ' < ' in filter:
#             col_name = filter.split(' < ')[0]
#             filter_value = float(filter.split(' < ')[1])
#             dff = dff.loc[dff[col_name] < filter_value]

#     if len(sorting_settings):
#         dff = dff.sort_values(
#             [col['column_id'] for col in sorting_settings],
#             ascending=[
#                 col['direction'] == 'asc'
#                 for col in sorting_settings
#             ],
#             inplace=False
#         )

#     return dff.iloc[
#         pagination_settings['current_page']*pagination_settings['page_size']:
#         (pagination_settings['current_page'] + 1) *
#         pagination_settings['page_size']
#     ].to_dict('rows')


@app.callback(
    dash.dependencies.Output('cluster-table', 'children'),
    [dash.dependencies.Input('query-cluster-dropdown', 'value'),
    dash.dependencies.Input('options-dropdown', 'value')])
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
        dfcluster_species = pd.DataFrame({"label":labels,"value":values})
        return html.Div([
                    html.H6([""],
                            className="h6_gene_individual_table gs-header gs-table-header padded"
                            ),
                    html.Table(make_dash_pretty_table(dfcluster_species),className="gene_individual_table")
                ], className="twelve columns about_text")
