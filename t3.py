import sys
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


class MainWindow(QMainWindow):
    QMap: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('design.ui', self)

        self.map_zoom = 17
        self.map_ll = [30.302348, 59.991619]
        self.map_key = ''

        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_PageUp:
            if self.map_zoom < 21:
                self.map_zoom += 1
        if event.key() == QtCore.Qt.Key.Key_PageDown:
            if self.map_zoom > 0:
                self.map_zoom -= 1
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.map_ll[0] -= 0.001
        if event.key() == QtCore.Qt.Key.Key_Right:
            self.map_ll[0] += 0.001
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.map_ll[1] += 0.0007
        if event.key() == QtCore.Qt.Key.Key_Down:
            self.map_ll[1] -= 0.0007

        self.refresh_map()

    def refresh_map(self):
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'z': self.map_zoom,
            'apikey': api_key
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        response = session.get('https://static-maps.yandex.ru/v1?', params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.QMap.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
