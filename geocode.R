# This program was used to take the files scraped with the old non-scrapy method,
# remove the word counts, tidy the html content and save in the new format.

library(dplyr)
library(readr)
library(ggmap)

# -----------------
# Read hospital data
# -----------------

# Load original
d <- read_csv("input/hospital_list.csv") %>%
  mutate(name=paste(`Hospital Name`,"USA"))

# -----------------
# First lot of geocoding
# -----------------

x = d$name[1:100]
loc <- geocode(x)

x1 <- d$name[101:300]
loc1 <- geocode(x1)

df <- data.frame(x,loc,y=(sample.int(101,size=length(x),replace=TRUE)-1))
df1 <- data.frame(x=x1,loc1,y=(sample.int(101,size=length(x1),replace=TRUE)-1))
df <- bind_rows(df,df1)

# Save geocoded list
merge_df <- df %>% select(name=x,lon,lat) %>%
  left_join(d,.,by="name") %>% select(-name) %>%
  write.csv("./input/hospital_list_geocoded.csv",row.names=F)

# -----------------
# Subsequent geocoding sessions
# -----------------

# Load partially geocoded data
d <- read_csv("input/hospital_list_geocoded.csv") %>%
  mutate(name=paste(`Hospital Name`,"USA"))

x <- d %>% filter(is.na(lon)) %>% select(name)
x <- x$name[1:2000]
loc <- geocode(x)

df <- data.frame(name=x,loc,y=(sample.int(101,size=length(x),replace=TRUE)-1))

# Save
odie <- df %>% select(name,lon,lat) %>%
  left_join(d,.,by="name") %>% select(-name) %>%
  mutate(lon=ifelse(is.na(lon.x)&!is.na(lon.y),lon.y,lon.x),
         lat=ifelse(is.na(lon.x)&!is.na(lon.y),lat.y,lat.x)) %>%
  select(-lon.x,-lat.x,-lon.y,-lat.y) %>%
  write.csv("./input/hospital_list_geocoded.csv",row.names=F)
