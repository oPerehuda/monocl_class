from selenium import webdriver
import time


driver = webdriver.Firefox()

driver.get("https://www.wikipedia.org/")

time.sleep(5)
driver.quit()

