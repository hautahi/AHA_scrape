'''
This program scrapes ...
Note can only take text not images. SO the welcome in http://www.abbgen.net/ cannot be read
Also, only the Learn in http://www.abbgen.net/ that is text that can be read. SO it picks up 3
and not 5 on the page.
Author: Hautahi
Date: 28 June 2017
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

#-------------------------------------------------------------#
# 2. Define Functions
#-------------------------------------------------------------#

# This function creates a soup object
def make_soup(url):
    html = urllib2.urlopen(url).read()
    #req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    #html = urllib2.urlopen(req).read()    
    return BeautifulSoup(html, "lxml")

# This functions gets all links in webpage
def process(url):
 
    soup = make_soup(url)
    
    # Get all links on page
    # odie = [link.get('href') for link in soup.find_all('a',href=re.compile(''))]
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
        x = process(i)
        links2 = links2+x
    links2 = links2+y
    
    # Remove duplicates
    links2 = list(set(links2))
    
    # Remove outside links that don't start with url
    x = [s for s in links2 if s.startswith(url) == True]

    return x

# This function counts the number of occurences of keywords on each page in links
def count_keys(links,key):
    Totalcount = []
    for l in links:
        try:
            soup = make_soup(l)
        except urllib2.HTTPError, e:
            print 'Error:', e
            print(len(Totalcount))
            continue
        COUNT = [l]
        for word in key:
            # This gets number of blocks it occurs in
            #odie = soup.find_all(text=lambda x: x and word in x.lower())
            #count = len(odie)
            # But we actually want word count right
            text=soup.get_text()
            count=text.lower().count(word)
            COUNT.append(count)
        Totalcount.append(COUNT)
    
    # Save to a dataframe
    headers = ['url']+key
    d = pd.DataFrame(Totalcount,columns=headers)
    return d

def main_function(url,key,name):
    
    start_time = time.time() 
    
    links = get_pages(url)
    
    #links = links[0:50]  
    d = count_keys(links,key)
    d['hospital'] = name
    d['hospital_website'] = url
    
    cols = ['hospital','hospital_website','url'] + keywords
    d = d[cols]
    d.to_csv('./output/'+name+'.csv',index=False)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
#-------------------------------------------------------------#
# 3. Analysis
#-------------------------------------------------------------#

# Load data
d = pd.read_csv("./data/SIE-IMPAQ-URL-05252017.csv")
d.columns = map(str.lower, d.columns)
df = d[0:1]

# Load keywords
with open('./data/keywords.csv', 'rb') as f:
    reader = csv.reader(f)
    key_list = list(reader)
keywords = [val for sublist in key_list for val in sublist]

# Loop over this    
for url, name in zip(df["website"], df["hospital name"]):
    print('Processing hospital: '+name)
    main_function(url,keywords,name)
