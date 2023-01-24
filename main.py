import pygame
import requests
import os

ll = input().split()

spn = input()

api_server = "http://static-maps.yandex.ru/1.x/"

params = {
    "ll": ",".join([ll[0], ll[1]]),
    "spn": ",".join([spn, spn]),
    "l": "map"
}

response = requests.get(api_server, params=params)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
# пример ввода ll - 37.530887 55.703118 | spn - 0.002
