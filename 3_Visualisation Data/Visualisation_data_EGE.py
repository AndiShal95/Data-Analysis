'''
Типы визуализации данных. Задача:
1) Загрузите данные по ЕГЭ за последние годы: https://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv
2) Выбрать данные за 2018-2019 учебный год.
3) Выберите тип диаграммы для отображения результатов по административному округу Москвы,
  постройте выбранную диаграмму для количества школьников, написавших ЕГЭ на 220 баллов и выше.
4) Выберите тип диаграммы и постройте ее для районов Северо-Западного административного округа Москвы для количества
   школьников, написавших ЕГЭ на 220 баллов и выше.
'''
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 10)
pd.set_option('display.width', 1000)

data = pd.read_csv("http://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv", delimiter=";")
data["District"] = data["District"].str.replace("район", "").astype("category")   # убираем слово район, и назначаем колонку с данными как категорию, для быстрой сортировки
data["AdmArea"] = data["AdmArea"].apply(lambda x: x.split(" ")[0]).astype("category")  # разбиваем строку по пробелу, берем первый элемент
data = data.set_index("YEAR").loc["2018-2019"].reset_index()    # взяли индексную колонку "YEAR", отсортировали нужные данные и сбросили индекс

#  выводим круговую диаграмму распределения данных по административным округам Москвы
fig = plt.figure(figsize=(12, 12))    # выводим холст для построения графиков
area = fig.add_subplot(1, 2, 1)      # на первой части выведем график
area.set_title("ЕГЭ в Москве", fontsize=20)    # заголовок графика
data_adm = data.set_index("AdmArea")   #  взяли индексную колонку "AdmArea"
data_adm["PASSES_OVER_220"].groupby("AdmArea").sum().plot.pie(ax=area, label="")   # извлекаем данные по отличникам,
                                # группируем по округам и выводим сумму отличников в каждом округе на круговой диаграмме

# строим второй тип диаграммы для распределения отличников по Северо-Западному административному округу Москвы
area = fig.add_subplot(1, 2, 2)
area.set_title("ЕГЭ в СЗАО", fontsize=20)
data_district = data_adm.loc["Северо-Западный"].reset_index().set_index("District")    # выбираем данные по СЗАО, сбрасываем индекс по "AdmArea" и
                                                                                        # назначаем индекс по району
data_district = data_district["PASSES_OVER_220"].groupby("District").sum()
total = sum(data_district)    # суммируем результаты по районам
data_district.plot.pie(ax=area, label="", autopct=lambda x: round(int(total * x / 100)))  # проставляем результаты на круговой диаграмме
plt.show()




