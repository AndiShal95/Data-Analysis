'''
Выделение данных из файла
Задача:
1) Получить данные по безработице в Москве: https://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv
2) Найти, с какого года процент людей с ограниченными возможностями (UnemployedDisabled) среди всех безработных
   (UnemployedTotal) стал меньше 2%
'''
import pandas as pd

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)

data = pd.read_csv("http://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv", delimiter=";")
data["Sum"] = data.apply(lambda x: 100*x[6]/x[7], axis=1)  # создаем новый столбец данных, в котором вычислено
# процентное отношение UnemployedDisabled/UnemployedTotal
data = data[data['Sum'] < 2]    # фильтруем данные по процентному условию задачи
data = data.set_index('Year')   # задаем индекс нумерации данных по колонке 'Year'
data = data.sort_index()    # сортируем данные по возрастанию значения в колонке 'Year'
print(data.index[0:1])      # выводим искомое значение года (с 2018 года)
