
'''
This program scrapes content from US hospital websites
Output is a csv file for each hospital with two columns
    - one gives the url of the subpage
    - the other gives the scraped html content

The program calls a scrapy spider to crawl the websites.
This should be placed and called from within the scrapy folder

Usage: python main_scrape.py index_start index_end

Author: hautahi
Date: 13 June 2017

To do:
When main page has subdomains and ends with a .aspx, this is being
included in the allowed subdomain. Need to remove this.
'''

#-------------------------------------------------------------#
# 1. Setup
#-------------------------------------------------------------#

print("Code is Working...")

import subprocess
import os
import pandas as pd
from urlparse import urlparse
import requests
import sys
import time

#-------------------------------------------------------------#
# 2. Define Function
#-------------------------------------------------------------#

def main():

    # First element of args is the function name
    args = sys.argv[1:]

    # Check to make sure the proper numbr of arguments exist
    if not args or len(args) < 2:
        print('usage: start_index end_index')
        sys.exit(1)

    # Assign parameters
    s1, s2 = [int(x) for x in args]

    # Read the main input file
    print('Now reading the main input file...')
    d_name = "../input/hospital_list.csv"
    d = pd.read_csv(d_name)
    d.columns = map(str.lower, d.columns)
    df = d[s1:s2]
    print("")

    # Define user agent
    h = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}

    # Loop over hospitals
    start_time1 = time.time()
    i = s1
    for url, name in zip(df["website"], df["hospital name"]):

        print('Processing hospital: ' +name+ ', index = %s' %i)
        print(time.ctime(time.time()))
        start_time = time.time()
                            
        # Check if there's a redirect
        try:
            response = requests.get(url, timeout=5,headers=h,verify=True)
            if response.url.startswith(url)==False:
                        url_new = response.url
                        print("Request was redirected from: "+url)
                        print("To: "+url_new)
            else:
                url_new = url
        except Exception:
            url_new=url

        # Create the allowed_domain url 
        parsed_url = urlparse(url_new).netloc
        parsed_url = parsed_url.replace("www.","")
        short_url = "al="+parsed_url
        print("Allowed domain: " + parsed_url)

        # Create subdomain allow
        parsed_suburl = urlparse(url_new).path
        sub_url = "allow_subdom="+parsed_suburl
        print("Allowed subdomain: " + parsed_suburl)

        # Remove old file if it exists because scrapy automatically appends
        fname = "../output/scrapy_content/"+name+".csv"
        try:
            os.remove(fname)
        except OSError:
            pass

        # Call scrapy and suppress output
        print("Scraping: " + url_new)
        full = "url="+url_new
        FNULL = open(os.devnull,'w')
        retcode = subprocess.call(["scrapy", "crawl", "AHAscrape", "-a", full,"-a",short_url,"-a",sub_url,"-o",fname,"-t","csv"],stdout=FNULL,stderr=subprocess.STDOUT)
        
        # Print duration and update loop variables
        print("--- %s seconds ---" % (time.time() - start_time))
        i += 1

    print("---Total Job: %s seconds ---" % (time.time() - start_time1))

if __name__ == '__main__':
    main()
