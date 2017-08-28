# This program was used to take the files scraped with the old non-scrapy method,
# remove the word counts, tidy the html content and save in the new format.

library(dplyr)
library(readr)
library(ggmap)
library(leaflet)

# -----------------
# Plot
# -----------------

# Load original data
o <- read_csv("input/hospital_list_original.csv") %>%
  mutate(name=`Hospital Name`,`Hospital Name`=paste(name,City,State)) %>%
  select(`Hospital Name`,name)
  
# Load geocoded data and put original names into geocoded data
d <- read_csv("input/hospital_list_geocoded.csv") %>%
  left_join(o)

# Load counts
counts <- read_csv("wordcounts_depth3.csv") %>%
  left_join(d,.,by="name")

# Plotting dataframe
df <- counts %>% filter(!is.na(lon),!is.na(lat),State!="HI",State!="AS",State!="AK",State!="GU",State!="PR",State!="MP",
                        !is.na(teamwork),teamwork>0)


# Plot
qpal <- colorBin("Reds", df$teamwork, bins=5)
m <- leaflet(data=df) %>%
  addTiles() %>%
  addCircleMarkers(~lon,~lat,radius=5,color = ~qpal(teamwork))%>%
  addLegend(values=~teamwork,pal=qpal,title="Number of Hits")
m

library(rgdal)
shp <- readOGR(dsn = "shapes", layer = "gz_2010_us_040_00_500k")

states <- spTransform(shp, CRS("+init=epsg:4326"))

pal <- colorBin("Reds", states$CENSUSAREA, bins = 5)

m <- leaflet(states) %>%
  addTiles()


