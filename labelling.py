# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:20:43 2019

@author: Abhis
"""

import pandas as pd
import re
import json

data = pd.read_csv('keywords_tfidf.csv')
labels = pd.read_excel('PhenylKetonuria_group_keywords_1.xlsx')

label_d={}
for row in labels.iterrows():
    label_d[row[1]["label"]] = row[1]["Words"]


def matcher(text,label):
    "label - for which label"
    
    corpus = text.lower().split(' ')
    words = label_d[label].lower().split(',')
    
    m = {}
    for w in words:
        w = w.strip()
        for t in corpus:
            t = t.strip()
            if w == t:
                if not w in m.keys():
                    reg = "\S+?\s?\S+?\s?\S+?\s?\S+?\s?\S+?\s?\S+?\s?"+str(w)+"\s\S+?\s\S+?\s\S+?\s\S+?\s\S+?" #"(\S+?\s+?){0,7}"+str(w)+"\s(\S+?\s+?){0,7}"
                    textn = re.findall(reg, str(text).lower())
                    m[w] = {"freq":1,
                             "string":textn}
                    #m[w]["freq"] = 1
                    #m[w]["string"] = text
                    continue
                m[w]["freq"] += 1
                
    return json.dumps(m)


titles = label_d.keys()


for label in  titles:
    data[label] = data.tfidf.apply(lambda x: matcher(text=x,label=label))
    
    
data.to_csv("labelling_done_1.csv")
data.to_excel("labelling_done_1.xlsx")