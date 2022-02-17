'''
Формирование отчета из набора данных (Геральдические символы Москвы)
Задача:
1) Сгенерировать PDF документ из списка флагов и гербов районов Москвы: https://video.ittensive.com/python-advanced/data-102743-2019-11-13.utf.csv
2) На каждой странице документа выведите название геральдического символа (Name), его описание (Description) и его изображение (Picture).
3) Для показа изображений использовать адрес: https://op.mos.ru/MEDIA/showFile?id=XXX (XXX - это значение поля Picture в наборе данных.)
'''
import pandas as pd
import pdfkit

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.width', 1000)

data = pd.read_csv("http://video.ittensive.com/python-advanced/data-102743-2019-11-13.utf.csv", delimiter=";")
# print(data.head())

# Формируем HTML-документ для отчета
html = '''<html>
<head>
    <title>Геральдические символы Москвы</title>
    <meta charset="utf-8"/>
</head>
<body>'''
for i, item in data.iterrows():    # перебираем в цикле набор данных построчно
    if i == 0:    # для первого столбца данных стиль не задаем
        html += '<h1>' + item['Name'] + '</h1>'
    else:         # для остальных столбцов с данными вставим разрыв страницы(чтобы каждому символу была своя страница)
        html += '<h1 style="page-break-before:always">' + item['Name'] + '</h1>'
# вывод изображения геральдического символа в увеличенном виде, задаем размер картинки, сдвиг слева от страницы
# и задаем source(источник из которого загружаем картинку) на который ссылается тег
    html += '''<p>
        <img style="width:70%;margin-left:15%"
        src="https://op.mos.ru/MEDIA/showFile?id=''' + item['Picture'] + '''">  
    </p>'''
# вывод описания геральдического символа, увеличиваем шрифт для читаемости
    html += '<p style="font-size:150%">' + item['Description'] + '</p>'
html += '</body></html>'      #

# сконфигурируем HTML-код в PDF-отчет при момощи библиотеки pdfkit и бинарного файла, к которому пропишем путь
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

# задаем опции страницы PDF-отчета: размер листа и пагинацию(автонумерацию страниц) в верхнем колонтитуле справа
options = {
    'page-size': 'A4',
    'header-right': '[page]'
}
pdfkit.from_string(html, 'heraldic.pdf', configuration=config, options=options)  # сгенерируем из строки HTML-файл в PDF-отчет
# -------------------



