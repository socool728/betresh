import datetime
import bs4
import requests

url = input("Enter URL")
current_month = datetime.datetime.now().month
current_year = datetime.datetime.now().year

print(current_month - 6)