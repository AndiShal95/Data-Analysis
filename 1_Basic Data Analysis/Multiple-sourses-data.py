'''
Задание: получить данные по безработице за 2019 год и данные по вызовам пожарных.
1) Объединить данные из двух источников в одну таблицу по индексу (Месяц-Год) для Центрального административного округа
2) Найдите значение поля UnemployedMen в том месяце, когда было меньше всего вызовов в Центральном административном округе.
'''

import pandas as pd

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', 1000)

#               Подготовка данных
data1 = pd.read_csv('http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv', delimiter=';')
data1 = data1.set_index(["Year", "Period"])   # создаем множественный индекс по году и периоду

data2 = pd.read_csv('http://video.ittensive.com/python-advanced/data-5283-2019-10-04.utf.csv', delimiter=';')
data2 = data2.set_index(["AdmArea", "Year", "Month"])    # создаем множественный индекс по области, году и месяцу
data2 = data2.loc["Центральный административный округ"]   # из множественного индекса по колонке "AdmArea" отбираем нужные данные
data2.index.names = ["Year", "Period"]    # изменяем множественный индекс для соответствия с 1-м dataframe

#               Объединение данных
data = pd.merge(data1, data2, left_index=True, right_index=True)  # объединяем по созданному мультииндексу 2 dataframe
data = data.reset_index()  # отбрасываем объединяющий индекс
data = data.set_index(["Calls"])   # назначаем новый индекс по кол-ву вызовов
data = data.sort_index()  # сортируем индекы по возрастанию

print(data["UnemployedMen"][0:1])   # вывод кол-ва нетрудоустроенных граждан


