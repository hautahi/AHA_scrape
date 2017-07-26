# This program takes the old scraped files and tranforms into smaller html
# text files to be processed and counted by the python code
# Usage: Rscript get_webtext.R pathname textpathname start stop
# pathname: path to input file directory
# textpathname: path to output file directory
# start: integer index for start of slice in files
# stop: integer index for end of slice in files. If user wants to do the whole set,
#	then enter a negative number

# author: hautahi
# date: July 26 2017

# -----------------
# Setup
# -----------------

# Read inputs from terminal
args <- commandArgs(TRUE)
pathname = args[1]
textpathname = args[2]
start_index = as.numeric(args[3])

# Load packages
library(dplyr)
library(readr)
library(stringr)
library(data.table)

# -----------------
# Define Functions
# -----------------

# Import filenames
files <- list.files(path=pathname, pattern="*.csv", full.names=T, recursive=FALSE)

# Limit to files with size>0
info = file.info(files)
info = info[order(info$size),]
files = rownames(info[info$size != 0, ])

# Get stop index from terminal
if (as.numeric(args[4])<0) {
  stop_index = length(files)
} else {
  stop_index = as.numeric(args[4])
}

# Loop over files
start_time <- proc.time()
i <- start_index
for (f in files[start_index:stop_index]) {
  
  # Print every 100th iteration
  if(i %% 100==0) {
    cat(paste0("file number: ", i, "\n"))
  }

  # Read and write files
  name <- gsub(".csv","",f)
  name <- gsub(pathname,"",name)
  read_csv(f,col_types = cols()) %>% select(content) %>%
    apply( 1, paste, collapse="") %>% paste(collapse=" ") %>%
    list() %>%
    fwrite(paste(textpathname, name,".text",sep=""),verbose=FALSE,buffMB = 8L)
  
  i=i+1

}

print(proc.time() - start_time)
