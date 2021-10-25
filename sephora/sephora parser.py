from bs4 import BeautifulSoup
import selenium 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import pandas as pd
import time
import warnings 
warnings.filterwarnings("ignore")


base_url = 'https://www.sephora.com'
url = 'https://www.sephora.com/shop/fragrances-for-women'
css_class_pages = 'css-om7j74'

def get_pages(url, css_class_pages):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    parsed_html = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return int(int(parsed_html.find('div', css_class_pages).text.split(' ')[2])/60) + 1 

def collect_parfume_links(pages):
    parfume_links = []
    driver = webdriver.Chrome(ChromeDriverManager().install())

    for page in range(1, pages+1):
        driver.get('{0}?currentPage={1}'.format(url, page))
        y = 0
        # print(driver.execute_script('return document.body.scrollHeight;'))
        while y < driver.execute_script('return document.body.scrollHeight;'):
            driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 100
            time.sleep(1)
        parsed_html = BeautifulSoup(driver.page_source, 'html.parser')
        
        for i in parsed_html.find_all('div', 'css-1322gsb'):
            for a in i.find_all('a', href=True):
                parfume_links.append('{0}{1}'.format(base_url, a['href']))

    return parfume_links


pages = get_pages(url, css_class_pages)
parfume_links = collect_parfume_links(pages)

with open('parfume_links.txt', 'w') as f:
    for item in parfume_links:
        f.write("%s\n" % item)