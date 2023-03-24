import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers 


hh = 'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=python&ored_clusters=true'
headers = Headers(os='win', browser='opera')
def get_page(url):
    return requests.get(url, headers=headers.generate())
html = get_page(hh).text

soup = BeautifulSoup(html, "html.parser")
jobs = soup.find_all("div", class_="vacancy-serp-item__layout")

job_list = []

def str_check(el) -> str:
    if not el:
        return "Данные не указаны"

    return el.get_text(strip=True) 

for job in jobs:
    description = job.find("div", class_="g-user-content").text.lower()
    print(description)
    print()
    if "django" in description or "flask" in description:
        title = job.find("a", class_="serp-item__title").text
        link = job.find('a')['href']
        company = job.find('a', {'data-qa': "vacancy-serp__vacancy-employer"}).text
        salary = str_check(job.find('span', {'data-qa':"vacancy-serp__vacancy-compensation"}))
        address = job.find('div', {'data-qa': "vacancy-serp__vacancy-address"}).text

        job_info = {
            "title": title,
            "link": link,
            "company": company,
            "salary": salary,
            "address": address,
        }
        job_list.append(job_info)

with open("job_information.json", "w", encoding="utf-8") as f:
    json.dump(job_list, f, indent=4, ensure_ascii=False)

    

