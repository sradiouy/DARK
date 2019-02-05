import string 
import nltk
import pandas as pd 

#external functions

def create_words_list(dfhhblits):
    removepunct = string.punctuation #keep - and _ in text other punctuation removed
    dictremove = {}
    for punct in removepunct:
        dictremove[punct] = " "
    table = str.maketrans(dictremove) # create table to make the replacements
    dictclust = {}
    for index, row in dfhhblits.iterrows():
        dictclust[str(row.cluster)] = " ".join([*map(str.lower, nltk.word_tokenize(" ".join([value.split("[")[0] for value in row.values.tolist()[2:] if len(value.split("[")) > 1 ]).translate(table)))])
    words = []
    clusters = []
    for key,value in dictclust.items():
        if value != "":
            for word in nltk.word_tokenize(value):
                if word not in words and len(word) > 1:
                    try:
                        temp = int(word)
                    except:    
                        words.append(word)
            clusters.append([key," ".join(set(nltk.word_tokenize(value)))])
        else:
            clusters.append([key,"-"])
    fo = open("data/words.txt","w")
    for word in words:
        fo.write(word + "\n")
    df = pd.DataFrame(clusters,columns=["Cluster","Words"])


def generate_word_cluster(words_by_cluster):
    words_by_cluster  = "data/cluster_words.tsv"
    dfwords = pd.read_csv(words_by_cluster,sep="\t",header=0)
    word_dict = defaultdict(list)
    for cluster in dfwords.Cluster.tolist():
        for word in dfwords[dfwords["Cluster"] == cluster].iloc[0].Words.split(" "):
            word_dict[word].append(cluster)


def create_hyp_dataframe():   
    gene_info = "data/gene_info.tsv"
    gene_dataframe = pd.read_csv(gene_info,sep="\t",header=0)
    gene_dataframe = gene_dataframe[["cluster","gene_product"]]
    cluster_product = defaultdict(list)
    for index,row in gene_dataframe.iterrows():
        try:
            check = numpy.isnan(row.gene_product)
            cluster_product[row.cluster].append("-")
        except:
            cluster_product[row.cluster].append(row.gene_product)
    cluster_hypothetical = defaultdict(list)
    for key in cluster_product:
        if len(cluster_product[key]) >= 5:
            for value in cluster_product[key]:
                if "uncharacterized" in value.lower() or "hypothetical" in value.lower() or "uncharacterised" in value.lower() or "unspecified" in value.lower() or "unknown" in value.lower() or value == "-":
                    cluster_hypothetical[key].append(1)
                else:
                    cluster_hypothetical[key].append(0)
    cluster_50 = []
    cluster_80 = []
    cluster_100 = []
    for key in cluster_hypothetical:
        percent_of_hyp = sum(cluster_hypothetical[key])/len(cluster_hypothetical[key])
        if percent_of_hyp >= 0.5:
            cluster_50.append(key)
        if percent_of_hyp >= 0.8:
            cluster_80.append(key)
        if percent_of_hyp == 1:
            cluster_100.append(key)
    pd.set_option('display.float_format','{:.0f}'.format)
    data = {"50":cluster_50,"80":cluster_80,"100":cluster_100}
    df_hyp = pd.DataFrame.from_dict(data, orient='index',dtype=numpy.int64)
    df_hyp = df_hyp.transpose()
    df_hyp = df_hyp.fillna(0)
    df_hyp = df_hyp.apply(pd.to_numeric)
    df_hyp.to_csv("data/hypothetical_cluster.tsv",sep="\t",header=True,index=False)


def generate_dataframe_hyp_info():
    annotation_info = "data/cluster_annotations.tsv"
    annotation_dataframe = pd.read_csv(annotation_info,sep="\t",header=0)
    lst_uniclust30 = []
    lst_pdb70 = []
    lst_scop70 = []
    lst_pfamA = []
    lst_full = []
    cluster = []
    for index, row in annotation_dataframe.iterrows():
        uniclust30 = row.uniclust_1
        pdb70 = row.pdb_1
        scop70 = row.scop_1
        pfamA = row.pfam_1
        if uniclust30 != "-":
            lst_uniclust30.append(1)
        else:
            lst_uniclust30.append(0)
        if pdb70 != "-":
            lst_pdb70.append(1)
        else:
            lst_pdb70.append(0)
        if scop70 != "-":
            lst_scop70.append(1)
        else:
            lst_scop70.append(0)
        if pfamA != "-":
            lst_pfamA.append(1)
        else:
            lst_pfamA.append(0)
        if uniclust30 != "-" or pdb70 != "-" or scop70 != "-" or pfamA != "-":
            lst_full.append(1)
        else:
            lst_full.append(0)
        cluster.append(row.cluster)
    data = {"cluster":cluster,"pdb":lst_pdb70,"uniclust":lst_uniclust30,"scop":lst_scop70,"pfam":lst_pfamA,"full":lst_full}
    df = pd.DataFrame(data)
    df.to_csv("data/Cluster_Annotation_summary.tsv",sep="\t",header=True,index=False)



def create_hyp_graph():
    graph_hypothetical_dataframe = open("data/dark_summary.tsv","w")
    header = "\t".join(["list","total","full","uniclust","pdb","scop","pfam"]) + "\n"
    graph_hypothetical_dataframe.write(header)
    hypothetical_info = "data/hypothetical_cluster.tsv"
    hypothetical_dataframe = pd.read_csv(hypothetical_info,sep="\t",header=0)
    cluster_annotation_summary = "data/Cluster_Annotation_summary.tsv"
    cluster_annotation_summary_dataframe = pd.read_csv(cluster_annotation_summary,sep="\t",header=0)
    lst_50 = [int(str(num).replace(".0","")) for num in hypothetical_dataframe["50"] if num != 0]
    lst_80 = [int(str(num).replace(".0","")) for num in hypothetical_dataframe["80"] if num != 0]
    lst_100 = [int(str(num).replace(".0","")) for num in hypothetical_dataframe["100"] if num != 0]
    lst_all = cluster_annotation_summary_dataframe.cluster.tolist()
    full_lists = [lst_all,lst_50,lst_80,lst_100]
    count = 0
    for type_list in full_lists:
        total_annotated = []
        total_pdb = []
        total_scop = []
        total_pfam = []
        total_uniclust = []
        count += 1
        for item in type_list:
            row = cluster_annotation_summary_dataframe[cluster_annotation_summary_dataframe['cluster'] == item]
            if len(row) == 0:
                full = 0
                pdb = 0
                scop = 0
                pfam = 0
                uniclust = 0
            else:
                full = row.full.values[0]
                pdb = row.pdb.values[0]
                scop = row.scop.values[0]
                pfam = row.pfam.values[0]
                uniclust = row.uniclust.values[0]
            total_annotated.append(full)
            total_pdb.append(pdb)
            total_scop.append(scop)
            total_pfam.append(pfam)
            total_uniclust.append(uniclust)
        if count == 1:
            name_list = "All"
        elif count == 2:
            name_list = "50"
        elif count == 3:
            name_list = "80"
        elif count == 4:
            name_list = "100"   
        y = "\t".join(map(str,[name_list,len(total_annotated),sum(total_annotated),sum(total_uniclust),sum(total_pdb),sum(total_scop),sum(total_pfam)])) + "\n"
        graph_hypothetical_dataframe.write(y)
    graph_hypothetical_dataframe.close()
    return None




def create_genus_summary_dataframe():
    cluster_info = "data/cluster_info.tsv"
    cluster_dataframe = pd.read_csv(cluster_info,sep="\t",header=0)
    genus_dataframe = cluster_dataframe[['Trypanosoma', 'Leishmaniinae', 'Blechomonas','Paratrypanosoma']]
    trypanosoma_spp = 0
    trypanosoma_leishmaniinae_spp = 0
    trypanosoma_paratrypanosoma_spp = 0
    trypanosoma_blechomonas_spp = 0
    leishmaniinae_spp = 0
    leishmaniinae_paratrypanosoma_spp = 0
    leishmaniinae_blechomonas_spp = 0
    paratrypanosoma_spp = 0
    paratrypanosoma_blechomonas_spp = 0
    blechomonas_spp = 0
    all_spp = 0

    fo = open("data/genus_summary.tsv","w")
    fo.write("Genus\tAll\tTrypanosoma\tLeishmaniinae\tParatrypanosoma\tBlechomonas\n")
    for index,row in genus_dataframe.iterrows():
        trypanosoma,leishmaniinae,paratrypanosoma,blechomonas = row.tolist()
        if trypanosoma >= 5 and leishmaniinae == 0 and paratrypanosoma == 0 and blechomonas == 0:
            trypanosoma_spp += 1
        elif trypanosoma >= 5 and leishmaniinae >= 5:
            trypanosoma_leishmaniinae_spp += 1
        elif trypanosoma >= 5 and paratrypanosoma >= 1:
            trypanosoma_paratrypanosoma_spp += 1
        elif trypanosoma >= 5 and blechomonas >= 1:
            trypanosoma_blechomonas_spp += 1
        if trypanosoma == 0 and leishmaniinae >= 5 and paratrypanosoma == 0 and blechomonas == 0:
            leishmaniinae_spp += 1
        elif leishmaniinae >= 5 and paratrypanosoma >= 1:
            leishmaniinae_paratrypanosoma_spp += 1
        elif leishmaniinae >= 5 and blechomonas >= 1:
            leishmaniinae_blechomonas_spp += 1
        if trypanosoma == 0 and leishmaniinae == 0 and paratrypanosoma >= 1 and blechomonas == 0:
            paratrypanosoma_spp += 1
        elif blechomonas == 0 and paratrypanosoma >= 1:
            paratrypanosoma_blechomonas_spp += 1
        if trypanosoma == 0 and leishmaniinae == 0 and paratrypanosoma == 0 and blechomonas >= 1:
            blechomonas_spp += 1
        if trypanosoma >= 5 and leishmaniinae >= 5 and paratrypanosoma >= 1 and blechomonas >= 1:
            all_spp += 1


    fo.write("\t".join(map(str,["Trypanosoma",all_spp,trypanosoma_spp,trypanosoma_leishmaniinae_spp,trypanosoma_paratrypanosoma_spp,trypanosoma_blechomonas_spp])) + "\n")
    fo.write("\t".join(map(str,["Leishmaniinae",all_spp,trypanosoma_leishmaniinae_spp,leishmaniinae_spp,leishmaniinae_paratrypanosoma_spp,leishmaniinae_blechomonas_spp])) + "\n")
    fo.write("\t".join(map(str,['Paratrypanosoma',all_spp,trypanosoma_paratrypanosoma_spp,leishmaniinae_paratrypanosoma_spp,paratrypanosoma_spp,paratrypanosoma_blechomonas_spp])) + "\n")
    fo.write("\t".join(map(str,['Blechomonas',all_spp,trypanosoma_blechomonas_spp,leishmaniinae_blechomonas_spp,paratrypanosoma_blechomonas_spp,blechomonas_spp])) + "\n")
    fo.close()
    return None