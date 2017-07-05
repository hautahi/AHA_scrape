'''
This program scrapes and counts keywords from US hospital websites.
Main output is a csv file for each hospital with word counts and contextual sentences

Author: hautahi
Date: 28 June 2017

Limitations:
Can only take text not images. So the "welcome" in http://www.abbgen.net/ cannot be read
Also, only the "Learn" in http://www.abbgen.net/ that is text that can be read. So it picks up 3
rather than 5

Bugs:

I think fixed:
1. The "invalid schema" error pops up with the : after the .com. This is repeatable (abingtonhealth)
2. requests.exceptions.ConnectionError for webpage http://www.keepingyouwell.com/FindaDoctor.aspx

Still to be fixed:
1. The handshake failure error. Looks to only happen sometimes. Need to figure out how to use exceptions to get around it
2. Connection error Errno 11004
3. When scraping, I think it excludes some tags. Like image descriptions and maybe stuff in the head.

'''

#-------------------------------------------------------------#
# 1.  Setup
#-------------------------------------------------------------#

print "Code is Working..."

import pandas as pd
from bs4 import BeautifulSoup
import urlparse
import time
import csv
import unicodedata
import requests
#from time import sleep
#from random import uniform
import sys

#-------------------------------------------------------------#
# 2. Define Functions
#-------------------------------------------------------------#

def make_soup(url):
    '''
    Function creates a soup object from url string
    '''    
    
   #sleep(uniform(0,1))    
    try:
        response = requests.get(url, timeout=5)
        html, stat = response.text, response.status_code
    except requests.exceptions.HTTPError:
        html, stat = "", 0
    except requests.exceptions.Timeout:
        html, stat = "", 1
    except requests.exceptions.ConnectionError:
        html, stat = "", 2
    except requests.exceptions.RequestException:
        html, stat = "", 3
    # Probably need to add more errors in here
        
    print("Status Code: %s" % stat)
    return BeautifulSoup(html, "lxml"), stat

def process(url):
    '''
    Function retrieves all links from a webpage excluding external links
    ''' 
    soup, stat = make_soup(url)
    
    # Get all links on page
    links = [urlparse.urljoin(url,tag['href']) for tag in soup.findAll('a', href=True)]
    
    # Remove bookmark section from urls
    links1 = [x.split("#")[0] for x in links]    
    
    # Remove duplicates
    links1 = list(set(links1))
    
    # Remove outside links that don't start with url
    links = [s for s in links1 if s.startswith(url) == True]
      
    return links, stat

def get_pages(url):
    '''
    Function retrieves all links from a webpage and its subpages
    excluding external links
    '''     
    
    # Get links on main page
    links1, stat1 = process(url)

    # Get links on each subpage
    links2, STATS = [], []
    
    for i in links1:
        print(i)
        x, stat = process(i)
        
        links2 += x
        STATS += [stat]
    links = links2 + links1
    
    # Save urls and status codes to csv
    STATS = [stat1] + STATS
    LINKS = [url] + links1
    d1 = pd.DataFrame(LINKS,columns=['url'])
    d2 = pd.DataFrame(STATS,columns=['status code'])
    d = pd.concat([d1, d2], axis=1, join_axes=[d1.index])
    
    # Remove duplicates
    links = list(set(links))

    return links, d

def get_index(text, a):
    '''
    Function returns the index places of "a" in the string "text"
    '''   
    return [i for i,x in enumerate(text.split()) if x==a]
    
def get_sentences(text,term,n):
    '''
    Function returns a list of sentences of "n" words around the "term"
    in the "text" string
    '''
    ind = get_index(text,term)
    sentence_list = [text.split()[max(0,i-n):i+n] for i in ind]
    sentences = [' '.join(x) for x in sentence_list]
    
    # Remove unicode
    sentences1 = [unicodedata.normalize('NFKD',x).encode('ascii','ignore') for x in sentences]
    return sentences1

def count_keys(links,key,n):
    '''
    Function counts the number of occurences of keywords on each page in links,
    returns the relevant sentences, and the status code of the page request
    '''
    Totalcount, Totalsent = [], []
    
    for l in links:

        print(l)
        soup, stat = make_soup(l)
        
        COUNT, SENT = [l,stat], []
        for word in key:
            
            # Get text
            text = soup.get_text()
            
            # Get word count
            ind = get_index(text,word)
            count = len(ind)
            COUNT.append(count)
            
            # Get sentences
            sentences = get_sentences(text,word,n)
            SENT.append(sentences)            
            
        Totalcount.append(COUNT)
        Totalsent.append(SENT)
    
    # Save counts to a dataframe
    headers = ['url','status code'] + key
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
    links, stats = get_pages(url)
    dlinks = pd.DataFrame(links,columns=["sub_pages"])
    dlinks.insert(0,'hospital',name)
    dlinks.insert(1,'hospital_website',url)
    dlinks.to_csv('./output/'+name+'_subpagelinks.csv',index=False, encoding='utf-8')
    
    # Count keywords in subpages
    print('Counting keywords...')
    #links = links[0:20]  
    d = count_keys(links,key,n)
    d.insert(0,'hospital',name)
    d.insert(1,'hospital_website',url)
    d.to_csv('./output/'+name+'.csv',index=False, encoding='utf-8')
    
    print("--- %s seconds ---" % (time.time() - start_time))

#-------------------------------------------------------------#
# 3. Main function
#-------------------------------------------------------------#

def main():
    """
    Function main() expects arguments via terminal entry.
    
    The inputs should be:
    input_data,keywords,sentence_length,start_index,end_index
    """

    # The first element of args is the function name.
    args = sys.argv[1:]
    
    # Check to make sure the proper number of arguments exist.
    if not args or len(args) < 5:
        print('usage: input_file keyword_file sentence_length start_index end_index')
        sys.exit(1)
    d_name, key_name = args[0], args[1]
    n, s1, s2 = int(args[2]),int(args[3]),int(args[4])
    
    # Get the main input file
    print('Now reading the main input file...')
    d = pd.read_csv(d_name)
    d.columns = map(str.lower, d.columns)
    df = d[s1:s2]
    
    # Get the keyword file
    print('Reading keyword files...')
    with open(key_name, 'rb') as f:
        reader = csv.reader(f)
        key_list = list(reader)
    keywords = [val for sublist in key_list for val in sublist]
    
    # Initialize model.
    print('Start Scraping...')
    
    # Loop over hospitals
    for url, name in zip(df["website"], df["hospital name"]):
        print('Processing hospital: '+name)
        main_function(url,keywords,name,n)

if __name__ == '__main__':
    main()

#-------------------------------------------------------------#
# 4. Manual Analysis
#-------------------------------------------------------------#

# Load data
#d = pd.read_csv("./data/SIE-IMPAQ-URL-05252017.csv")
#d.columns = map(str.lower, d.columns)
#df = d[34:40]
#
## Load keywords
#with open('./data/keywords.csv', 'rb') as f:
#    reader = csv.reader(f)
#    key_list = list(reader)
#keywords = [val for sublist in key_list for val in sublist]
#
## Parameters
#n = 10
#
## Loop over this    
#for url, name in zip(df["website"], df["hospital name"]):
#    print('Processing hospital: '+name)
#    main_function(url,keywords,name,n)
