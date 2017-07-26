# This program simulates the DOL-ETA H-2A simple model

# -----------------
# Setup
# -----------------

library(dplyr); library(ggplot2)
library(RColorBrewer)
library(readr)
library(reshape2) # for melt()

colorchoice <- brewer.pal(3, "Pastel1")

inputdata = "final_depth3.csv"

# -----------------
# Define Functions
# -----------------

# Load data
d1 <- read_csv(inputdata) %>% select(-contains("text-")) %>% filter(!is.na(teamwork))

# Set plot theme
theme_set <-  theme_bw() + theme(legend.title=element_blank(),
                                  #axis.ticks.x=element_blank(),
                                  legend.position="bottom",
                                  #panel.grid.major = element_blank(),
                                  panel.grid.minor = element_blank(),
                                  #panel.border = element_blank(),
                                  axis.text.x = element_text(size=12),
                                  axis.text.y = element_text(size=12),
                                  strip.text.x = element_text(size=12),
                                  strip.text.y = element_text(size=12),
                                  strip.background = element_rect( fill="white",color="white"))

# Melt dataframe for plots
melt_df <- melt(d1) %>% select(-name)

# Plot histogram of counts
melt_df %>% filter(variable!="page count") %>%
ggplot(aes(x=value)) + geom_histogram(fill=colorchoice[2]) + facet_wrap(~variable ,ncol=2)+
  theme_set + xlab("Number of occurences in hospital website") +
  ylab("Count of Hospitals")
ggsave("./plots/count_hist.jpg")

# Plot histogram of counts > 0
melt_df %>% filter(variable!="page count",value>0,value<300) %>%
ggplot(aes(x=value)) + geom_histogram(fill=colorchoice[2],bins=200) + facet_wrap(~variable ,ncol=2) +
  theme_set + xlab("Number of occurences in hospital website") +
  ylab("Count of Hospitals") +ylim(c(0,400))
ggsave("./plots/positive_count_hist.jpg")

# Plot histogram of page counts > 0
melt_df %>% filter(variable=="page count",value<10000) %>%
  ggplot(aes(x=value)) + geom_histogram(fill=colorchoice[2],bins=100) + facet_wrap(~variable ,ncol=2) +
  theme_set + xlab("Number of pages in website") +
  ylab("Count of Hospitals")
ggsave("./plots/pagecount_hist.jpg")

# -----------------
# Extract some html
# -----------------

hosp_name <- "./output/scrapy_content/Clarke County Hospital.csv"
df <- read_csv(hosp_name)
x <- df['content'][[1]][1]
# write(x, file = "data.text",append = FALSE, sep = " ")
