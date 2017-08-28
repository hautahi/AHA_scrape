'''
This program has a number of small and useful little sections
'''

#-------------------------------------------------------------#
# 1.  Setup
#-------------------------------------------------------------#

print "Code is Working..."

import pandas as pd
import os
import csv
import re
from operator import itemgetter
from itertools import groupby
import unicodedata
from bs4 import BeautifulSoup

#-------------------------------------------------------------#
# 2. Read and Process old files
#-------------------------------------------------------------#

'''
This section reads in data produced by the old scraping code
and processes it into the new format. Moved this to do in R though
because something weird happens when the csv files are read in.
Will try to read in some lines.
'''

# Read in list of scraped files
#files = os.listdir("./output/originals/")
#
#for f in files:
#    print(f)
#    # Load data
#    d = pd.read_csv("./output/originals/"+f,error_bad_lines=False,warn_bad_lines=False,
#                    quoting=csv.QUOTE_NONE,encoding='utf-8',usecols=['hospital','content'])
#    
#    content = []
#    content_list = d['content']
#    for x in content_list:
#        lines = (line.strip() for line in x.splitlines())
#        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#        text = ' '.join(chunk for chunk in chunks if chunk)
#        result=re.sub('{[^}]+}', '', text)
#        result= re.sub("ga([^))]+)","",result)
#        content.append(result[1:-1])
#        
#    # Select columns
#    df = d[['url']]
#    df['content'] = content
#
#    short_f = re.sub("_webcontent","",f)
#    df.to_csv("./output/original_content/"+short_f,index=False)

#-------------------------------------------------------------#
# 3. Find missing hospitals, general tidy
#-------------------------------------------------------------#

'''
This section helps to find out which files are missing from various folders
'''

def group_indices(d):
    ranges = []
    for key, group in groupby(enumerate(d), lambda (index, item): index - item):
        group = map(itemgetter(1), group)
        if len(group) > 1:
            ranges.append(xrange(group[0], group[-1]))
        else:
            ranges.append(group[0])
    
    return ranges

# Read main list
d = pd.read_csv("./input/hospital_list.csv")
d.columns = map(str.lower, d.columns)

# Read in list of newly scraped files
f = os.listdir("./output/scrapy_content/")
#scraped_files = [re.sub('.csv', '', x) for x in f]
scraped_files = [x[:-4] for x in f]
scraped_index = list(d[d['hospital name'].isin(scraped_files)].index)
scraped_range = group_indices(scraped_index)
print(scraped_range)

# Read in list of combined scraped files
f = os.listdir("./output/content_depth3/")
#scraped_files = [re.sub('.csv', '', x) for x in f]
scraped_files = [x[:-4] for x in f]
scraped_index = list(d[d['hospital name'].isin(scraped_files)].index)
scraped_range1 = group_indices(scraped_index)
print(scraped_range1)

# Read in list of old scraped files
f = os.listdir("./output/originals/")
scraped_files = [re.sub('_webcontent.csv', '', x) for x in f]
scraped_index = list(d[d['hospital name'].isin(scraped_files)].index)
scraped_range = group_indices(scraped_index)
print(scraped_range)

# Read in list of text files
f = os.listdir("./output/htmltext_depth3/")
scraped_files = [re.sub('.text', '', x) for x in f]
scraped_index = list(d[d['hospital name'].isin(scraped_files)].index)
scraped_range = group_indices(scraped_index)

# Read in list of scraped files from work comp
f = os.listdir("./output/scrapy_content_depth1/")
scraped_files = [re.sub('\.csv$', '', x) for x in f]
scraped_index = list(d[d['hospital name'].isin(scraped_files)].index)
scraped_range = group_indices(scraped_index)
print(scraped_range)

# Read in list of scraped files from mac
f = os.listdir("./output/scrapy_content_mac/")
scraped_files_mac = [re.sub('\.csv$', '', x) for x in f]
scraped_index_mac = list(d[d['hospital name'].isin(scraped_files_mac)].index)
scraped_range_mac = group_indices(scraped_index_mac)
print(scraped_range_mac)

# Find unscraped files
names = d['hospital name'].tolist()
toscrape = list(set(names)-set(scraped_files))

# Get indices of unscraped hospitals
odie = list(d[d['hospital name'].isin(toscrape)].index)

# import collections
# print [item for item, count in collections.Counter(names).items() if count > 1]

'''
To do:
1. Create a new column with hospital name and state
2. Change files to pull from "hospital name state column"
3. Rename all files to new state convention
'''

##-------------------------------------------------------------#
## 2. Create new column
##-------------------------------------------------------------#
#
#d = pd.read_csv("./input/hospital_list.csv")
#
## Drop duplicate websites
#df = d.drop_duplicates(subset="Website")
#
## Drop duplicate names
#df['Hospital Name State'] = df['Hospital Name']+" "+df["City"]+" " +df['State']
#web = d['Website'].tolist()
#web1 = list(set(web))
#
#import collections
#webdups =  [item for item, count in collections.Counter(web).items() if count > 1]
#dups = [x in web for x in web1]
#
#names = d['Hospital Name'].tolist()
#newnames = d['Hospital Name State'].tolist()
#
#names1 = list(set(names))
#newnames1 = list(set(newnames))
#
##-------------------------------------------------------------#
## 2. Combine Files
##-------------------------------------------------------------#
#
## Load keywords    
#with open("./input/keywords.csv", 'rb') as f:
#    reader = csv.reader(f)
#    key_list = list(reader)
#keywords = [val for sublist in key_list for val in sublist]    
#    
## Get list of files
#f_list = os.listdir("./output_combined")
#han = [x for x in f_list if "_" not in x]
#
## Combine files
#F = []
#for f in han:
#    d = pd.read_csv("./output_combined/"+f)
#    sums = [sum(d[k]) for k in keywords[0:-1]]
#    sums = [f[0:-4]] + sums
#    F.append(sums)
#df = pd.DataFrame(F,columns=['hospital'] + keywords[0:-1])
#
#df.to_csv("final.csv",index=False)
#
##-------------------------------------------------------------#
## 2. Count key_words
##-------------------------------------------------------------#
#
## Load keywords    
#with open("./input/keywords.csv", 'rb') as f:
#    reader = csv.reader(f)
#    key_list = list(reader)
#key = [val for sublist in key_list for val in sublist]   
#key = key[:-1]
