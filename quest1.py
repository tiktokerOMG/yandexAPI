import os
import sys

import pygame
import requests

from object_delta import object_delta

toponym_to_find = 'г. Бугульма, ул. Мусы Джалиля, 60'
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print('Ошибка запроса.')


# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
corners = toponym["boundedBy"]["Envelope"]
lower_corner = corners["lowerCorner"].split()
up_corner = corners["upperCorner"].split()
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

toponym_longitude = float(toponym_longitude)
toponym_lattitude = float(toponym_lattitude)


object_x = object_delta(toponym)[0]
object_y = object_delta(toponym)[1]

map_params = {
    "ll": ",".join([str(i) for i in (toponym_longitude, toponym_lattitude)]),
    "l": "map",
    "z": 16,
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
response = requests.get(map_api_server, params=map_params)
with open(map_file, "wb") as file:
    file.write(response.content)


def refresh():
    response = requests.get(map_api_server, params=map_params)
    with open(map_file, "wb") as file:
        file.write(response.content)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    screen.blit(pygame.image.load("map.png"), (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print('hello1')
            if event.key == pygame.K_PAGEUP:
                print('hello')
                map_params["z"] += 1
            elif event.key == pygame.K_PAGEDOWN:
                map_params["z"] -= 1
            elif event.key == pygame.K_RIGHT:
                toponym_longitude += 0.002
                map_params["ll"] = ",".join([str(i) for i in (toponym_longitude, toponym_lattitude)])
            elif event.key == pygame.K_LEFT:
                toponym_longitude -= 0.002
                map_params["ll"] = ",".join([str(i) for i in (toponym_longitude, toponym_lattitude)])
            elif event.key == pygame.K_DOWN:
                toponym_lattitude -= 0.002
                map_params["ll"] = ",".join([str(i) for i in (toponym_longitude, toponym_lattitude)])
            elif event.key == pygame.K_UP:
                toponym_lattitude += 0.002
                map_params["ll"] = ",".join([str(i) for i in (toponym_longitude, toponym_lattitude)])
    refresh()
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)