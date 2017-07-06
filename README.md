# AHA_scrape

This repository contains web scraping code that visits hospital websites, extracts their subpages, downloads and saves their content, and searches for keywords.

- `scrape.py` is the main scraping code
It can be run from the terminal using the following command:
`python scrape.py input_data keywords index_start index_end [sentence_length]`

where each of the inputs are as follows:


- `input` contains the two input data files
	- `hospital_list.csv`
	- `keywords.csv'

- `output` folder contains the resulting keyword search data. For each hospital, there are two output csv files. One contains the keyword counts. The other contains the full downloaded text from each subpage.
