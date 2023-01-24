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
        self.setGeometry(300, 300, 300, 300)
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

        self.bt = QPushButton(self)
        self.bt.clicked.connect(self.map)
        self.bt.move(240, 140)

    def map(self):
        ll = self.line_ed_l1.text(), self.line_ed_l2.text()
        spn = self.s.text()
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


app = QApplication(sys.argv)
ex = Input()
ex.show()
sys.exit(app.exec())

# пример ввода ll - 37.530887 55.703118 | spn - 0.002
