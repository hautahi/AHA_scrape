
print "Code is Working..."

import subprocess
import os
import pandas as pd

#-------------------------------------------------------------#
# 2. Define Functions
#-------------------------------------------------------------#

s1, s2 = 0, 2

d_name = "../input/hospital_list.csv"

# Read the main input file
print('Now reading the main input file...')
d = pd.read_csv(d_name)
d.columns = map(str.lower, d.columns)
df = d[s1:s2]

for url, name in zip(df["website"], df["hospital name"]):
    full = "url="+url
    print("Scraping: " + url)
    fname = "../output/scrapy_content/"+name+".csv"

	# Remove old file if it exists because scrapy automatically appends
    try:
        os.remove(fname)
    except OSError:
        pass
	
	# call scrapy and suppress output
    FNULL = open(os.devnull,'w')
    retcode = subprocess.call(["scrapy", "crawl", "AHAscrape", "-a", full,"-o",fname,"-t","csv"],stdout=FNULL,stderr=subprocess.STDOUT)
    print("Saving under: " + fname)

