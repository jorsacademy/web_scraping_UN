import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import csv
%run functions/functions.ipynb
# Defining the root and extension of the project browsing page in UN website
root_browse = 'https://sdgs.un.org/partnerships/'
ext_browse = 'browse'

# Assigning the number of pages to be itirated through in page_count variable
page_count = range(0,448)   

extensions = []
browse_url = 'https://sdgs.un.org/partnerships/browse?page='

for page in to_five:
    extension = get_links(browse_url, str(page))
    extensions.extend(extension)

extensions

root = 'https://sdgs.un.org'
header = ['Project', 'Description', 'StartDate', 'EndDate', 'Partners', 'ContactName', 'ContactLink', 'SDG Codes', 'InfoLink']

# Writing only column names to the csv
with open('WebScraping.csv', 'w', newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
  
# Iterating through the projects and scraping the data in the given extensions  
for ext in extensions:
    html_con = get_html(root, ext)
    data = scrape_data(html_con)
    write_data(data)

