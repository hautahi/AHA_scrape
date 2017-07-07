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
import OpenSSL
#from time import sleep
#from random import uniform

#-------------------------------------------------------------#
# 2. Define Functions
#-------------------------------------------------------------#

def make_soup(url):
    '''
    Function creates a soup object from url string. It also returns the url, 
    which might have been redirected, and the status code of the request.
    '''
    
    #sleep(uniform(0,1))
    # Set user agent for request    
    h = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}
    
    # If there is a redirect, check to see if it's a big one, then re-assign the url
    try:
        response = requests.get(url, timeout=5,headers=h,verify=True)
        if response.url.startswith(url)==False:
            url_re = response.url
        else:
            url_re = url
        html, stat = response.text, response.status_code
    except requests.exceptions.HTTPError:
        html, stat, url_re = "", 0, url
    except requests.exceptions.Timeout:
        html, stat, url_re = "", 1, url
    except requests.exceptions.ConnectionError:
        html, stat, url_re = "", 2, url
    except requests.exceptions.RequestException:
        html, stat, url_re = "", 3, url
    except OpenSSL.SSL.Error:
        html, stat, url_re = "", 4, url
        
    #print("Status Code: %s" % stat)
    return BeautifulSoup(html, "lxml"), stat, url_re

def process(url):
    '''
    Function retrieves all links from a webpage excluding external links
    ''' 
    soup, stat, url_redirect = make_soup(url)
    
    # Get all links on page. 'urljoin' creates absolute links from relative
    # ones for those that don't start with http://
    links = [urlparse.urljoin(url_redirect,tag['href']) for tag in soup.findAll('a', href=True)]
    links = [url_redirect] + links
    
    # Remove bookmark section from urls
    links1 = [x.split("#")[0] for x in links]    
    
    # Remove duplicates
    links1 = list(set(links1))
    
    # Remove pdf links
    links_pdf = [s for s in links if s.endswith("pdf") != True]
    
    return links_pdf, stat, url_redirect

def get_pages(url):
    '''
    Function retrieves all links from a webpage and its subpages
    excluding external links
    '''     
    
    # Get links on main page
    links1, s, url_redirect = process(url)
    if url_redirect.startswith(url)==False or url.startswith(url_redirect)==False:
        print "Request was redirected"
        print "From:", url
        print "To:", url_redirect
        
    # Remove outside links that don't start with url
    links = [x for x in links1 if x.startswith(url_redirect) == True]

    # Get links on each subpage
    links1 = []   
    for i in links:
        #print(i)
        x, s, r = process(i)        
        links1 += x

    links1 = links + links1

    # Remove duplicates
    links1 = list(set(links1))
    
    # Remove outside links that don't start with url
    links = [x for x in links1 if x.startswith(url_redirect) == True]

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
        soup, stat, url_redirect = make_soup(l)
        
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
        
        # Get subpage content and count keywords
        print('Retrieving content and counting keywords...')
        time1 = time.time()
        #links = links[0:20]  
        d, w = count_keys(links,keywords,n)
        print("Retrieving content and counting keywords took %s seconds" % (time.time() - time1))
        
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
