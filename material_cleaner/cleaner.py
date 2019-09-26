# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:47:23 2019

@author: Abhis
"""
import nltk
from nltk.corpus import stopwords
import re
import spacy
from spacy.tokens import Doc
#tokenizer
class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab
    def __call__(self,text):
        words = text.split()
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)  
    
from nltk.stem import PorterStemmer 
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class text_cleaner(object):
    
    stop_words = stopwords.words('english')+list(punctuation)
    reg = '^[¢‘»®™•°/’!"#$%&\€Ÿ\'()*+\,\,-./:;<=>?@[\]^_`{|}~\“\”]+' # removes from start
    reg1 = '[¢‘»®™•°/’!"#$%&\€Ÿ\'()*+\,\,-./:;<=>?@[\]^_`{|}~\“\”]+$' # removes from end
    reg2 = '^[¢‘»®™•°/’!"#$%&\\'()*+\,\,-./:;<=>?@[\]^_`{|}~\“\”0-9]+$' # if word only had these
    remove_reg = "[!$=?@^~°*º]" 
    ps = PorterStemmer()
    nlp = spacy.load('en_core_web_sm')
    nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)
    
    with open('stemmeshfinal.txt','r') as f:
        content = f.read().split()
    
    with open('stemplus.txt','r') as f:
        content1 = f.read().split()  
        

    @classmethod
    def tokenise(cls, text):
        mat = nltk.word_tokenize(text)
        mat = ' '.join(mat)
        mat = re.split(r"[:+\.\s|]|\b[0-9]?[a-z]?\'[a-z]?[0-9]?\b|\b[a-z]?\,[a-z]?\b",mat)
        return mat
    
    @classmethod
    def rem_stopwords(cls, text):
        mat = list(set([w for w in text if not w in cls.stop_words]))
        return mat
    
    @classmethod
    def rem_reg(cls, text):
        mat1=[]
        for w in text:
            if w=='':
                continue
            w = re.sub("(\'s)$",'',w)
            w = re.sub("(\`s)$",'',w)
            w = re.sub(cls.reg,'',w)
            w = re.sub(cls.reg1,'',w)
            w = re.sub("[\‟\′\'�_]",'',w)
            w = re.sub(cls.reg2,'',w)
            if re.search(cls.remove_reg,w):
                continue
            elif re.search('[mk]?[cmlgin]{0,3}/[mk]?[cmlgin]{0,3}|fig',w):
                continue
            elif re.search('^(.[/-_])+.?$',w):
                continue
            elif 3<=len(w)<45:
                w = re.sub("[\‟\′\'�_]",'',w)
                mat1.append(w)
        return mat1

    @classmethod   
    def rem_spac(cls,text):
        text = ' '.join(text)
        doc = cls.nlp(text)
        text1 =[token.text for token in doc if not token.pos_ == "VERB"] #in #['AFX','JJR','JJS','RBR','RBS','VBD','VBN']]
        return text1
    
    @classmethod
    def rem_dic_stem(cls,text):
        text = [ w for w in text if cls.ps.stem(w) not in cls.content]
        text = [w for w in text if w not in cls.content1]
        return text
    
    @classmethod
    def join_words(cls,text):
        return ' '.join(text)
    
    @classmethod
    def __run__(cls,text):
        mat = cls.tokenise(text=text)
        mat = cls.rem_stopwords(text=mat)
        mat = cls.rem_reg(text=mat)
        mat = cls.rem_spac(text=mat)
        mat = cls.rem_dic_stem(text=mat)
        mat = cls.join_words(text=mat)
        return mat

    @classmethod
    def abs_clean(cls,text,per_dict=True):
        #mat = cls.tokenise(text=text)
        mat = cls.rem_stopwords(text=text)
        mat = cls.rem_reg(text=mat)
        mat = cls.rem_spac(text=mat)
        if per_dict:
            mat = cls.rem_dic_stem(text=mat)
        mat = cls.join_words(text=mat)
        return mat

    
    
    
# for key, value  in ra_text.items():
#     value = text_cleaner.__run__(value)
#     ra_text[key] = value    


# =============================================================================
# 
# 
# class tfidf(object):
#     
#     
#     @classmethod
#     def toke(text):
#         text = text.split()
#         return text
#       
#         
#     def __init__(self,doc,max_df,cls.toke):
#         self.doc = doc
#         self.max_df = max_df
#         self.toke = cls.toke
#     def cv(self):
#         cv = CountVectorizer(max_df=self.max_df,analyzer='word',tokenizer=self.toke)
#         word_count_vector = cv.fit_transform(docs)
#         
#         
#         
# =============================================================================
# =============================================================================
#         
#    =============================================================================
# 
# from sklearn.feature_extraction.text import CountVectorizer
# 
# docs = dataset.pre_processing.tolist()
# def toke(text):
#     text = text.split()
#     return text
#     
# cv = CountVectorizer(max_df=0.70,analyzer='word',tokenizer=toke)
# word_count_vector = cv.fit_transform(docs)
# 
# 
# list(cv.vocabulary_.keys())[:10]
# 
# 
# from sklearn.feature_extraction.text import TfidfTransformer
# tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
# tfidf_transformer.fit(word_count_vector)
# feature_names = cv.get_feature_names()
# 
# def sort_coo(coo_matrix):
#     tuples = zip(coo_matrix.col, coo_matrix.data)
#     return sorted(tuples, key=lambda x:(x[1],x[0]), reverse = True)
# 
# def extract_topn_from_vector(feature_names, sorted_items, topn=10):
#     """get the feature names and tf-idf score of top n items"""
#     
#     #use only topn items from vector
#     sorted_items = sorted_items[:topn]
#  
#     score_vals = []
#     feature_vals = []
#     
#     # word index and corresponding tf-idf score
#     for idx, score in sorted_items:
#         
#         #keep track of feature name and its corresponding score
#         score_vals.append(round(score, 3))
#         feature_vals.append(feature_names[idx])
#  
#     #create a tuples of feature,score
#     #results = zip(feature_vals,score_vals)
#     results= {}
#     for idx in range(len(feature_vals)):
#         results[feature_vals[idx]]=score_vals[idx]
#     
#     return results
# 
# 
# keywords=[]
# for item in docs:
#      tf_idf_vector=tfidf_transformer.transform(cv.transform([item]))
#      sorted_items=sort_coo(tf_idf_vector.tocoo())
#      keyl = extract_topn_from_vector(feature_names,sorted_items,10000)
#      keyw=[key for key in keyl.keys()]
#      keywords.append(keyw)
# 
# for i in range(len(keywords)):
#     item = keywords[i]
#     wojoi = ' '.join(item)
#     keywords[i] = wojoi
#       
# =============================================================================
    
# =============================================================================
# cl = text_cleaner()
# mat = cl.tokenise(text=text)
# mat = cl.rem_stopwords(text=mat)
# mat = cl.rem_reg(text=mat)
# mat = cl.rem_spac(text=mat)
# mat = cl.rem_dic_stem(text=mat)
# mat = cl.join_word(text=mat)
# =============================================================================
        
        