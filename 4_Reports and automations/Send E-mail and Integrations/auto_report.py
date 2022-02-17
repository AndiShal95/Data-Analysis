'''
Автоматические отчеты - создание отчета и отправка по электронной почте
Задача:
1) Собрать отчет по результатам ЕГЭ в 2018-2019 году, используя данные: https://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv
2) Отправтье отчет в HTML формате по адресу support@ittensive.com, используя только Python
Отчет состоит из:
а) общее число отличников (учеников, получивших более 220 баллов по ЕГЭ в Москве)
б) распределение отличников по округам Москвы
в) название школы с лучшими результатами по ЕГЭ в Москве

  Диаграмма распределения должна быть вставлена в HTML через data:URI формат (в base64-кодировке).
Приложить к отчету PDF документ того же содержания (дублирующий письмо).
'''
import os
import pandas as pd
import matplotlib.pyplot as plt
import pdfkit
from io import BytesIO
import binascii
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 500)
pd.set_option('display.width', 1000)

data = pd.read_csv("http://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv", delimiter=";")
data = data[data["YEAR"] == "2018-2019"]  # выделяем из файла данные только 2018-2019 годов
data_best = data.sort_values("PASSES_OVER_220", ascending=False).head(1)  # находим лучшую школу по результатам ЕГЭ за 18-19 год
data["AdmArea"] = data["AdmArea"].apply(lambda x: x.split(" ")[0])  # преобразуем названия адм.округа, оставив только 1-е слово
data_adm = data.groupby("AdmArea").sum()["PASSES_OVER_220"].sort_values()  # сгруппируем данные по округам, найдем сумму отличников по каждому округу
total = data_adm.sum()  # общее число отличников по административным округам Москвы, данные для отчета и вывода доли


# Создаем холст и график для визуализации данных
fig = plt.figure(figsize=(11, 6))   # создаем холст для нанесения графика
area = fig.add_subplot(1, 1, 1)     # строим график на холсте
explode = [0] * len(data_adm)       # задаем на графике explode(доли из кругового графика и меру их выноса из основной массы)
explode[0] = 0.4       # выносим из графика первые две доли, как наименьшие по округам
explode[1] = 0.4
data_adm.plot.pie(ax=area,
                  labels=[""] * len(data_adm),
                  label="Отличники по ЕГЭ",
                  cmap="tab20",
                  autopct=lambda x: int(round(total * x / 100)),
                  pctdistance=0.9,
                  explode=explode)
plt.legend(data_adm.index, bbox_to_anchor=(1.5, 1, 0.1, 0))  # справа выводим легенду с подписями округов
# plt.show()

# Сохраняем получившийся график как отдельное изображение для будущего отчета
img = BytesIO()     # создаем объект в памяти для изображения
plt.savefig(img)    # сохраням картинку
img = 'data:image/png;base64,' + binascii.b2a_base64(img.getvalue(), newline=False).decode("UTF-8")  # Для вставки изображения в отчет
# преобразуем его в b64 кодировку
# print(img)

# Формируем HTML-отчет со всеми данными
html = '''<html>
<head>
    <title>Результаты ЕГЭ по Москве: отличники</title>
    <meta charset="utf-8"/>
</head>
<body>
    <h1>Результаты ЕГЭ по Москве: отличники в 2018-2019 году</h1>
    <p>Всего: ''' + str(total) + '''</p>
    <img src="''' + img + '''" alt="Отличники по округам"/>
    <p>Лучшая школа: ''' + str(data_best["EDU_NAME"].values[0]) + '''</p>
</body>
</html>'''

# сформируем из отчет из HTML-страницы с помощью pdfkit
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
options = {
    "page-size": "A4",
    "header-right": "[page]"
}

pdfkit.from_string(html, "ege.best.pdf", configuration=config, options=options)  # формируем отчет из HTML

# Сформированный отчет отправляем по e-mail
letter = MIMEMultipart()
letter['From'] = "schaltyckov95@yandex.ru"   # почта-отправитель
letter['Subject'] = "Результаты по ЕГЭ в Москве"
letter['Content-Type'] = "text/html; charset=utf-8"
letter['To'] = "support@ittensive.com"     # почта-получатель
letter.attach(MIMEText(html, "html"))
attachment = MIMEBase("application", "pdf")
attachment.set_payload(open("ege.best.pdf", "rb").read())
attachment.add_header("Content-Disposition",
                      "attachment", filename="ege.best.pdf")
encoders.encode_base64(attachment)
letter.attach(attachment)
user = "schaltyckov95@yandex.ru"     # свой логин почты-отправителя
password = "12********76"            # свой пароль почты-отправителя
server = smtplib.SMTP_SSL("smtp.yandex.com", 465)
server.login(user, password)
server.sendmail("schaltyckov95@yandex.ru",
                "support@ittensive.com",
                letter.as_string())
server.quit()


# os.getenv("EMAIL_PASSWORD")

