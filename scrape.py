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

To do:
1. Save soup or text objects in folders

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
import sys
#from time import sleep
#from random import uniform

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
    # Might need to add more errors in here
        
    #print("Status Code: %s" % stat)
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
    links, s = process(url)

    # Get links on each subpage
    links2 = []   
    for i in links:
        #print(i)
        x, s = process(i)        
        links2 += x

    links = links2 + links

    # Remove duplicates
    links = list(set(links))

    return links

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
    Webcontent = []
    
    for l in links:
        
        # Fetch website
        #print(l)
        soup, stat = make_soup(l)
        
        # Save website content
        Webcontent.append([l,stat,[soup.get_text(separator=" ", strip=True)]]) 
        
        # Get word counts and sentences
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
    
    # Remove text of last keyword
    del Sdf['text-'+key[-1]]
    
    # Combine dataframes
    comb = pd.concat([d, Sdf], axis=1, join_axes=[d.index])
    
    return comb, Webcontent

#-------------------------------------------------------------#
# 3. Main function
#-------------------------------------------------------------#

def main():
    """
    Function main() expects arguments via terminal entry. Enter the following:
    
    python scrape.py input_data,keywords,start_index,end_index,sentence_length
    
    Definitions of inputs are as follows:
    input_data: csv file with two variables ("hospital name" and "website")
    keywords: csv file with list of keywords (the last word will not have
    the printed content so best to use a test case such as "the")
    start_index/end_index: program slices the input data between these integers    
    sentence_length: number of words on each side of a keyword for context
    (This is optional, default is 16).    
    """

    # The first element of args is the function name.
    args = sys.argv[1:]
    
    # Check to make sure the proper number of arguments exist.
    if not args or len(args) < 4:
        print('usage: input_file keyword_file start_index end_index sentence_length(optional)')
        sys.exit(1)
    
    # Assign parameters
    d_name, key_name = args[0:2]
    s1, s2 = [int(x) for x in args[2:4]]
    
    # Optional sentence length parameter
    if len(args) == 5:
        n = int(args[4])
    else:
        n = 16
    
    # Read the main input file
    print('Now reading the main input file...')
    d = pd.read_csv(d_name)
    d.columns = map(str.lower, d.columns)
    df = d[s1:s2]
    
    # Read the keyword file
    print('Reading keyword files...')
    with open(key_name, 'rb') as f:
        reader = csv.reader(f)
        key_list = list(reader)
    keywords = [val for sublist in key_list for val in sublist]
    
    # Loop over hospitals
    print('Start Scraping...')
    
    for url, name in zip(df["website"], df["hospital name"]):
        
        print('Processing hospital: '+name)
        
        start_time = time.time() 
    
        # Get all subpage links
        print('Retrieving Links...')
        links = get_pages(url)
        print("Retrieving links took %s seconds" % (time.time() - start_time))
        time1 = time.time()
        
        # Get subpage content and count keywords
        print('Counting keywords...')
        #links = links[0:20]  
        d, w = count_keys(links,keywords,n)
        print("Counting keywords took %s seconds" % (time.time() - time1))
        
        # Save keyword counts
        d.insert(0,'hospital',name)
        d.insert(1,'hospital_website',url)
        d.to_csv('./output/'+name+'.csv',index=False, encoding='utf-8')
        
        # Save content from each page (using manual write for more efficiency)
        wd = pd.DataFrame(w,columns=["url","status",'content'])
        wd.insert(0,'hospital',name)
        wd.insert(1,'hospital_website',url)
        wd.to_csv('./output/'+name+'_webcontent.csv',index=False, encoding='utf-8')
        
        print("--- %s seconds ---" % (time.time() - start_time))

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
