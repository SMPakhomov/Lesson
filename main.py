import pygame
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import QLineEdit, QLabel, QPushButton
import sys


class Input(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 320, 400)
        self.setWindowTitle('Введите координаты')
        l = QLabel(self)
        l.setText("Долгота: ")
        l.move(10, 70)
        self.line_ed_l1 = QLineEdit(self)
        self.line_ed_l1.move(70, 70)

        l = QLabel(self)
        l.setText("Широта: ")
        l.move(10, 140)
        self.line_ed_l2 = QLineEdit(self)
        self.line_ed_l2.move(70, 140)

        s = QLabel(self)
        s.setText("Размер: ")
        s.move(10, 210)
        self.s = QLineEdit(self)
        self.s.move(70, 210)

        self.bt_c = QPushButton(self)
        self.bt_c.setText("Найти место")
        self.bt_c.clicked.connect(self.place)
        self.bt_c.move(220, 140)

        l = QLabel(self)
        l.setText("Объект")
        l.move(10, 340)

        self.obj_ln = QLineEdit(self)
        self.obj_ln.move(70, 340)

        self.bt_obj = QPushButton(self)
        self.bt_obj.setText("Найти объект")
        self.bt_obj.clicked.connect(self.obj)
        self.bt_obj.move(220, 340)

    def obj(self):
        object = self.obj_ln.text()
        params = {
            "l": "map",
            "text": object
        }
        self.search_obj(object)

    def place(self):  # поиск места по коорд
        ll = self.line_ed_l1.text(), self.line_ed_l2.text()
        z = self.s.text()

        params = {
            "ll": ",".join([ll[0], ll[1]]),
            "z": z,
            "l": "map"
        }
        self.draw(params)

    def search_obj(self, obj):  # поиск объекта
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        search_params = {
            "apikey": api_key,
            "text": obj,
            "lang": "ru_RU",
        }
        response = requests.get(search_api_server, search_params).json()
        object = response["features"][0]
        coords = object["geometry"]["coordinates"]
        params = {
            "l": "map",
            "ll": ','.join(map(str, coords)),
            "pt": f"{','.join(map(str, coords))},pmgnl",
            "z": '17'
        }
        self.draw(params)

    def draw(self, params):  # рисовка карты по переданным параметрам
        map_file = "map.png"
        pygame.init()
        screen = pygame.display.set_mode((600, 450))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    z_delt = 0
                    if event.key == pygame.K_PAGEUP:  # изм. масштаба
                        z_delt = 1
                    if event.key == pygame.K_PAGEDOWN:  # изм. масштаба
                        z_delt = -1
                    z = int(params["z"]) + z_delt
                    z = max(0, z)
                    z = min(17, z)
                    params["z"] = str(z)

            api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(api_server, params=params)

            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)

            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        pygame.quit()

        os.remove(map_file)


app = QApplication(sys.argv)
ex = Input()
ex.show()
sys.exit(app.exec())

# пример ввода ll - 37.530887 55.703118 | z - 16
