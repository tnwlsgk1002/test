import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import os # 확장자 파일 가져오기

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('labeling program')
        self.setGeometry(300, 300, 850, 500)

        # 라벨
        self.label_list = []
        self.label = QLabel(self)
        #SetCursor 설정
        #Cursor = QCursor(QPixmap('cross.png'))
        #self.label.setCursor(Cursor)
        #self.label.setGeometry(30, 30, 700, 400)
        #self.label.setStyleSheet("background-color: white")

        # 라디오버튼
        self.dog = QRadioButton('Dog', self)
        self.cat = QRadioButton('Cat', self)

        icon = QIcon('red.png')
        self.dog.setIcon(icon)

        icon = QIcon('blue.png')
        self.cat.setIcon(icon)

        #self.dog.move(750, 30)
        #self.cat.move(750, 60)

        self.dog.setChecked(True)

        # 디렉터리 선택 및 표시
        dirbtn = QPushButton('디렉터리 선택', self)
        #dirch.setGeometry(30, 450, 120, 30)
        dirbtn.clicked.connect(self.Directory)

        self.dir = QLineEdit(self)
        self.dir.setReadOnly(True)
        #self.dir.setGeometry(170, 450, 500, 30)
        #self.dir.setStyleSheet("background-color: white;")

        # 이미지 이동 버튼
        leftbtn = QPushButton("<", self)
        rightbtn = QPushButton(">", self)
        leftbtn.setShortcut("Left")
        rightbtn.setShortcut("Right")

        #leftbtn.setGeometry(700, 450, 50, 30)
        #rightbtn.setGeometry(770, 450, 50, 30)

        # 레이아웃 설정
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(leftbtn)
        hbox.addWidget(rightbtn)
        hbox.addStretch(3)
        hbox.addWidget(self.dog)
        hbox.addWidget(self.cat)
        vbox.addLayout(hbox)

        #vbox.addStretch(1)
        vbox.addWidget(self.label)
        #vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addWidget(dirbtn)
        hbox.addWidget(self.dir)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()

    def Directory(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/')
        try:
            self.dir.setText(folder)
            file_list = os.listdir(folder)
            self.label_list = [file for file in file_list if file.endswith(".png") or file.endswith(".jpg")]
            if self.label_list == "":
               pass

            '''
            self.label = Label(folder+"/"+self.label_list[0])
            Cursor = QCursor(QPixmap('cross.png'))
            self.label.setCursor(Cursor)
            self.label.update()
            #self.label.setGeometry(30, 30, 700, 400)
            '''
            image = cv2.imread(folder+"/"+self.label_list[0], cv2.IMREAD_COLOR)
            h, w = image.shape[:2]
            qimage = QImage(image.data, w, h, image.strides[0], QImage.Format_BGR888)
            self.label.setPixmap(QPixmap.fromImage(qimage))

        except FileNotFoundError:
            pass


class Label(QLabel):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.drawing = False
        self.setupUi()
        self.PrevX = None
        self.PrevY = None
        self.NextX = None
        self.NextY = None

    def setupUi(self):
        image = cv2.imread(self.file, cv2.IMREAD_COLOR)
        print(image.shape)
        h, w = image.shape[:2]
        qimage = QImage(image.data, w, h, image.strides[0], QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(qimage))

    def mousePressEvent(self, e):
        pass

    def mouseMoveEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        pass

    def bounding_box(self, x, y):
        pass

    def save(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())