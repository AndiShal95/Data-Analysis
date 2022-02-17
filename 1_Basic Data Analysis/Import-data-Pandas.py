'''
Задание импортировать данные по вызовам пожарных служб в Москве за 2015-2019 годы с сайта:
1) Получите из них фрейм данных (таблицу значений)
2) По табличным данным вычислите среднее значение вызовов пожарных машин в месяц
   в одном округе Москвы, округлив до целых
'''

import pandas as pd

pd.set_option('max_rows', 25)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)

df = pd.read_csv('http://video.ittensive.com/python-advanced/data-5283-2019-10-04.utf.csv', delimiter=';', index_col='ID')
# print(df.head())
print(df["Calls"].mean().round())  # подсчет среднего числа вызовов из столбца файла и округление до целого
