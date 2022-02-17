'''
Парсинг интернет-магазина
Задача:
1) Используя методы парсинга, найти информацию о двух товарах на сайте
2) Определить на сколько литров отличается общий объем холодильников Саратов 263 и Саратов 452?
'''
# страница донор "https://video.ittensive.com/data/018-python-advanced/beru.ru/"

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "ittensive-python-courses/1.0 (+schaltyckov95@yandex.ru)"}    # этика парсинга с обозначением пользователя, собирающего информацию
r = requests.get("https://video.ittensive.com/data/018-python-advanced/beru.ru/", headers=headers)
html = BeautifulSoup(r.content, "lxml")
links = html.find_all("a", {"class": "_3ioN70chUh"})   # ищем все ссылки, по которым можно найти нужные холодильники
for link in links:    #  перебираем ссылки
    if str(link).find("Саратов 263") > -1:
        link_263 = link["href"]
    if str(link).find("Саратов 452") > -1:
        link_452 = link["href"]


def find_volume (link):
    r = requests.get("https://video.ittensive.com/data/018-python-advanced/beru.ru/" + link)
    html = BeautifulSoup(r.content, "lxml")
    volume = html.find_all("span", {"class": "_112Tad-7AP"})   # находим строку со значением объема холодильника
    return int(''.join(i for i in volume[2].get_text() if i.isdigit()))  # выделяем из найденной строки числа


if link_263 and link_452:         #   находим разницу значений объемов холодильников с помощью функции find_volume
    volume_263 = find_volume(link_263)
    volume_452 = find_volume(link_452)
    diff = max(volume_263, volume_452) - min(volume_263, volume_452)
    print(diff)
    # print(volume_263, volume_452)
