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

driver.get("https://tos.planion.com/Web.User/SearchSessions?ACCOUNT=TOS&CONF=OW2024&USERPID=PUBLIC&ssoOverride=OFF&STANDALONE=YES")

table = driver.find_elements(By.XPATH, '//div[@id="CONTENT"]/table[2]/tbody/tr')

print(len(table), "elements found")


for item in table[1:10]:
    session_url_raw = item.find_element(By.XPATH, '.').get_attribute("onclick")
    print(session_url_raw) 
    
    
    
#     rank = item.find_element(By.XPATH, './th[1]').text
#     #album = item.find_element(By.XPATH, './td[1]/i/a').text
#     album = item.find_element(By.XPATH, './td[1]').text
#     artist = item.find_element(By.XPATH, './td[3]').text
#     try:
#         duration = item.find_element(By.XPATH, './td[5]').text
#     except NoSuchElementException:
#         duration = 'no duration'
        
    
    #ws.append([rank, album, artist, duration])
    
    #print(rank, album, artist, duration)

#wb.save('WiKi.xlsx')



#driver.quit()
