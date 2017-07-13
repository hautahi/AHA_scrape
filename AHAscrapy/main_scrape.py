
print "Code is Working..."

import subprocess
import os
import pandas as pd
from urlparse import urlparse
import requests
import sys
import OpenSSL
import time
import sys

#-------------------------------------------------------------#
# 2. Define Functions
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
    d_name = "../input/hospital_list.csv"
    print('Now reading the main input file...')
    d = pd.read_csv(d_name)
    d.columns = map(str.lower, d.columns)
    df = d[s1:s2]
    print("")

    # Define user agent
    h = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}

    # Loop over hospitals
    i = s1
    for url, name in zip(df["website"], df["hospital name"]):

        print('Processing hospital: ' +name+ ', index = %s' %i)
        
        start_time = time.time()
                            
        # Check if there's a redirect
        try:
            response = requests.get(url, timeout=5,headers=h,verify=True)
            if response.url.startswith(url)==False:
                        url_new = response.url
                        print("Request was redirected from: "+url)
                            #print("From: "+url)
                        print("To: "+url_new)
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

        # Create the allowed_domain url 
        parsed_url = urlparse(url_new).netloc
        short_url = "al="+parsed_url
        print("Allowed domain: " + parsed_url)

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
        retcode = subprocess.call(["scrapy", "crawl", "AHAscrape", "-a", full,"-a",short_url,"-o",fname,"-t","csv"],stdout=FNULL,stderr=subprocess.STDOUT)

        print("--- %s seconds ---" % (time.time() - start_time))
        i += 1
       # subprocess.call(["scrapy", "crawl", "AHAscrape", "-a", full,"-a",short_url,"-o",fname,"-t","csv"])

if __name__ == '__main__':
    main()
