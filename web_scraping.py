# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:57:02 2019

@author: Abhis
"""

# =============================================================================
link = "https://www.ncbi.nlm.nih.gov/pmc/?term=Phenylketonuria"
# import requests
# r = requests.get(link).text
# from bs4 import BeautifulSoup as bs
# soup = bs(r,'lxml')
# t = soup.find_all('div',{'class':'rprt'})
# t[0].find('div',{'class':'rslt'}).div.a["href"]
# =============================================================================



d=[]


#use selenium to open browser and load ajax content
import pdb
import os
import functools 
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException    

    
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def random_proxy(): 
    r = requests.get("http://34.213.20.241/?Key=PROFEZA").text.split('\\')[1][1:]  #newline
    proxy = r #random.choice(proxiess)}
    return proxy

def abs_extractor(link):
    driver1 = webdriver.Chrome(path,options = options)
    driver1.get(link)
    

#page_links = []
def appender_text(html):
    global d
    #pdb.set_trace()
    soup = bs(html,'lxml')
    cit_link = soup.find_all('div',{'class','rprt'})
    for tag in cit_link:
        abs_link = tag.find('div',{'class':'rslt'}).div.a["href"]
        abs_link = "https://www.ncbi.nlm.nih.gov"+str(abs_link)
        d.append(abs_link)
        #abs_extractor(link=abs_link)
        

def selenium_wrap(f):
    @functools.wraps(f)
        def funtion_that_runs_f():
            print("start")
            f()
            print("after")
        return funtion_that_runs_f

def selen():
    prox = proxy_setter()
    path = os.getcwd()+"\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    profile = {
               "plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               #"download.default_directory": download_folder,
               "download.extensions_to_open": ""
                }
    options.add_experimental_option("prefs", profile)
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    driver = webdriver.Chrome(path,options = options)
    
    
        


prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
r_prox = random_proxy()
prox.http_proxy = r_prox
prox.socks_proxy = r_prox
prox.ssl_proxy = r_prox
path = os.getcwd()+"\\chromedriver.exe"
options = webdriver.ChromeOptions()
profile = {
           "plugins.plugins_list": [{"enabled": False,
                                     "name": "Chrome PDF Viewer"}],
           #"download.default_directory": download_folder,
           "download.extensions_to_open": ""
            }
options.add_experimental_option("prefs", profile)
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)
driver = webdriver.Chrome(path,options = options)

xpath= "//div[contains(@class,'pagination')]/a[contains(@class,'active page_link next')]"

flag = True
j=0
while flag == True:
    if j == 0:
        driver.get(link)
        print("Select the appropriate filters and then enter in the console")
        input()
    if j>1:
        driver.find_element_by_xpath(xpath=xpath).click()
    #driver.implicitly_wait(2)
    html = driver.page_source
    appender_text(html=html)
    flag = check_exists_by_xpath(xpath=xpath)
    j+=1
driver.close()

d= list(set(d))
with open('last_5_links.txt','w') as f:
    for item in d:
        f.write('%s\n'%item)       
with open('last_5_links.txt','r') as f:
    d=f.read().split()

def extract(html,link):
    global e
    soup =bs(html,'lxml')
    try:
        doi = soup.find('span',{'class','doi'}).a.text
    except:
        doi=''
    try: pmid = soup.find('div',{'class','fm-citation-pmid'}).a.text
    except: pmid = ''
    try: abstract = soup.find('div',{'class','tsec sec'}).text
    except: abstract=''
    e.append((doi,pmid,abstract,link))
    
duplicacy=[]    
e=[]
driver = webdriver.Chrome(path,options = options)

for link in d:
    if link in duplicacy:
        continue
    duplicacy.append(link)
    driver.get(link)
    html = driver.page_source
    extract(html=html,link=link)    
driver.close()   


import pandas as pd
df = pd.DataFrame(e, columns=('doi','pmid','text','link'))
df.to_csv("last_5.csv")
    
def abstract(text):
    if "go to:abstract" in text.lower():
        return "abstract"
    elif "go to:summary" in text.lower():
        return "abstract"
    else:
        return "not"

df["label1"] = df.text.apply(lambda x: abstract(x))
df.label1.value_counts()
df = df[~(df.label1=="not")]
df.to_csv("last_5_cleaned.csv")


