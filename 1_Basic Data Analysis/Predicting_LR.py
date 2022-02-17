'''
Предсказать процентное значение безработных людей с ограниченными возможностями относительно всего
безработного населения России за 2020 год, округлить ответ до сотых процента
'''

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

pd.set_option('max_rows', 25)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)

data = pd.read_csv('http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv', delimiter=';')

# Нужно определить процентное соотношение между столбцами UnemployedDisabled/UnemployedTotal
data["UPD"] = round((100 * data['UnemployedDisabled'] / data['UnemployedTotal']), 2)
# print(data.head())

data_group = data.groupby("Year").filter(lambda x: x["UPD"].count() > 5)  # сортируем данные по годам и фильтруем по
# количеству записей за год, должно быть не меньше 6-ти записей, т.к. статистика с меньшим кол-вом данных не репрезентативна
# Метод .filter возвращает не группы данных, а чистые данные по условию, поэтому снова нужна группировка
data_group = data_group.groupby("Year").mean()   # группируем данные по году, и находим среднее значение за год
# print(data_group)

x = np.array(data_group.index).reshape(len(data_group.index), 1)
y = np.array(data_group["UPD"]).reshape(len(data_group.index), 1)
# .reshape(len(data_group.index), 1) - это форма данных двумерного массива

model = LinearRegression()    # для полученных данных применяем модель линейной регрессии
model.fit(x, y)    # подгоняем значения x, y  под коэффициенты построенной линии регрессии

# print(model.predict(np.array(2020).reshape(1, 1)))  # предсказываем значение следующего индекса по линии линейной регрессии
print(np.round(model.predict(np.array(2020).reshape(1, 1)), 2))   # округляем значение предсказания согласно условиям задачи


