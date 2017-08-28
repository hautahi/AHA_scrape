# AHA_scrape

This repository contains web scraping code that visits hospital websites, extracts their subpages, downloads and saves their content, and searches for keywords. It uses the `Scrapy` framework.

- `AHAscrapy` contains the code for the scrapy spider.

	- `main_scrape.py` is the script used to call the spider. It can be run from the terminal using the following command:
		
	`python main_scrape.py index_start index_end`

	where the `index_start` and `index_end` are integers used to slice the input data. For example, `index_start = 40` and `index_end = 50` scrapes the websites for those hospitals between 40 and 50 in `hospital_list.csv`.

	- `AHAscrapy/spiders/main.py` defines the spider 

- `input` contains the two input data files (the other files are the old versions that had duplicate names and url's).
	- `hospital_list.csv`
	- `keywords.csv`

- `output` folder contains the resulting scraped data. `content_depthx` contains the scraped data from a `depth=x` scrape. There is a csv file for each hospital containing the html text for each subpage of that hospital. `htmltext_depthx` contains one text file for each hospital with all the text.
