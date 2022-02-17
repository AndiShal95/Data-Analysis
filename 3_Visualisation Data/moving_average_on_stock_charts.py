'''
Скользящие средние на биржевых графиках
Задача:
1) Загрузить данные индекса Российских Торговых Систем(РТС): http://video.ittensive.com/python-advanced/rts-index.csv
2) Построить отдельные графики закрытия (Close) индекса по дням за 2017, 2018, 2019 годы в единой оси X.
3) Добавить на график экспоненциальное среднее за 20 дней для значения Max за 2017 год.
4) Найти последнюю дату, когда экспоненциальное среднее максимального дневного значения (Max) в 2017 году было больше,
 чем соответствующее значение Close в 2019 году (это последнее пересечение графика за 2019 год и графика для среднего за 2017 год).
'''
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('max_rows', 100)
pd.set_option('max_columns', 25)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 1000)

data = pd.read_csv("http://video.ittensive.com/python-advanced/rts-index.csv")
# Приведем все данные к дням года, чтобы отобразить на оси Х
data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)    # преобразуем данные строки в данные по времени, чтобы не было ошибок при преобразовании
                                                                # данных -> вводим dayfirst-True
dates = pd.date_range(min(data["Date"]), max(data["Date"]))
data = data.set_index("Date")
data = data.reindex(dates).ffill()    # Переиндексируем данные и заполняем пустые ячейки предыдущими значениями
data["Day"] = pd.to_datetime(data.index).dayofyear   # добавим серию данных "День года" для подписи по оси Х
data.index.name = "Date"   # назначаем название индекса, которое утратили при переиндексации
data.sort_index()
data_2019 = data["2019"].reset_index().set_index("Day")    # создаем отдельную серию данных 2019, для дальнейшего сравнения с 2017 годом
data_2017 = data["2017"].reset_index().set_index("Day")["Max"].ewm(span=20).mean()  # создаем отдельную серию данных 2017 как экспоненциальную среднюю со сдвигом 20

fig = plt.figure(figsize=(12, 8))    # создаем холст для отображения графиков
area = fig.add_subplot(1, 1, 1)    # строим график(область графика) на весь холст
data_2019["Close"].plot(ax=area, color="red", label="2019", lw=3)

data_2017.plot(ax=area, color="blue", label="Exp.2017", lw=3)   # нанесем обычную серию данных за 2017 год в виде фоновой области
data["2017"].reset_index().set_index("Day")["Close"].plot.area(ax=area, color=".5", label="2017")
data["2018"].reset_index().set_index("Day")["Close"].plot(ax=area, color="green", label="2018", lw=3)  # наносим на график данные за 2018 год в виде линии
data_fall = data_2019[data_2019["Close"] < data_2017[0:len(data_2019)]]   # фильтруем и выбираем данные, когда данные по закрытой позиции в 2019
                                                                                # окончательно превзошли максимум за 2017 год
data_fall.set_index("Date", inplace=True)     # создаем индекс для фильрованных данных
data_fall = data_fall.sort_index(ascending=False)  # сортируем по индексу в порядке убывания

plt.legend()    # указываем на графике легенду, с обозначением каждой линии
plt.show()
print(data_fall.head(1).index)