# coding=utf-8
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import os
import datetime



from app import app
import header





list_box = html.Div([
    html.Div([dcc.Markdown('''### Genes''')],style={"margin-bottom": "0px","margin-left": "47%"}),
    html.Div(id='list-genes-container',
    children=[
        dcc.Textarea(
            id='list_gene_terms',
            title='Enter (one by line) genes to retrieve information',
            className='area-text',
            style={"margin-left": "31%","height": "200px","width": "40%","margin-bottom": "0px","margin-top": "20px"},
            value='Tb927.5.440\nTb927.5.640\nTb927.7.6830\nTb927.7.6850\nTb927.7.7480\nTb927.8.7340\nTb927.8.7350\nTb05.5K5.260'
        )
    ]
    ),
    html.Button("Compute",id="get-list-btn",style={"margin-bottom": "0px","margin-top": "30px","margin-left": "45.5%"})
    ]
)




layout = html.Div([
    header.layout_gene_list,
    list_box,
    html.Div(id="return-button",style={"margin-bottom": "0px","margin-top": "30px","margin-left": "5%"})
    ])



@app.callback(dash.dependencies.Output("return-button","children"), [dash.dependencies.Input('get-list-btn', 'n_clicks')],[dash.dependencies.State('list_gene_terms','value')])
def on_click(number_of_times_button_has_clicked,gene_list_value):
    if number_of_times_button_has_clicked!= None:
        gene_list_value = list(gene_list_value.split("\n"))
        if len(gene_list_value[0]) >= 3:
            now = datetime.datetime.now()
            basename = "dark_" + now.strftime("%Y-%m-%d-%H-%M")
            if not os.path.exists("DARK_RESULTS"):
                os.makedirs("DARK_RESULTS")
            output_path = os.getcwd() + "/DARK_RESULTS/"
            genes = gene_list_value
            gene_file = os.path.dirname(os.path.abspath(__file__)) + "/data/gene_info.tsv"
            df_gene_info = pd.read_table(gene_file,sep="\t",header=0)
            df_gene_info = df_gene_info[df_gene_info['primary_key'].isin(genes)].fillna("-")
            genes_info = output_path + basename + "_info.tsv"
            df_gene_info.to_csv(genes_info,sep="\t",header=True,index=False)
            gene_not_analyzed = output_path + basename + "_not_analyzed.txt"
            with open(gene_not_analyzed,"w") as fo:
                for x in genes:
                    if x not in df_gene_info['primary_key'].tolist():
                        fo.write(x+"\n")
            file_cluster = os.path.dirname(os.path.abspath(__file__)) + "/data/cluster_info.tsv"
            df_cluster = pd.read_table(file_cluster,sep="\t",header=0)
            df_cluster = df_cluster[['Cluster', 'Size', 'Trypanosoma', 'Leishmaniinae', 'Blechomonas','Paratrypanosoma']]
            df_cluster.columns = ['CLUSTER','SIZE','TRYPANOSOMA','LEISHMANIINAE','BLECHOMONAS','PARATRYPANOSOMA']
            df_cluster = df_cluster[df_cluster['CLUSTER'].isin(df_gene_info["cluster"].tolist())]
            tmp = df_gene_info[["primary_key","cluster",'gene_product']]
            tmp.columns = ["ID","CLUSTER","FUNCTION"]
            df_cluster = tmp.merge(df_cluster,on="CLUSTER")
            file_annot = os.path.dirname(os.path.abspath(__file__)) + "/data/cluster_annotations.tsv"
            dfhhblits = pd.read_csv(file_annot,sep="\t",header=0)
            dfhhblits.columns = ['CLUSTER', 'HMM L', 'PDB70 (1)', 'PDB70 (2)', 'PDB70 (3)', 'PFAM_A (1)', 'PFAM_A (2)', 'PFAM_A (3)', 'SCOP70 (1)', 'SCOP70 (2)', 'SCOP70 (3)', 'UNICLUST30 (1)', 'UNICLUST30 (2)', 'UNICLUST30 (3)']
            dfhhblits = dfhhblits[['CLUSTER','UNICLUST30 (1)', 'UNICLUST30 (2)', 'UNICLUST30 (3)', 'PFAM_A (1)', 'PFAM_A (2)', 'PFAM_A (3)', 'PDB70 (1)', 'PDB70 (2)', 'PDB70 (3)', 'SCOP70 (1)', 'SCOP70 (2)', 'SCOP70 (3)']]
            df_cluster = df_cluster.merge(dfhhblits,on="CLUSTER",how="left")
            df_cluster = df_cluster.fillna("-")
            file_cluster_results = output_path + basename + "_clusters.tsv"
            df_cluster.to_csv(file_cluster_results,sep="\t",header=True,index=False)
            pubmed_file = os.path.dirname(os.path.abspath(__file__)) + "/data/pubmed_cluster.tsv"
            dfpubmed = pd.read_table(pubmed_file,sep="\t",header=None,names=["CLUSTER","PUBMED","TITLE","JOURNAL","YEAR"])
            dfpubmed = dfpubmed[dfpubmed['CLUSTER'].isin(df_cluster["CLUSTER"].tolist())]
            dfpubmed = tmp.merge(dfpubmed,on="CLUSTER")
            file_pubmed_results = output_path + basename + "_articles.tsv"
            dfpubmed.to_csv(file_pubmed_results,sep="\t",header=True,index=False)
            go_file = os.path.dirname(os.path.abspath(__file__)) + "/data/GO_information_by_cluster.tsv"
            dfgo = pd.read_table(go_file,sep="\t",header=0, names=["CLUSTER","TYPE","GO","INFO"],dtype={"CLUSTER":"int64","GO":"str","TYPE":"str","INFO":"str"})
            dfgo = dfgo[dfgo['CLUSTER'].isin(df_cluster["CLUSTER"].tolist())]
            dfgo = tmp.merge(dfgo,on="CLUSTER")
            file_go_results = output_path + basename + "_go.tsv"
            dfgo.to_csv(file_go_results,sep="\t",header=True,index=False)
            display_line = "Finished! Look in your working directory, the folder named DARK_RESULT"
            return html.Div(display_line)
        else:
            return html.Div("Empty List!")


