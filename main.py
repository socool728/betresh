import datetime
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import Workbook

# https://www.betrush.com/pick,Capalaba_Women_vs_Lions_Women,219834.html
url = 'https://www.betrush.com/tipster,1477.html'

# url = input("Enter URL: ")
current_month = datetime.datetime.now().month
current_year = datetime.datetime.now().year

options = Options()
options.headless = True
driver = webdriver.Chrome()
# driver.set_window_size(1366, 768)
driver.get(url)
action = ActionChains(driver)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tipstername")))
name = driver.find_element(By.CSS_SELECTOR, "div.tipstername").text
print(name)
trs = driver.find_elements(By.CSS_SELECTOR, 'div#bymonth table tbody tr')
links = []
data = []
data_num = 1
for i in range(1, len(trs), 2):
    tds = trs[i].find_elements(By.TAG_NAME, 'td')
    date = tds[0].text.split('-')
    pick = tds[len(tds) - 1].find_element(By.TAG_NAME, 'a')
    if(int(date[0]) >= current_month - 6 and int(date[1]) == current_year):
        driver.execute_script("arguments[0].click();", pick)
        time.sleep(0.5)
        anchors = trs[i + 1].find_elements(By.CSS_SELECTOR, "table tbody tr td:first-child a")
        for anchor in anchors:
            if("https://www.betrush.com/pick" in anchor.get_attribute('href')):
                links.append(anchor.get_attribute('href'))
for link in links:
    driver.get(link)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[style="font-size:11px;"]')))
    span_element = driver.find_element(By.CSS_SELECTOR, 'span[style="font-size:11px;"]')

    # Get the text of the span element
    span_text = span_element.text

    # Extract the date from the span text
    country = span_text.split('\n')[0].split(" ")[1]
    event_date = span_text.split('\n')[1].split(": ")[1]
    event_name = driver.find_element(By.TAG_NAME, 'h1').text
    pick = driver.find_element(By.CSS_SELECTOR, 'span.pick_bookie').text.split('\n')[0].split(": ")[1]
    data.append({
        "sport": "Football",
        "country": country,
        'URL': url,
        'pick': pick,
        'event_name': event_name,
        'event_date': event_date,
        'combopick': 'TBC',
        'formula': f'=IF(OR(ISNUMBER(SEARCH($C${data_num}, D{data_num}))=1, ISNUMBER(SEARCH($C${data_num}, G{data_num}))=1), E{data_num} & G{data_num}, ""',
        'time_stamp': 'TBC',
        'closing_odd': 'TBC'
    })
    data_num = data_num + 1
        
wb = Workbook()
ws = wb.active
ws.append(["Sport", "Country", "URL", "Pick", "Event Name", "Event Date", "Combo Pick", "Formula", "Time Stamp", "Closing Odd"])
for data_simple in data:
    newData =[ data_simple["sport"], data_simple["country"], data_simple["URL"], data_simple["pick"], data_simple["event_name" ], data_simple["event_date" ], data_simple["combopick" ], data_simple["formula"], data_simple["time_stamp"], data_simple["closing_odd"]]
    ws.append(newData)
wb.save(f"{name}.xlsx")