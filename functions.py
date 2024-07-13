import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import csv

# Method for retrieving all html content in a page
def get_html(root, extension):
    url = root + extension
    response = requests.get(url)
    html_content = response.text
    return html_content

def scrape_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Project
    box = soup.find(id="block-porto-content")
    if box is not None:
        inner_html = box.find('h1', class_ = 'separator-bottom mt-5')
        if inner_html is not None:
            project = inner_html.get_text(strip=True, separator=',')
        else:
            project = "NA"
    else:
        project = "NA"
        
    # Description
    box = soup.find('div', class_ = "clearfix text-formatted field field--name-field-description field--type-text-long field--label-above")
    if box is not None:
        description = box.find('div', class_ = 'field__item').get_text(strip=True)
    else:
        description = "NA"
        
    # Start Date
    box = soup.find('div', class_ = 'views-field views-field-field-start-date')
    if box is not None:
        inner_html = box.find(class_ = 'field-content')
        if inner_html is not None:
            start_date = inner_html.get_text(strip=True)[:-13]
        else:
            start_date = "NA"
    else:
        start_date = "NA"

    # End Date
    box = soup.find('div', class_ = 'views-field views-field-field-date-of-completion')
    if box is not None:
        inner_html = box.find(class_ = 'field-content')
        if inner_html is not None:
            end_date = inner_html.get_text(strip=True)[:-21]
        else:
            end_date = "NA"
    else:
        end_date = "NA"
        
    # Partners
    box = soup.find('div', class_ = "clearfix text-formatted field field--name-field-partners field--type-text-long field--label-above")
    if box is not None:
        partners = box.find('div', class_ = 'field__item').get_text(strip=True)
    else:
        partners = "NA"
        
    # Contact Info
    box = soup.find(id = "block-views-block-partnerships-contact-information-block-1")
    if box is not None:
        box_con_name = box.find('div', class_ = "views-field views-field-field-contact-name")
        if box_con_name is not None:
            contact_name = box_con_name.find('div', class_ = 'field-content').get_text(strip=True)
        else:
            contact_name = "NA"
        
        box_con_link = box.find('div', class_ = "views-field views-field-field-email")
        if box_con_link is not None:
            contact_link = box_con_link.find('div', class_ = 'field-content').get_text(strip=True)
        else:
            contact_link = "NA"
    else:
        contact_name = "NA"
        contact_link = "NA"
    
    # SDG Codes
    if soup.find(id="block-views-block-good-practices-block-7") is not None:
        sdg_list = soup.find(id="block-views-block-good-practices-block-7").get_text(strip=True, separator=',')[5:]
    else:
        sdg_list = "NA"
    
    # Info Link
    if soup.find(id="block-views-block-good-practices-block-5") is not None:
        info_link = soup.find(id="block-views-block-good-practices-block-5").get_text().strip()[20:]
    else:
        info_link = "NA"
        
    
    
    data = [project, description, start_date, end_date, partners, contact_name, contact_link, sdg_list, info_link]
    
    return data


# Method for retrieving the url extensions for each project in the page
def get_links(root, extension):
    html = get_html(root, extension)
    soup = BeautifulSoup(html, 'html.parser')
    elements = list(soup.find_all('div', class_ = 'views-field views-field-title'))
    
    href_links = []

    for element in elements:
        soup = BeautifulSoup(str(element), 'html.parser')
        a = soup.find('a')['href']
        href_links.append(a)
    
    return href_links


# Method for exporting data into a csv file
def write_data(data):
    
    with open('WebScraping.csv', 'a+', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def scrape_range(browse_url, page_range, root):
    extensions = []
    # Getting the extensions in the range
    for page in page_range:
        extension = get_links(browse_url, str(page))
        extensions.extend(extension)
        print(f'Extensions in page {page} saved.')
    
    # Iterating through the extensions and writing the data to the excel file    
    for ext in extensions:
        html_con = get_html(root, ext)
        data = scrape_data(html_con)
        link = root + ext
        data.append(link)
        write_data(data)
        print(f'Data in extension {ext} is saved.')
        
    print(f'Data in {page_range} has been successfully saved in excel file.')
