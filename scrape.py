import requests
from bs4 import BeautifulSoup
import re
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

vacancies = []
for vacancy in soup.find_all('div', {'class': 'vacancy-serp-item'}):
    link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
    company = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).text
    city = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).text
    wages = vacancy.find('div', {'class': 'vacancy-serp-item__compensation'}).text
    min_wage, max_wage = re.findall(r'\d+', wages)
    description = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).text
    if re.search("Django", description) and re.search("Flask", description):
        vacancies.append({'link': link, 'company': company, 'city': city, 'min_wage': min_wage, 'max_wage': max_wage})

with open('vacancies.json', 'w') as f:
    json.dump(vacancies, f)
