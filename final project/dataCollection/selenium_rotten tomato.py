import requests
import csv
import pandas as pd
import os
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

web="https://www.rottentomatoes.com/"
fake_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
}


driver_path = os.path.join('D:\chrome', "chromedriver")
driver = webdriver.Chrome(driver_path)

driver.get(web)
elem = driver.find_element_by_class_name("search-text")#根据类名找到搜索框
elem.send_keys('Arrival')#搜索关键词
elem.send_keys(Keys.ENTER)
#time.sleep(5)

page = driver.page_source

driver.close()

soup = BeautifulSoup(page,'html.parser')

print(soup)

year = soup.find("span", attrs={"class":"year"}).get_text().strip()
percent = soup.find("span", attrs={"class":"percentage"}).get_text().strip()


print(year,percent)
