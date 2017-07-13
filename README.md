# AHA_scrape

This repository contains web scraping code that visits hospital websites, extracts their subpages, downloads and saves their content, and searches for keywords. There are two different approaches.

1. `Requests` + `Beautiful Soup`
2. `Scrapy`

## 1. `Requests` + `Beautiful Soup`

- `scrape.py` is the main scraping code. It can be run from the terminal using the following command:

	`python scrape.py input/hospital_list.csv input/keywords.csv index_start index_end [sentence_length]`

	where the index_start and index_end inputs are integers used to slice the input data. For example, index_start = 40 and index_end = 50 scrapes the websites for those hospitals between 40 and 50 in `hospital.csv`. `sentence_length` is an optional integer that determines the number of words to extract from either side of a keyword that is useful for providing context. The defualt value is 16.


- `input` contains the two input data files
	- `hospital_list.csv`
	- `keywords.csv`

- `output` folder contains the resulting keyword search data. For each hospital, there are two output .csv files. One contains the keyword counts. The other contains the full downloaded text from each subpage.

## 2. `Scrapy`

- `AHAscrapy` contains the code for the scrapy spider.

- `main_scrape.py` is the script used to call the spider. It can be run from the terminal using the following command:
		
	`python main_scrape.py index_start index_end`

	where the `index_start` and `index_end` are integers used to slice the input data. For example, `index_start = 40` and `index_end = 50` scrapes the websites for those hospitals between 40 and 50 in `hospital_list.csv`.

- `AHAscrapy/spiders/main.py` defines the spider 
