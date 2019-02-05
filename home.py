import header
from app import app

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


import pandas as pd 

cluster_info = "data/cluster_info.tsv"

cluster_dataframe = pd.read_csv(cluster_info,sep="\t",header=0)


dark_summary = "data/dark_summary.tsv"

dark_dataframe = pd.read_csv(dark_summary,sep="\t",header=0)

genus_summary = "data/genus_summary.tsv"

genus_dataframe = pd.read_csv(genus_summary,sep="\t",header=0)





def create_graph_cluster_size_distribution(cluster_dataframe):
    total_cluster = len(cluster_dataframe)
    cluster_of_size_1 = len(cluster_dataframe[cluster_dataframe["Size"] == 1])
    cluster_of_size_2_10 = len(cluster_dataframe[(cluster_dataframe["Size"] > 1) & (cluster_dataframe["Size"] <= 10)])
    cluster_of_size_11_50 = len(cluster_dataframe[(cluster_dataframe["Size"] > 10) & (cluster_dataframe["Size"] <= 50)])
    cluster_of_size_50_plus = len(cluster_dataframe[(cluster_dataframe["Size"] > 50)])
    return [go.Bar(
    text = [str(round((total_cluster/total_cluster)*100)) + " %",str(round((cluster_of_size_1/total_cluster)*100)) + " %",str(round((cluster_of_size_2_10/total_cluster)*100)) + " %",str(round((cluster_of_size_11_50/total_cluster)*100)) + " %",str(round((cluster_of_size_50_plus/total_cluster)*100)) + " %"],

    x = ["All","1","2-10","11-50","50 +"],
    y=[total_cluster,cluster_of_size_1,cluster_of_size_2_10,cluster_of_size_11_50,cluster_of_size_50_plus],

    marker=dict(
        color='#da1818',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5,
        )
    ))]


dropdown_taxa = html.Div([
    html.Div(
        children=[
            dcc.Dropdown(
                id='taxa-cluster-dropdown',
                options=[
                    {'label': i, 'value': i} for i in ['All','Trypanosoma', 'Leishmaniinae', 'Blechomonas','Paratrypanosoma']
                ],
                multi=False,
                searchable=False,
                clearable=False,
                value="All"
            )
        ],style={"margin-left":"5%","width": "50%"}
    )]
)


dropdown_genus = html.Div([
    html.Div(
        children=[
            dcc.Dropdown(
                id='genus-cluster-dropdown',
                options=[
                    {'label': i, 'value': i} for i in ['Trypanosoma', 'Leishmaniinae', 'Blechomonas','Paratrypanosoma']
                ],
                multi=False,
                searchable=False,
                clearable=False,
                value="Trypanosoma"
            )
        ],style={"margin-left":"5%","width": "50%"}
    )]
)

dropdown_summary = html.Div([
    html.Div(
        children=[
            dcc.Dropdown(
                id='hyp-cluster-dropdown',
                options=[
                    {'label': i, 'value': i.replace(" %","")} for i in ['0 %', '50 %', '80 %','100 %']
                ],
                multi=False,
                searchable=False,
                clearable=False,
                value="0"
            )
        ],style={"margin-left":"5%","width": "50%"}
    )]
)




layout = html.Div([
    header.layout_home,
    html.Div([dcc.Markdown('''# Cluster Exploration:''')],style={"margin-bottom": "30px","margin-left": "3%"}),
    html.Hr(),
    html.Div([dcc.Markdown('''### Sizes:''')],style={"margin-bottom": "30px","margin-left": "3%"}),
    dropdown_taxa,
    html.Div(id="taxa-home-container"),
    html.Div([html.H6([""],className="gs-header padded",style={"height": "22px","margin-bottom":"30px","background":"#152d42"})], className="twelve columns about_text"),
    html.Div([dcc.Markdown('''### Genus:''')],style={"margin-bottom": "30px","margin-left": "3%"}),
    dropdown_genus,
    html.Div(id="genus-home-container"),
    html.Div([html.H6([""],className="gs-header padded",style={"height": "22px","margin-bottom":"30px","background":"#152d42"})], className="twelve columns about_text"),
    html.Div([dcc.Markdown('''### Annotations:''')],style={"margin-bottom": "30px","margin-left": "3%"}),
    dropdown_summary,
    html.Div(id="summary-home-container"),
    html.Hr()
])


@app.callback(
    dash.dependencies.Output('genus-home-container', 'children'),
    [dash.dependencies.Input('genus-cluster-dropdown', 'value')])
def make_taxa_plot(genus):
    x = ['All', 'Trypanosoma', 'Leishmaniinae', 'Paratrypanosoma', 'Blechomonas']
    y = genus_dataframe[genus_dataframe["Genus"] == genus].values[0][1:].tolist()
    if genus == "Trypanosoma":
        text = ["Trypanosoma: >= 5\nLeishmaniinae: >= 5\nParatrypanosoma: >= 1\nBlechomonas: >= 1\n","Only in Trypanosoma (>=5)","Trypanosoma and Leishmaniinae (>=5; >=5)","Trypanosoma and Paratrypanosoma (>=5; >=1)","Trypanosoma and Blechomonas (>=5; >=1)"]
    if genus == "Leishmaniinae":
        text = ["Trypanosoma: >= 5\nLeishmaniinae: >= 5\nParatrypanosoma: >= 1\nBlechomonas: >= 1\n","Leishmaniinae and Trypanosoma (>=5; >=5)","Only in Leishmaniinae (>=5)","Leishmaniinae and Paratrypanosoma (>=5; >=1)","Leishmaniinae and Blechomonas (>=5; >=1)"]
    if genus == 'Paratrypanosoma':
        text = ["Trypanosoma: >= 5\nLeishmaniinae: >= 5\nParatrypanosoma: >= 1\nBlechomonas: >= 1\n","Paratrypanosoma and Trypanosoma (>=1; >=5)","Paratrypanosoma and Leishmaniinae (>=1; >=5)","Only in Paratrypanosoma (>=1)","Paratrypanosoma and Blechomonas (>=1; >=1)"]
    if genus == 'Blechomonas':
        text = ["Trypanosoma: >= 5\nLeishmaniinae: >= 5\nParatrypanosoma: >= 1\nBlechomonas: >= 1\n","Blechomonas and Trypanosoma (>=1; >=5)","Blechomonas and Leishmaniinae (>=1; >=5)","Blechomonas and Paratrypanosoma (>=1; >=1)","Only in Blechomonas (>=1)"]
    data = [go.Bar(
        y = y,
        x =x,
        text=text,
        marker=dict(
            color='#da1818',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ))]
    return html.Div([
        dcc.Graph(
            id='genus-distribution',
            figure={
                'data': data,
                'layout': go.Layout(
                    title="Genus Distribution",
                    yaxis={'title': 'Number of Clusters'},
                    margin={'l': 70, 'b': 25, 't': 80, 'r': 60},
                    legend={'x': 0, 'y': 1},
                )
            }
        ),
        dcc.Markdown('This graph explores the diatribution of clusters in the genus represented in DARK.',className="graph_text")
    ])


@app.callback(
    dash.dependencies.Output('summary-home-container', 'children'),
    [dash.dependencies.Input('hyp-cluster-dropdown', 'value')])
def make_taxa_plot(hyp):
    x = ['Total', 'Any', 'UNICLUST', 'PDB', 'SCOP', 'PFAM']
    if hyp =="0":
        y = dark_dataframe[dark_dataframe["list"] == "All"].values[0][1:].tolist()
    elif hyp =="50":
        y =dark_dataframe[dark_dataframe["list"] == "50"].values[0][1:].tolist()
    elif hyp =="80":
        y = dark_dataframe[dark_dataframe["list"] == "80"].values[0][1:].tolist()
    elif hyp =="100":
        y = dark_dataframe[dark_dataframe["list"] == "100"].values[0][1:].tolist()
    text = [str(round((value/y[0])*100)) + " %" for value in y]
    data = [go.Bar(
        y = y,
        x =x,
        text=text,
        marker=dict(
            color='#da1818',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ))]
    return html.Div([
        dcc.Graph(
            id='annotation-distribution',
            figure={
                'data': data,
                'layout': go.Layout(
                    title="Annotation Summary",
                    yaxis={'title': 'Number of Clusters'},
                    margin={'l': 70, 'b': 25, 't': 80, 'r': 60},
                    legend={'x': 0, 'y': 1},
                )
            }
        ),
        dcc.Markdown('This graph explores the number of clusters annotated by DARK.',className="graph_text")
    ])


@app.callback(
    dash.dependencies.Output('taxa-home-container', 'children'),
    [dash.dependencies.Input('taxa-cluster-dropdown', 'value')])
def make_taxa_plot(taxa):
    if taxa == "All":
        return html.Div([
        dcc.Graph(
            id='cluster-size-distribution',
            figure={
                'data': create_graph_cluster_size_distribution(cluster_dataframe),
                'layout': go.Layout(
                    title="Cluster Size Distribution",
                    xaxis={'title': 'Cluster Size'},
                    yaxis={'title': 'Number of Clusters'},
                    #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                )
            }
        ),
        dcc.Markdown('This graph explores the number of clusters formed from all the proteins present in the TriTrypDB database.\n A large percentage of unique Cluster is observed, which is probably due to non-real proteins.',className="graph_text")
    ])
    elif taxa == "Trypanosoma":
        y = [len(cluster_dataframe[(cluster_dataframe[specie] > 0)]) for specie in ['Trypanosoma','Trypanosoma_vivax', 'Trypanosoma_cruzi', 'Trypanosoma_congolense', 'Trypanosoma_brucei', 'Trypanosoma_rangeli','Trypanosoma_theileri', 'Trypanosoma_evansi', 'Trypanosoma_grayi']]
        x = ['Trypanosoma','Trypanosoma vivax', 'Trypanosoma cruzi', 'Trypanosoma congolense', 'Trypanosoma brucei', 'Trypanosoma rangeli','Trypanosoma theileri', 'Trypanosoma evansi', 'Trypanosoma grayi']
        text = ["unique protein cluster: % " + str(round(len(cluster_dataframe[(cluster_dataframe[specie] == 1)])/len(cluster_dataframe[(cluster_dataframe[specie] > 0)])*100)) for specie in ['Trypanosoma','Trypanosoma_vivax', 'Trypanosoma_cruzi', 'Trypanosoma_congolense', 'Trypanosoma_brucei', 'Trypanosoma_rangeli','Trypanosoma_theileri', 'Trypanosoma_evansi', 'Trypanosoma_grayi']]

    elif taxa == "Leishmaniinae":
        y = [len(cluster_dataframe[(cluster_dataframe[specie] > 0)]) for specie in ['Leishmaniinae','Leishmania_aethiopica', 'Leishmania_tropica', 'Leishmania_panamensis', 'Leishmania_braziliensis', 'Leishmania_sp', 'Leishmania_major', 'Leishmania_infantum', 'Leishmania_mexicana', 'Leishmania_donovani', 'Leishmania_amazonensis', 'Leishmania_arabica', 'Leishmania_enriettii', 'Leishmania_gerbilli', 'Leishmania_tarentolae', 'Leishmania_turanica', 'Crithidia_fasciculata', 'Endotrypanum_monterogeii', 'Leptomonas_pyrrhocoris', 'Leptomonas_seymouri']]
        x = ['Leishmaniinae','Leishmania aethiopica', 'Leishmania tropica', 'Leishmania panamensis', 'Leishmania braziliensis', 'Leishmania sp', 'Leishmania major', 'Leishmania infantum', 'Leishmania mexicana', 'Leishmania donovani', 'Leishmania amazonensis', 'Leishmania arabica', 'Leishmania enriettii', 'Leishmania gerbilli', 'Leishmania tarentolae', 'Leishmania turanica', 'Crithidia fasciculata', 'Endotrypanum monterogeii', 'Leptomonas pyrrhocoris', 'Leptomonas seymouri']
        text = ["unique protein cluster: % " + str(round(len(cluster_dataframe[(cluster_dataframe[specie] == 1)])/len(cluster_dataframe[(cluster_dataframe[specie] > 0)])*100)) for specie in ['Leishmaniinae','Leishmania_aethiopica', 'Leishmania_tropica', 'Leishmania_panamensis', 'Leishmania_braziliensis', 'Leishmania_sp', 'Leishmania_major', 'Leishmania_infantum', 'Leishmania_mexicana', 'Leishmania_donovani', 'Leishmania_amazonensis', 'Leishmania_arabica', 'Leishmania_enriettii', 'Leishmania_gerbilli', 'Leishmania_tarentolae', 'Leishmania_turanica', 'Crithidia_fasciculata', 'Endotrypanum_monterogeii', 'Leptomonas_pyrrhocoris', 'Leptomonas_seymouri']]

    elif taxa == "Blechomonas":
        y = [len(cluster_dataframe[(cluster_dataframe["Blechomonas_ayalai"] > 0)])]
        x = ["Blechomonas ayalai"]
        text = ["unique protein cluster: % " + str(round(len(cluster_dataframe[(cluster_dataframe[specie] == 1)])/len(cluster_dataframe[(cluster_dataframe[specie] > 0)])*100)) for specie in ["Blechomonas_ayalai"]]

    else:
        y = [len(cluster_dataframe[(cluster_dataframe["Paratrypanosoma_confusum"] > 0)])]
        x = ["Paratrypanosoma confusum"]
        text = ["unique protein cluster: % " + str(round(len(cluster_dataframe[(cluster_dataframe[specie] == 1)])/len(cluster_dataframe[(cluster_dataframe[specie] > 0)])*100)) for specie in ["Paratrypanosoma_confusum"]]

    data = [go.Bar(
        y = y,
        x =x,
        text=text,
        marker=dict(
            color='#da1818',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ))]
    return html.Div([
        dcc.Graph(
            id='taxa-distribution',
            figure={
                'data': data,
                'layout': go.Layout(
                    title="Cluster Size By Taxa",
                    yaxis={'title': 'Total Clusters'},
                    margin={'l': 70, 'b': 95, 't': 80, 'r': 60},
                    legend={'x': 0, 'y': 1},
                )
            }
        ),
        dcc.Markdown('This graph explores the number of clusters formed in each genus present in the TriTrypDB database.',className="graph_text")
    ])