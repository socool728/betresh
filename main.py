import datetime
from bs4 import BeautifulSoup
import requests

url = input("Enter URL")
current_month = datetime.datetime.now().month
current_year = datetime.datetime.now().year

print(current_month - 6)

response = requests.get("https://api.example.com/data")
soup = BeautifulSoup(response.content, "html.parser")
country = soup.find_all('a[href="javascript://"]')[1]
print(country.text)