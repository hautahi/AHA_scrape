# This program merges the original hospital list file
# with the page counts and the word counts csv files
# Usage: Rscript merge.R mainfile pagecountfile wordcounfile finalfile
# mainfile: hospital list

# author: hautahi
# date: July 17 2017

# red inputs from 
args <- commandArgs(TRUE)
mainfile = args[1]
pagecountfile = args[2]
wordcountfile = args[3]
finalfile = args[4]

# Load packages
library(dplyr)
library(readr)

# Import filenames

d = read_csv(mainfile) %>% select(name=`Hospital Name`,website=Website)
page = read_csv(pagecountfile)
word = read_csv(wordcountfile)

# Merge and save
d <- left_join(d,page,by="name") %>% left_join(word,by="name")
d[is.na(d)] <- 0
write_csv(d,finalfile)
