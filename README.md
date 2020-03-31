# covid19-bz-scraper

## process_municipalities_singleday.py

Script to pull municipal data for positive tested COVID-19 cases for province of South Tyrol from excel file
and write/append to csv

### Usage:
    python process_municipalities_singleday.py [URL]
### Parameters:
URL (string): URL to xls sheet containing municipal covid-19 data for South Tyrol 
e.g. http://www.provinz.bz.it/news/de/news.asp?news_action=300&news_image_id=1062388
### Output:
creates new .csv file for specific day and appends data to (existing) .csv file containing previous days

