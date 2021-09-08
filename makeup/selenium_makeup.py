import selenium 
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
import pyodbc 
from config import server,database,username,password


def writeToDB(fragrance):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO dbo.parfumes_ values(?,?,?,?,?,?,?,?,?,?,?,?)", 
    fragrance['Классификация'].values[0],
    fragrance['Тип аромата'].values[0],
    fragrance['Пол'].values[0],
    fragrance['Начальная нота'].values[0],
    fragrance['Нота сердца'].values[0],
    fragrance['Конечная нота'].values[0],
    fragrance['Сделано в'].values[0],
    fragrance['Премьера аромата'].values[0],
    fragrance['Страна ТМ'].values[0],
    fragrance['Code'].values[0],
    fragrance['Brand'].values[0],
    fragrance['Parfume'].values[0])
    cnxn.commit()
    cursor.close()


def getPages(driver):
    driver.get('https://makeup.com.ua/categorys/3/#o[2251][]=22429&o[2251][]=22443&o[2251][]=23335')
    parsed_html = BeautifulSoup(driver.page_source,'html.parser')
    pages = int(parsed_html.find_all('li','page__item')[-1].text)
    return pages 

def createDF(driver):
    driver.get('https://makeup.com.ua/product/127021')
    parsed_html_one = BeautifulSoup(driver.page_source,'html.parser')
    columns = []
    for length in parsed_html_one.find_all("strong"):
        columns.append(length.text[:-1])
    columns = columns[:9]
    columns.extend(['Code','Brand','Parfume'])
    fragrance = pd.DataFrame(columns=columns)
    return fragrance

def addParfume(page,driver,fragrance):
    driver.get("https://makeup.com.ua/product/{}/".format(page))
    parsed_html_one = BeautifulSoup(driver.page_source,'html.parser')
    for col in parsed_html_one.find_all("strong")[:9]:
        try:
            fragrance.loc[0,col.text[:-1]] = col.next_sibling.strip()
        except:
            continue
    fragrance.loc[0,'Code'] = page
    fragrance.loc[0,'Brand'] = parsed_html_one.find_all('span',itemprop="name")[3].text
    fragrance.loc[0,'Parfume'] = parsed_html_one.find_all('span',itemprop="name")[2].text
    writeToDB(fragrance)



def f(i,fragrance):
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://makeup.com.ua/categorys/3/#o[2251][]=22429&o[2251][]=22443&o[2251][]=23335&offset={}".format(36*i))
    parsed_html_page = BeautifulSoup(driver.page_source,'html.parser')
    for j in parsed_html_page.find_all('li',{'class': 'simple-slider-list__item'}):
        try:
            addParfume(j['data-id'],driver,fragrance)
        except:
            continue
    driver.close()

# def main(): 
#     pool = Pool(4)
#     pool.map(f, range(1,getPages()))

def main():
    driver = webdriver.Chrome('./chromedriver')
    fragrance = createDF(driver)
    pages = getPages(driver)
    driver.close()
    for i in range(1,pages):
        f(i,fragrance)

main()
