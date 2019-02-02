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




