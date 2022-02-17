'''
Результаты марафона. Задача:
1) Загрузить данные по итогам марафона: https://video.ittensive.com/python-advanced/marathon-data.csv
2) Привести время половины и полной дистанции к секундам.
3) Найти, данные каких серии данных коррелируют (используя диаграмму pairplot в Seaborn).
4) Найдите коэффициент корреляции этих серий данных, используя scipy.stats.pearsonr
5) Постройте график jointplot для коррелирующих данных.
'''
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as stats

# используем функцию для конвертации времени к секундам значений марафона и полумарафона
def convert_time(a):
    return sum(x * int(t) for x,t in zip([3600, 60, 1], a.split(":")))


data = pd.read_csv("http://video.ittensive.com/python-advanced/marathon-data.csv", delimiter=",")
# изменяем значения времени split-final при помощи функции convert_time
data["split"] = data["split"].apply(convert_time)
data["final"] = data["final"].apply(convert_time)
# print(data.head())

# Строим парный график для определения данных коррелирующих друг с другом
sns.pairplot(data, hue="gender", height=4)
plt.show()

# Строим корреляционный график между двумя сериями значений и найдем коэффициент корреляции
sns.jointplot("split", "final", data, height=12, kind="kde").annotate(stats.pearsonr)
plt.show()

# Дополнительно выведем коэф-нт Пирсона для 2 серий данных отдельно
print(round(stats.pearsonr(data["split"], data["final"])[0], 2))

