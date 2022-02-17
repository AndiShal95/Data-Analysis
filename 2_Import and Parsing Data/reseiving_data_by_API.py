'''
Получение данных по API
Задание:
1) Изучить API геокодера Яндекса
2) Получить ключ API в кабинете разработчика
3) Выполнить запрос к API и узнать долготу точки на карте(Point) для города Самара
'''
import requests
import json

# https://geocode-maps.yandex.ru/1.x?geocode=Самара&apikey=700575a5-4b23-40bc-838b-255d2ffd4bdc&format=json&result=1

r = requests.get("https://geocode-maps.yandex.ru/1.x?geocode=РоссияСамара&apikey=700575a5-4b23-40bc-838b-255d2ffd4bdc&format=json&result=1")

geo = json.loads(r.content)
print(geo["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")[0])

# Поочередная распаковка словарей .json для нахождения point - искомой координаты города