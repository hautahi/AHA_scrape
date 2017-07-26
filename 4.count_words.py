'''
This program takes long html strings from text files as inputs.
It counts keywords and stores the counts in csv file

Usage: python count_words.py start stop input_folder outname
start: integer index for start of slice in files
stop: integer index for end of slice in files
input_folder: path to input files
outname: name of output csv file

author: hautahi
date: July 17 2017
'''

#-------------------------------------------------------------#
# 1.  Setup
#-------------------------------------------------------------#

print "Code is Working..."

import pandas as pd
import os
import csv
import re
import sys
import time
import io

#-------------------------------------------------------------#
# 2. Define functions
#-------------------------------------------------------------#

def count_keys(files,key,start,stop,input_folder):
    '''
    Function counts the number of occurences of keywords in each file contained
    in "files". It also returns the relevant sentences. Returns a dataframe with
    a row per webpage.
    '''

    Totalcount = []
    for count, f in enumerate(files[start:stop]):

        if (count % 100 == 0):
            print("file number: %s" %count)

        try:
            
            # Fetch file            
            txt = io.open(input_folder+f,"r", encoding='utf8', errors='ignore')
            df = []
            for line in txt:
                df.append(line.strip("\n").lower())
            txt.close()
        
            # Get word counts
            COUNT = []
            for line in df:
                
                COUNT.append([line.count(word) for word in key])

            # Gather stats for this file
            Totalcount.append([re.sub('\.text$', '', f)] + [sum(i) for i in zip(*COUNT)]) 
            
        # Deal with empty csv files
        except pd.io.common.EmptyDataError:
            Totalcount.append([re.sub('\.text$', '', f)] + ["" for x in key]) 
            continue
    
    # Throw into dataframe
    d = pd.DataFrame(Totalcount,columns=['name'] + key)  
    
    return d
    
def main():
    
    start_time = time.time()    
    
    # The first element of args is the function name.
    args = sys.argv[1:]
    
    # Check to make sure the proper number of arguments exist.
    if not args or len(args) < 4:
        print('usage: python count_words.py start_index end_index input_folder outname')
        sys.exit(1)
    
    # Assign parameters
    start, stop = [int(x) for x in args[0:2]]
    input_folder, outname = args[2:4]
    
    # Load keywords    
    with open("./input/keywords.csv", 'rb') as f:
        key_list = list(csv.reader(f))
    key = [val for sublist in key_list for val in sublist]   

    # Load content
    files = os.listdir(input_folder) 
    
    # Create counts and export to csv    
    df = count_keys(files,key,start,stop,input_folder)
    df.to_csv(outname,index=False)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
if __name__ == '__main__':
    main()
