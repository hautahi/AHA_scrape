'''
This program scrapes ...
Note can only take text not images. SO the welcome in http://www.abbgen.net/ cannot be read
Also, only the Learn in http://www.abbgen.net/ that is text that can be read. SO it picks up 3
and not 5 on the page.
Author: Hautahi
Date: 28 June 2017

Bugs:
1. The "invalid schema" error pops up with the : after the .com. This repeatable (abingtonhealth)
2. The handshake failure error. Looks to only happen sometimes. Need to figure out how to use exceptions to get around it
'''

#-------------------------------------------------------------#
# 1.  Setup
#-------------------------------------------------------------#

print "Code is Working..."

import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import urlparse
import time
import csv
import unicodedata
import requests
from time import sleep
from random import uniform
from warnings import warn

#-------------------------------------------------------------#
# 2. Define Functions
#-------------------------------------------------------------#

# This function creates a soup object
def make_soup(url): 
    #sleep(uniform(0,1)) 
    response = requests.get(url)
    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Status code: {}'.format(response.status_code))
    html=response.text
    return BeautifulSoup(html, "lxml")

# This functions gets all links in webpage
def process(url):
 
    soup = make_soup(url)
    
    # Get all links on page
    odie = [urlparse.urljoin(url,tag['href']) for tag in soup.findAll('a', href=True)]
    
    # Remove duplicates
    odie = list(set(odie))  
    
    return odie

# This function gets all links in webpage and subpages excluding external links   
def get_pages(url):
    
    # Get links on main page
    links1 = process(url)
    
    # Remove outside links that don't start with url
    y = [s for s in links1 if s.startswith(url) == True]

    # Get links on each subpage
    links2 = []
    for i in y:
        print(i)
        x = process(i)
        links2 = links2+x
    links = links2+y
    
    # Remove duplicates
    links = list(set(links))
    
    # Remove outside links that don't start with url
    x = [s for s in links if s.startswith(url) == True]

    return x

# This function returns the index places of "a" in the string "text"
def get_index(text, a):
    return [i for i,x in enumerate(text.split()) if x==a]
    
# This function a list of sentences of n words around the "term" in the "text" string
def get_sentences(text,term,n):
    ind = get_index(text,term)
    sentence_list = [text.split()[max(0,i-n):i+n] for i in ind]
    sentences = [' '.join(x) for x in sentence_list]
    
    # Remove unicode
    sentences1 = [unicodedata.normalize('NFKD',x).encode('ascii','ignore') for x in sentences]
    return sentences1

# This function counts the number of occurences of keywords on each page in links
# It also returns the relevant sentences
def count_keys(links,key,n):
    Totalcount = []
    Totalsent = []
    for l in links:
        try:
            soup = make_soup(l)
        except urllib2.HTTPError, e:
            print 'Error:', e
            print(len(Totalcount))
            continue
        COUNT = [l]
        SENT = []
        for word in key:
            # Get text
            text=soup.get_text()
            
            # Get word count
            ind = get_index(text,word)
            count = len(ind)
            COUNT.append(count)
            
            # get sentences
            sentences = get_sentences(text,word,n)
            SENT.append(sentences)            
            
        Totalcount.append(COUNT)
        Totalsent.append(SENT)
    
    # Save counts to a dataframe
    headers = ['url'] + key
    d = pd.DataFrame(Totalcount,columns=headers)
    
    # Save sentences to a dataframe
    S = [[' :: '.join(val) for val in sublist] for sublist in Totalsent]
    headers = ['text-'+x for x in key]
    Sdf = pd.DataFrame(S,columns=headers)
    
    # Combine dataframes
    comb = pd.concat([d, Sdf], axis=1, join_axes=[d.index])
    
    return comb

def main_function(url,key,name,n):
    '''
    n: number of words either side for contextual text
    '''
    start_time = time.time() 
    
    # Get all subpage links and save
    print('Retrieving Links...')
    links = get_pages(url)
    dlinks = pd.DataFrame(links,columns=["sub_pages"])
    dlinks.insert(0,'hospital',name)
    dlinks.insert(1,'hospital_website',url)
    dlinks.to_csv('./output/'+name+'_subpagelinks.csv',index=False, encoding='utf-8')
    
    # Cout keywords in subpages
    print('Counting keywords...')
    links = links[0:20]  
    d = count_keys(links,key,n)
    d.insert(0,'hospital',name)
    d.insert(1,'hospital_website',url)
    d.to_csv('./output/'+name+'.csv',index=False, encoding='utf-8')
    
    print("--- %s seconds ---" % (time.time() - start_time))

#-------------------------------------------------------------#
# 3. Analysis
#-------------------------------------------------------------#

# Load data
d = pd.read_csv("./data/SIE-IMPAQ-URL-05252017.csv")
d.columns = map(str.lower, d.columns)
df = d[5:8]

# Load keywords
with open('./data/keywords.csv', 'rb') as f:
    reader = csv.reader(f)
    key_list = list(reader)
keywords = [val for sublist in key_list for val in sublist]

# Parameters
n = 10

# Loop over this    
for url, name in zip(df["website"], df["hospital name"]):
    print('Processing hospital: '+name)
    main_function(url,keywords,name,n)


