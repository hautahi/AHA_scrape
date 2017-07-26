# This program takes the old scraped files and tranforms into smaller html
# text files to be processed and counted by the python code

# -----------------
# Setup
# -----------------

# Read inputs from terminal
args <- commandArgs(TRUE)
if (length(args)<1) {
  start_index = 1
} else {
  start_index = as.numeric(args[1])
}

# Load packages
library(dplyr)
library(readr)
library(stringr)
library(data.table)

# -----------------
# Define Functions
# -----------------

# Parameters
pathname = "./output/content_depth3/"
# keypath = "./input/keywords.csv"
textpathname = "./output/htmltext_depth3/"
# outname = "pagecounts_depth3.csv"

# Import filenames
files <- list.files(path=pathname, pattern="*.csv", full.names=T, recursive=FALSE)

# Limit to files with size>0
info = file.info(files)
info = info[order(info$size),]
files1 = rownames(info[info$size != 0, ])
stop_index = length(files1)

# Import keywords
#keywords <- read_csv(keypath,col_names = FALSE) %>% as.vector()
#key <- keywords[[1]]
#key <- key[1:length(key)-1]

# Loop over files
#dat <- NULL
start_time <- proc.time()
i=start_index
for (f in files1[start_index:stop_index]) {
  
  # Read file
  # print(f)
  # print(i)
  # Print every 100th iteration
  if(i %% 100==0) {
    cat(paste0("file number: ", i, "\n"))
  }
#   x=list()
#   x[[1]] <- read_csv(f,col_types = cols()) %>% select(content) %>%
# 	  apply( 1, paste, collapse="") %>% paste(collapse=" ")

  name <- gsub(".csv","",f)
  name <- gsub(pathname,"",name)
  read_csv(f,col_types = cols()) %>% select(content) %>%
    apply( 1, paste, collapse="") %>% paste(collapse=" ") %>%
    list() %>%
    #fwrite(paste(textpathname, name,".text",sep=""),verbose=FALSE,buffMB = 1L,nThread=1)
    fwrite(paste(textpathname, name,".text",sep=""),verbose=FALSE,buffMB = 8L)
  
  #pagenumber <- nrow(d)
  
  # Create text
  
  # Count keywords
 #temp_count <- c()
 #for (w in key) {

  # count = str_count(d,w)
  # temp_count <- c(temp_count,count)

 #}
  
  # Save page and word counts into list
  # name <- gsub(".csv","",f)
  # name <- gsub(pathname,"",name)
  #temp = c(name,pagenumber,temp_count)  
  #temp = c(name,pagenumber)  
  #temp = c(name)  
  #dat <- rbind(dat,temp)
  
  # Save html text to file
  #x=list()
  #x[[1]]=d
  #fwrite(x,paste(textpathname, name,".text",sep=""),verbose=FALSE,buffMB = 1L,nThread=1)
  
  i=i+1

}

print(proc.time() - start_time)

# Save pagecounts
#df <- as.data.frame(dat)
#colnames(df) <- c("name","page count",key)
#colnames(df) <- c("name","page count")
#df = df[order(df$name),]
#write_csv(df,outname)

# ----------------------------------------------- #
# Archived COde (maybe of some use later)
# ----------------------------------------------- #

# Define sentence search function
# get_sentence <- function(str,keyword,lookaround) {
#   pattern <- paste0("([[:alpha:]]+ ){0,", lookaround, "}", keyword,
#                     "( [[:alpha:]]+){0,", lookaround, "}")
#   
#   return(regmatches(str, gregexpr(pattern, str)))
# }

# Use NLP to count and search
# library(NLP)
# y=strsplit(x,split=" ")
# strcount
# which(y[[1]] %in% "teamwork")

# Apply function "han" to files 1 instead of looping.
# hey <- lapply(files1,han)
# ho = data.frame(matrix(unlist(hey), nrow=length(hey), byrow=T))

# Save html files in different ways
# Save text 1
# write(d, file = paste("test1",name,".text",sep=""),append = FALSE, sep = " ")

# Save text 2
# start_time <- proc.time()
# file.create(paste("test3",name,".text",sep=""))
# fileConn <- file(paste("test3",name,".text",sep=""))
# writeLines(d, fileConn)
# close(fileConn)
# print(proc.time() - start_time)
