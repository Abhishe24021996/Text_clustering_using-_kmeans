import re
from nltk.corpus import stopwords
from string import punctuation
from material_cleaner.cleaner import text_cleaner
import pandas as pd


data = pd.read_csv("abstract_2sec.csv")

#first cleaned the text as it containsirregularities

def structure_1(text):
    text = text.lower()
    #substituting the known irregularities as from scraping
    text = text.replace("go to:abstract","")
    text = text.replace("go to:summary","")
    #removing last keywords as not needed using regex
    text = re.sub("\.keywords:.+","",text)
    return text.strip()

data.text = data.text.apply(lambda x : structure_1(x))

data.to_csv('finaldata111.csv')

def r_stopwords(text):
    text = [word for word in text.split() if not word in stop_words]
    return ' '.join(text)


data.text = data.text.apply(lambda x : text_cleaner.__run__(x))

#list of documents 
documents = data.text.tolist()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8,lowercase=True)
doc_vec = vectorizer.fit_transform(documents)

dtm = pd.DataFrame(doc_vec.toarray().transpose(), index = vectorizer.get_feature_names(), columns= data.doi.tolist())
import numpy as np
arr = np.array(dtm)

import matplotlib.pyplot as plt
# Using the elbow method to find the optimal number of clusters
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42,max_iter = 100, n_init = 10)
    kmeans.fit(arr)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 15), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


# no. of cluster == 5, 6, 10
n=5
model = KMeans(n_clusters=n, init='k-means++', max_iter = 100, n_init = 10)
model.fit(doc_vec.transpose())


import string
import collections
clustering = collections.defaultdict(list)
terms = vectorizer.get_feature_names()
for idx, label in enumerate(model.labels_):
    clustering[label].append(terms[idx])
print(dict(clustering))











keys=[0,1,2,3]
keywords=dict.fromkeys(keys, [])







keyword={}
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(n):
    print("Cluster %d:" % i),
    for ind in order_centroids[i,]:
        a=terms[ind]
        print(' %s' %a)
        if i in keyword.keys():
            keyword[i] += [a]
            continue
        keyword[i] = [a]
        


print("\n")
print("Prediction")



 



