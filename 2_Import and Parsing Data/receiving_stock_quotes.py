'''
Получение котировок акций
Задание:
1) получить данные котровок акций со страницы сайта МосБиржи
2) найти по какому тикеру был максимальный рост числа сделок(в процентах) за 1 ноября 2019 года
'''
import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('max_rows', 25)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)

r = requests.get(
    "https://mfd.ru/marketdata/?id=5&group=16&mode=3&sortHeader=name&sortOrder=1&selectedDate=01.11.2019")  # запрос на сайт для получения информации
html = BeautifulSoup(r.content, "lxml")  # систематизируем информацию через 'lxml'-парсер
table = html.find("table", {"id": "marketDataList"})  # находим нужный тег, в котором хранится информация, по id
rows = []  # создаем список в который будем собирать информацию из найденных строк
trs = table.find_all('tr')     # находим теги table row
for tr in trs:       # перебираем в цикле
    tr = [td.get_text(strip=True) for td in tr.find_all('td')]  # strip=True - первичная очистка данных от лишних символов
    if len(tr) > 0:  # если длина table row больше нуля
        rows.append(tr)  # добавляем значение в список
# print(rows)
data = pd.DataFrame(rows, columns=["Тикер", "Дата", "Сделки", "С/рост", "С/%", "Закрытие", "Открытие", "min", "max",
                                   "avg", "шт", "руб", "Всего"])
data = data[data["Сделки"] != "N/A"]  # отбрасываем строки, где нет сделок или не определены
data["С/%"] = data["С/%"].str.replace("−", "-").str.replace("%", "").astype(float)   # приводим данные столбца к вещественному виду
data = data.set_index("С/%")   # устанавливаем значения столбца "С/%" в качестве индекса, вместо стандартной нумерации строк Pandas
data = data.sort_index(ascending=False)   # сортировка значений столбца по убыванию

print(data["Тикер"].head(1))
# print(data)
# .str.replace("─", "-")   .astype(float)
