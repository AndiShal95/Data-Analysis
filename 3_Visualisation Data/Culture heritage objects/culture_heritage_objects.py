'''
Объекты культурного наследия России.
Задача:
1) Изучите данные по объектам культурного наследия России (gz-архив): http://video.ittensive.com/python-advanced/data-44-structure-4.csv.gz
2) Построить фоновую картограмму по количеству объектов в каждом регионе России, используя гео-данные: https://video.ittensive.com/python-advanced/russia.json
3) Выведите для каждого региона на карте количество объектов в нем.
4) Определить число объектов культурного наследия в Татарстане.
'''
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import descartes

# загружаем данные по культурным объектам
data = pd.read_csv("data-44-structure-4.csv.gz", usecols=["Объект", "Регион"])  # загружаем данные локально из-за большого объема
data["Регион"] = data["Регион"].str.upper()   # приводим данные региона к верхнему регистру
data = data.groupby("Регион").count()    # группируем данные по региону и считаем кол-во объектов
# print(data.index.values)

# загружаем гео-данные
geo = gpd.read_file("russia.json")   # загружаем координаты объектов формата .json
geo = geo.to_crs({"init": "epsg:3857"})  # приводим к проекции Меркатора
geo["NL_NAME_1"] = geo["NL_NAME_1"].str.upper()   # приводим данные названий регионов к верхнему регистру

# Произведем унификацию названия для набора данных
geo = geo.replace({
    "ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ": "ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ - ЮГРА",
    "РЕСПУБЛИКА АДЫГЕЯ": "РЕСПУБЛИКА АДЫГЕЯ (АДЫГЕЯ)",
    "ЧУВАШСКАЯ РЕСПУБЛИКА": "ЧУВАШСКАЯ РЕСПУБЛИКА - ЧУВАШИЯ",
    "РЕСПУБЛИКА МАРИЙ-ЭЛ": "РЕСПУБЛИКА МАРИЙ ЭЛ",
    "РЕСПУБЛИКА СЕВЕРНАЯ ОСЕТИЯ": "РЕСПУБЛИКА СЕВЕРНАЯ ОСЕТИЯ - АЛАНИЯ",
    "РЕСПУБЛИКА ТАТАРСТАН": "РЕСПУБЛИКА ТАТАРСТАН (ТАТАРСТАН)"
})

geo = pd.merge(left=geo, right=data,     # объединяем данные в один фрейм, указав расположение данных и наименования
               left_on="NL_NAME_1", right_on="Регион", how="left")
# print(geo[geo["Объект"].isnull()])   # проверка выода данных, которые не смогли объединить в датафрейм

# отрисовываем данные на графике
fig = plt.figure(figsize=(16, 9))   # создаем холст для построения графика
area = plt.subplot(1, 1, 1)   # задаем область отрисовки графика
geo.plot(ax=area, legend=True, column="Объект", cmap="plasma")  # строим график на области отрисовки, отображаем легенду
area.set_xlim(2e6, 2e7)

for _, region in geo.iterrows():     # дополнительно вводим аннотацию в виде числа объектов в каждом регионе
    area.annotate(region["Объект"],
                  xy=(region.geometry.centroid.x,
                      region.geometry.centroid.y), fontsize=8)
plt.show()
print(geo[geo["NL_NAME_1"] == "РЕСПУБЛИКА ТАТАРСТАН (ТАТАРСТАН)"]["Объект"])

