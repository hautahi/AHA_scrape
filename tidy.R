# This program was used to take the files scraped with the old non-scrapy method,
# remove the word counts, tidy the html content and save in the new format.

library(dplyr)
library(readr)

# -----------------
# Define Functions
# -----------------

# Get filenames
files <- list.files(path="./output/originals", pattern="*.csv", full.names=T, recursive=FALSE)

for (f in files) {
  print(f)
  
  # Read file and simplify the html content
  d <- read_csv(f,col_types = cols()) %>% select(content,url) %>%
    mutate(content = gsub('^.|.$', '', content),
           content=gsub("[\r\n]", "", content),
           content=gsub("\\{.*?\\}","",content),
           content=gsub("\\[|\\]","",content),
           content=gsub("<.*?>", "", content))
  
  # Save in new folder
  new_f <- gsub("_webcontent.csv",".csv",f)
  new_f <- gsub("/originals/","/original_content/",new_f)
  write_csv(d,new_f)
}

# -----------------
# Create dataframe with unique hospital names
# -----------------

# First rename original list to "hospital_list_original"

# Load original
d <- read_csv("input/hospital_list_original.csv")

# Create Unambiguous Names
d <- d %>% mutate(name=paste(`Hospital Name`,City,State))

# There are still a couple duplicate names
length(unique(d$name))

# Rename the duplicates
d <- d %>% mutate(dup=duplicated(name),name=ifelse(dup==TRUE,paste(name,2),name))

# Save this dataset
d %>% select(-dup) %>%
  write.csv("./input/hospital_list_unique.csv",row.names = F)

# -----------------
# Rename already scraped files with new unique name
# -----------------

d <- read_csv("input/hospital_list_unique.csv")

# Get the  files
path="./output/content_depth3"
files <- list.files(path=path, pattern="*.csv", full.names=T, recursive=FALSE)

for (f in files) {
  print(f)
  hname <- gsub(paste0(path,"/"),"",f)
  hname <- trimws(gsub(".csv","",hname),"r")
  
  odie <- d %>% filter(`Hospital Name`==hname)
  if (nrow(odie)>0) {
    print("changing")
    new_name <- trimws(odie$name[1],"r")
    
    # Rename file
    file.rename(f,paste0(path,"/",new_name,".csv"))
  }

}

# -----------------
# Remove duplicate websites and save new input list
# -----------------

d <- read_csv("input/hospital_list_unique.csv")

# All names should be unique
length(unique(d$name))

# There are still many duplicate hospital websites
length(unique(d$Website))

# Remove duplicated websites
d <- d %>% distinct(Website, .keep_all = TRUE) 

# Check that all the unique names remain unique
length(unique(d$name))

# Rename hospital name and save as new input csv
d %>% mutate(`Hospital Name`=name) %>% select(-name) %>%
  write.csv("input/hospital_list.csv",row.names=F)
  
