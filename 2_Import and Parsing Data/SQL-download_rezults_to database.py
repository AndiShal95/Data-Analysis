"""
Загрузка результатов парсинга в Базу Данных
Задача:
1) Соберите данные о моделях холодильников Саратов с сайта beru.ru: URL, название, цена, размеры, общий объем, объем холодильной камеры.
2) Создайте соответствующие таблицы в SQLite базе данных и загрузите полученные данные в таблицу beru_goods.
"""
import requests
import sqlite3
from bs4 import BeautifulSoup


#  "https://video.ittensive.com/data/018-python-advanced/beru.ru/"  - страница донор, содержащая локальные URL-ы
#   локальный URL-нужного ресурса(страницы донора) ( /kholodilnik-saratov-452-ksh-120.html ) - helper for parsing info from pages

# Вспомогательная функция для нахождения чисел в строке
def find_number(text):
    return int("0" + "".join(i for i in text if i.isdigit()))  # функция возвращает из текста только числа

# Вспомогательная функция-парсер для поиска информации по локальным URL-ам
def find_data(link):  # вводим функцию для того чтобы распарсить ссылки на товары  (использую зеркало сайта beru.ru)
    r = requests.get("https://video.ittensive.com/data/018-python-advanced/beru.ru/" + link)  # link абсолютный(для вывода рез-та подставляем часть нужного URL-a)
    html = BeautifulSoup(r.content, "lxml")
    title = html.find("h1", {"class": "_3TfWusA7bt"}).get_text()  # Находим заголовок товара, позиционируемся по классу, чтобы найти нужный, берем текст у тега <h1>
    price = find_number(html.find("span", {"data-tid": "c3eaad93"}).get_text())
    tags = html.find_all("span", {"class": "_112Tad-7AP"})  # теги с габаритными и рабочими характеристиками товара
    width = 0
    depth = 0  # определяем начальные переменные для параметров товара(если в html не найдутся, то не возникнет ошибки)
    height = 0
    volume = 0  # общий объем холодильника
    freezer = 0  # объем морозильной камеры
    for tag in tags:
        tag = tag.get_text()
        if tag.find("ШхВхГ") > -1:
            dimensions = tag.split(":")[1].split("х")
            # dimensions = tag.split(":")[1].split("X")  # полученные данные тега разделяем по ":", берем вторую часть и делим по "x"
            width = float(dimensions[0])
            depth = float(dimensions[1])
            height = float(dimensions[2].split(" ")[0])  # height = find_number(dimensions[2])
        if tag.find("общий объем") > -1:
            volume = find_number(tag)  # получаем значение тега через функцию поиска цифр в тексте
        if tag.find("объем холодильной камеры") > -1:
            freezer = find_number(tag)
    return [link, title, price, width, depth, height, volume, freezer]    # при вызове функция будет возвращать все обработанные значения и поместит их в список


# print(find_data("/kholodilnik-saratov-452-ksh-120.html"))   # Подставляем локальный URL для вывода результата на нужной странице

r = requests.get("https://video.ittensive.com/data/018-python-advanced/beru.ru/")
html = BeautifulSoup(r.content, "lxml")
links = html.find_all("a", {"class": "_3ioN70chUh"})
data = []
for link in links:
    if link["href"] and link.get_text().find("Саратов") > -1:
        data.append(find_data(link["href"]))
# print(data)

#  Создаем подключение к базе данных, в которую будем загружать результаты парсинга web-страниц
conn = sqlite3.connect("C:/Users/schal/Desktop/sqlite/data.db3")
db = conn.cursor()

# создание таблицы в базе данных
db.execute('''CREATE TABLE beru_refrigerators
            (id INTEGER PRIMARY KEY AUTOINCREMENT not null,
            url text,
            title text default '',
            price INTEGER default 0,
            width FLOAT default 0.0,
            depth FLOAT default 0.0,
            height FLOAT default 0.0,
            volume INTEGER default 0,
            freezer INTEGER default 0)''')
conn.commit()
db.executemany('''INSERT INTO beru_refrigerators (url, title, price, width, depth, height, volume, freezer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', data)   # добавляем в базу данных множество строк одновременно
conn.commit()
print(db.execute('''SELECT * FROM beru_refrigerators''').fetchall())
db.close()
# print(html)
