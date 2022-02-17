'''
Создание многостраничного отчета (сборка PDF-документа)
Задача:
1) Загрузить данные по посещаемости библиотек в районах Москвы: https://video.ittensive.com/python-advanced/data-7361-2019-11-28.utf.json
2) Построить круговую диаграмму суммарной посещаемости (NumOfVisitors) 20-ти наиболее популярных районов Москвы
3) Создайте PDF отчет, используя файл в качестве 1-й страницы: https://video.ittensive.com/python-advanced/title.pdf
4) Вывести итоговую диаграмму, самый популярный район Москвы и число посетителей библиотек в нем на 2-й странице
'''

from reportlab.pdfgen import canvas                       #   холст документа
from reportlab.lib import pagesizes                       #   формат листа
from reportlab.pdfbase import pdfmetrics                  #   доступ к шрифтам и изображениям из reportlab
from reportlab.pdfbase.ttfonts import TTFont              #   импорт truetype font
from reportlab.lib.utils import ImageReader               #   чтение .png файлов
from PyPDF2 import PdfFileMerger, PdfFileReader           #   объединение PDF, чтение PDF
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)


def extract_district(x):    # функция извлечения первого элемента списка 'ObjectAddress'-название района
    return list(map(lambda a: a['District'], x))[0]


r = requests.get("http://video.ittensive.com/python-advanced/data-7361-2019-11-28.utf.json")
data = pd.DataFrame(json.loads(r.content)).fillna(value=0)
data["District"] = data["ObjectAddress"].apply(extract_district)  #
data_sum = data.groupby("District").sum().sort_values("NumOfVisitors", ascending=False)
# print(data_sum.index)    # вывод списка всех названий районов(или значений словаря json)

# строим результирующую круговую диаграмму из 20-ти самых популярных районов
fig = plt.figure(figsize=(11, 6))   # строим холст для отображения графика
area = fig.add_subplot(1, 1, 1)     # строим график на холсте
data_sum[0:20]["NumOfVisitors"].plot.pie(ax=area, labels=[""]*20, label="Посещаемость", cmap="tab20")  # строим круговую
# диаграмму из 20-ти наиболее посещаемых библиотек
plt.legend(data_sum[0:20].index, bbox_to_anchor=(1.5, 1, 0.1, 0))  # отображаем в легенде названия районов, где находятся библиотеки
# plt.show()
plt.savefig('readers.png')   # сохраним график в картинку для дальнешей вставки в общий отчет

# формирование отчета (вторая страница общего документа)
PDF = canvas.Canvas("readers.pdf", pagesize=pagesizes.A4)
pdfmetrics.registerFont(TTFont("Trebuchet", "Trebuchet.ttf"))
PDF.setFont("Trebuchet", 48)
PDF.drawString(70, 650, "Посетители библиотек")
PDF.drawString(80, 590, "по районам Москвы")
PDF.setFont("Trebuchet", 13)
PDF.drawString(550, 820, "2")
PDF.drawImage(ImageReader("readers.png"), -200, 150)
PDF.setFont("Trebuchet", 20)
PDF.drawString(100, 150, "Самый популярный район")
PDF.setFont("Trebuchet", 24)
PDF.drawString(100, 120, data_sum.index[0])
PDF.setFont("Trebuchet", 20)
PDF.drawString(100, 90, "Посетителей: " + str(int(data_sum["NumOfVisitors"].values[0])))
PDF.save()

# объединим отчет с титульной страницей
files = ['title.pdf', "readers.pdf"]   # создаем список из соединяемых документов
merger = PdfFileMerger()    # инициализируем соединение документов из библиотеки PyPDF2
for filename in files:        # перебирая файлы
    merger.append(PdfFileReader(open(filename, "rb")))    # открываем и читаем их бинарном виде, далее соединяем в общий файл
merger.write("report.pdf")   # записываем результат в файл с новым названием


