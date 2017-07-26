# This program counts the number of subpages for each hospital webscrape.

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
library(readr)

# -----------------
# Define Functions
# -----------------

# Parameters
pathname = "./output/content_depth1/"
outname = "pagecounts_depth1.csv"

# Import filenames
files <- list.files(path=pathname, pattern="*.csv", full.names=T, recursive=FALSE)

# Limit to files with size>0
info = file.info(files) %>% arrange(-size)
info = info[order(info$size),]
files1 = rownames(info[info$size != 0, ])
stop_index = length(files1)
print(length(files1))

# Loop over files
dat <- NULL
start_time <- proc.time()
i <- start_index
for (f in files1[start_index:stop_index]) {
  
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