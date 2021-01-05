import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('labeling program')
        self.setFixedSize(850, 500)

        self.label = QLabel(self)
        self.label.setGeometry(30, 30, 700, 400)
        self.label.setStyleSheet("background-color: white")

        self.dog = QRadioButton('Dog', self)
        self.cat = QRadioButton('Cat', self)

        icon = QIcon('red.png')
        self.dog.setIcon(icon)

        icon = QIcon('blue.png')
        self.cat.setIcon(icon)

        self.dog.move(750, 30)
        self.cat.move(750, 60)

        self.dog.setChecked(True)

        dirch = QPushButton('디렉터리 선택', self)
        dirch.setGeometry(30, 450, 120, 30)

        dir = QLabel(self)
        dir.setGeometry(170, 450, 500, 30)
        dir.setStyleSheet("background-color: white;")

        leftbtn = QPushButton("<", self)
        rightbtn = QPushButton(">", self)
        leftbtn.setGeometry(700, 450, 50, 30)
        rightbtn.setGeometry(780, 450, 50, 30)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())