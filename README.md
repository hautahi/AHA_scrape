# AHA_scrape

This repository contains web scraping code that visits hospital websites, extracts their subpages, downloads and saves their content, and searches for keywords. It uses the `Scrapy` framework.

- `AHAscrapy` contains the code for the scrapy spider.

- `main_scrape.py` is the script used to call the spider. It can be run from the terminal using the following command:
		
	`python main_scrape.py index_start index_end`

	where the `index_start` and `index_end` are integers used to slice the input data. For example, `index_start = 40` and `index_end = 50` scrapes the websites for those hospitals between 40 and 50 in `hospital_list.csv`.

- `AHAscrapy/spiders/main.py` defines the spider 

- `input` contains the two input data files
	- `hospital_list.csv`
	- `keywords.csv`

- `output` folder contains the resulting keyword search data. For each hospital, there are two output .csv files. One contains the keyword counts. The other contains the full downloaded text from each subpage.
