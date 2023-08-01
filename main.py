import datetime
from bs4 import BeautifulSoup
import requests

url = input("Enter URL: ")
current_month = datetime.datetime.now().month
current_year = datetime.datetime.now().year

print(current_month - 6)

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
name = soup.find('div.tipstername').text
trs = soup.find_all('div#bymonth table tbody tr')
for tr in trs:
    print(tr.find('td').text)
country = soup.find_all('a[href="javascript://"]')
print(country.text)