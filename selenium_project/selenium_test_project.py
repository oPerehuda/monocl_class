from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC

import time

wb = Workbook()
ws = wb.active

table_title = [
    'Rank', 
    'Album', 
    'Artist', 
    'Duration',
    ]
ws.append(table_title)

driver = webdriver.Firefox()

driver.get("https://en.wikipedia.org/wiki/Billboard_200")

table = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr')


for item in table[1:]:
    rank = item.find_element(By.XPATH, './th[1]').text
    #album = item.find_element(By.XPATH, './td[1]/i/a').text
    album = item.find_element(By.XPATH, './td[1]').text
    artist = item.find_element(By.XPATH, './td[3]').text
    try:
        duration = item.find_element(By.XPATH, './td[5]').text
    except NoSuchElementException:
        duration = 'no duration'
        
    
    #ws.append([rank, album, artist, duration])
    
    print(rank, album, artist, duration)

#wb.save('WiKi.xlsx')



#driver.quit()
