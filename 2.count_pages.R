# This program counts the number of subpages for each hospital webscrape.
# Usage: Rscript count_pages.R pathname outname start stop
# pathname: path to input file directory
# outname: name of output csv file
# start: integer index for start of slice in files
# stop: integer index for end of slice in files. If user wants to do the whole set,
#	then enter a negative number

# author: hautahi
# date: July 26 2017

# -----------------
# Setup
# -----------------

# Read parameter inputs from terminal
args <- commandArgs(TRUE)
pathname = args[1]
outname = args[2]
start_index = as.numeric(args[3])

# Load packages
library(readr)
library(dplyr)

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
dat <- NULL
start_time <- proc.time()
i <- start_index
for (f in files[start_index:stop_index]) {
  
  # Print every 100th iteration
  if(i %% 100==0) {
    cat(paste0("file number: ", i, "\n"))
  }
  
  # Read file
  pagenumber <- nrow(read_csv(f,col_types = cols()))
  
  # Save pagecounts into list
  name <- gsub(".csv","",f)
  name <- gsub(pathname,"",name)
  temp = c(name,pagenumber)  
  dat <- rbind(dat,temp)
  
  i=i+1
}
print(proc.time() - start_time)

# Save pagecounts
df <- as.data.frame(dat)
colnames(df) <- c("name","page count")
df = df[order(df$name),]
write_csv(df,outname)
