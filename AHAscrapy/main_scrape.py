
print "Code is Working..."

import subprocess
import os
import pandas as pd
from urlparse import urlparse
import requests
import sys
import OpenSSL

#-------------------------------------------------------------#
# 2. Define Functions
#-------------------------------------------------------------#

s1, s2 = 0, 4

d_name = "../input/hospital_list.csv"

# Read the main input file
print('Now reading the main input file...')
d = pd.read_csv(d_name)
d.columns = map(str.lower, d.columns)
df = d[s1:s2]

h = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}

for url, name in zip(df["website"], df["hospital name"]):

    print('Processing hospital: '+name)

	# Check if there's a redirect
    try:
        response = requests.get(url, timeout=5,headers=h,verify=True)
        if response.url.startswith(url)==False:
		    url_new = response.url
		    print("Request was redirected. From: "+url)
			#print("From: "+url)
			
            #print("To: "+url_new)
        else:
            url_new = url
    except requests.exceptions.HTTPError:
		url_new = url
    except requests.exceptions.Timeout:
		url_new = url
    except requests.exceptions.ConnectionError:
		url_new = url
    except requests.exceptions.RequestException:
		url_new = url
    except OpenSSL.SSL.Error:
		url_new = url

    full = "url="+url_new
    print("Scraping: " + url_new)
    fname = "../output/scrapy_content/"+name+".csv"
    
    parsed_url = urlparse(url_new).netloc
    print(parsed_url)
    short_url = "al="+parsed_url
    print(short_url)

	# Remove old file if it exists because scrapy automatically appends
    try:
        os.remove(fname)
    except OSError:
        pass

	# Call scrapy and suppress output
    FNULL = open(os.devnull,'w')
    retcode = subprocess.call(["scrapy", "crawl", "AHAscrape", "-a", full,"-a",short_url,"-o",fname,"-t","csv"],stdout=FNULL,stderr=subprocess.STDOUT)

   # subprocess.call(["scrapy", "crawl", "AHAscrape", "-a", full,"-a",short_url,"-o",fname,"-t","csv"])

