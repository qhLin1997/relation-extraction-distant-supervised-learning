#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Version : Python 3.6

import json
import spacy
import inflect
import warnings
import requests
import itertools
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

corpus = pd.read_csv("./data/corpus.csv", index_col = 0)
targetrelation = pd.read_csv("./data/targetrelation.csv", index_col = 0)
trl = set(targetrelation["relation"])
targetrelation = pd.read_csv("./data/targetrelation.csv", index_col = 0)
line = list(corpus["sentence"])

def getrelation(e1, e2):
    file = open("./data/props.json")
    props = json.load(file)
    ie = inflect.engine()
    url = "https://www.wikidata.org/w/api.php"
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    if ie.singular_noun(e1):
        e1 = ie.singular_noun(e1)
    if ie.singular_noun(e2):
        e2 = ie.singular_noun(e2)
    params1 = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": e1
    }
    params2 = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": e2
    }
    r1 = requests.get(url, params = params1)
    r2 = requests.get(url, params = params2)
    e12id = r1.json()["search"]
    e12id = sorted(e12id, key = lambda k: int(k["id"][1:]), reverse = False)[:2]
    e22id = r2.json()["search"]
    e22id = sorted(e22id, key = lambda k: int(k["id"][1:]), reverse = False)[:2]
    relation = []
    numE1 = len(e12id)
    numE2 = len(e22id)
    if numE1 != 0 and numE2 != 0:
        for i in range(numE1):
            for j in range(numE2):
                ide1 = e12id[i]["id"]
                ide2 = e22id[j]["id"]
                query = "SELECT ?propLabel WHERE { wd:" + ide1 + " ?prop wd:" + ide2 + ". " + "SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'. }}"
                sparql.setQuery(query)
                res = sparql.query().convert()["results"]["bindings"]
                if res != []:
                    numR = len(res)
                    for k in range(numR):
                        link = res[k]["propLabel"]["value"]
                        index = link.find("P")
                        idr = link[index:]
                        for r in props:
                            if r["id"] == idr:
                                temp = r["label"]
                        relation.append((e1, ide1, e2, ide2, temp))
    file.close()
    return set(relation)
    
warnings.filterwarnings("ignore")
nlp = spacy.load("en_core_web_lg")
label = []
for i in line:
    nlpi = nlp(i)
    entities = nlpi.ents
    numE = len(entities)
    if numE > 1:
        combination = list(itertools.permutations(entities, 2))
        info = set()
        for j in combination:
            info = info|getrelation(str(j[0]), str(j[1]))
    sublabel = set()
    for j in info:
        if j[4] in trl:
            sublabel = sublabel|{j}
        else:
            sublabel = sublabel|{(j[0], j[1], j[2], j[3], "other")}
    label.append(sublabel)

numS = len(line)
entity1 = []
eid1 = []
entity2 = []
eid2 = []
relation = []
sentence = []
for i in range(numS):
    for j in label[i]:
        entity1.append(j[0])
        eid1.append(j[1])
        entity2.append(j[2])
        eid2.append(j[3])
        relation.append(j[4])
        sentence.append(line[i])
        
labeleddata = pd.DataFrame({"entityid1":eid1, "entityid2":eid2, "entity1":entity1, "entity2":entity2, "relation":relation, "sentence":sentence, "end":"###END###"})

df1 = labeleddata.sample(frac = 0.3)
df2 = labeleddata[~labeleddata.index.isin(df1.index)]
df1.to_csv("./data/test.txt", index = False, header = False, sep = "\t")
df2.to_csv("./data/train.txt", index = False, header = False, sep = "\t")

tgrelation = targetrelation["relation"]
relationid = [i for i in range(len(tgrelation))]
realtion2id = pd.DataFrame({"relation":tgrelation, "id":relationid})
realtion2id.to_csv("./data/relation2id.txt", index = False, header = False, sep = "\t")
