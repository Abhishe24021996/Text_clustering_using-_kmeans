# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:25:36 2019

@author: Abhis
"""

import pandas as pd
import scispacy
import spacy
import time
import os
import sys

filename =sys.argv[1]


models = ["en_ner_bionlp13cg_md","en_ner_bc5cdr_md","en_ner_jnlpba_md","en_ner_craft_md"]

def entity_file(model="en_ner_bionlp13cg_md", directory="scispacy"+str(time.time()).split('.')[0]):
    if not os.path.exists(directory):
        os.mkdir(directory)
    data = pd.read_csv('last_5_final.csv')  #filename
    nlp = spacy.load(model)
    doct = data.text.tolist()
    for idx,item in enumerate(doct):
        try:
            doc = nlp(item)
        except Exception as e: 
            print(e)
            continue       
        m={}
        for ent in doc.ents:
            if not ent.label_ in m.keys():
                m[ent.label_] = [ent.text]
                continue
            m[ent.label_].append(ent.text)
        for key, value in m.items():
            data.loc[idx,key] = ' , '.join(value)    
        print(idx)
    data.to_csv(os.path.join(directory,model+".csv"))
    
    
if __name__ == "__main__":
    for model in models:
        entity_file(model=model)