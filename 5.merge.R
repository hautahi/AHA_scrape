# This program merges the original hospital list file
# with the page counts and the word counts csv files

# Load packages
library(dplyr)
library(readr)

# Parameters
mainfile = "./input/hospital_list.csv"
pagecountfile = "pagecounts_depth1.csv"
wordcountfile = "wordcounts_depth1.csv"
finalfile = "final_depth1.csv"

# Import filenames
d = read_csv(mainfile) %>% select(name=`Hospital Name`,website=Website)
page = read_csv(pagecountfile)
word = read_csv(wordcountfile)

# Merge and save
d <- left_join(d,page,by="name") %>% left_join(word,by="name")
d[is.na(d)] <- 0
write_csv(d,finalfile)