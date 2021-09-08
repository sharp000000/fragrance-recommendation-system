from bs4 import BeautifulSoup
import selenium 
from selenium import webdriver
import requests
import json
import pandas as pd
import time

base_url = 'https://www.sephora.com'
url = 'https://www.sephora.com/shop/fragrances-for-women'

driver = webdriver.Chrome('../chromedriver') 

def getPages(url):
    driver.get(url)
    parsed_html = BeautifulSoup(driver.page_source, 'html.parser')
    return int(parsed_html.find('div', 'css-6su6fj').find_all('li')[-1].find('button', 'css-cx0up1 eanm77i0').text)


def collectParfumeLinks(pages):
    parfumeLinks = []
    driver = webdriver.Chrome('../chromedriver') 
    for page in range(1, pages+1):
        driver.get('{0}?currentPage={1}'.format(url, page))
        y = 0
        # print(driver.execute_script('return document.body.scrollHeight;'))
        while y < driver.execute_script('return document.body.scrollHeight;'):
            driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 200
        parsed_html = BeautifulSoup(driver.page_source, 'html.parser')
        
        for i in parsed_html.find_all('div', 'css-dkxsdo'):
            for a in i.find_all('a', href=True):
                parfumeLinks.append('{0}{1}'.format(base_url, a['href']))

    return parfumeLinks

pages = getPages(url)
collectParfumeLinks(pages)