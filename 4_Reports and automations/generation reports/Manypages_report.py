'''
Многостраничный отчет
Задача:
1) Используя данные по активностям в парках Москвы: http://video.ittensive.com/python-advanced/data-107235-2019-12-02.utf.json
2) Создайте PDF отчет, в котором выведите:
   а) Диаграмму распределения числа активностей по паркам, топ10 самых активных
   б) Таблицу активностей по всем паркам в виде Активность-Расписание-Парк
'''
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO     # преобразование изображений в bs64 (временное хранение бинарных данных изображения)
import binascii        # конвертация бинарных данных
import pdfkit

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)

r = requests.get("https://video.ittensive.com/python-advanced/data-107235-2019-12-02.utf.json")
data = pd.DataFrame(json.loads(r.content),      # из запрошенных данных извлекаем только три колонки для отчета
                    columns=["CourseName", "CoursesTimetable", "NameOfPark"])
data['NameOfPark'] = data['NameOfPark'].apply(lambda x: x['value'])   # из колонки с данными в формате(ключ:значение)
# извлекаем значение с помощью лямбда-функции
data.columns = ['Активность', 'Расписание', 'Парк']   # изменяем наименование колонок с данными
# print(data.head())
print('Тайцзицюань: ',
      data[data["Активность"].str.contains('Тайцзицюань')]['Активность'].count())   # находим сколько 'Тайцзицюань' есть в Москве

# Формируем диаграмму активностей по паркам
fig = plt.figure(figsize=(12, 6))     # создаем холст для нанесения графика
area = fig.add_subplot(1, 1, 1)       # создаем область графика на холсте
parks = data.groupby("Парк").count().sort_values("Активность", ascending=False)    # группируем данные по паркам(одинаковые строки складываем)
                                                                     # и сортируем по активности в порядке убывания
parks.head(10)["Активность"].plot.pie(ax=area, label="")   # топ-10 из списка парков по активности вносим в круговую диаграмму
img = BytesIO()
plt.savefig(img)        # временно сохраняем изображение графика
img = 'data:image/png;base64,' + binascii.b2a_base64(img.getvalue(), newline=False).decode("UTF-8")  # преобразовываем бинарные данные к bs64
# print(img)   # декодированная информация изображения

# формируем заголовки HTML-отчета
html = '''<html>
<head>
    <title>Активности в парках Москвы</title>
    <meta charset="utf-8"/>
</head>
<body>
    <h1>Активности в парках Москвы</h1>
    <img src="''' + img + '''" alt="Популярные парки"/>
    ''' + data.to_html(index=False) + '''
</body>
</html>'''

# собираем все данные для создания PDF-отчета
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
# задаем опции страницы PDF-отчета
options = {
    'page-size': 'A4',
    'header-right': '[page]'
}
# сгенерируем из HTML-строк PDF-отчет
pdfkit.from_string(html, 'parks.pdf', configuration=config, options=options)
# ---------------------------------





