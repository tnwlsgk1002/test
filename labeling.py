import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import os # 확장자 파일 가져오기
import copy

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('labeling program')
        self.setGeometry(300, 300, 850, 500)

        # 라벨
        self.label_list = []
        self.label = Label(self)

        #SetCursor 설정
        Cursor = QCursor(QPixmap('cross.png'))
        self.label.setCursor(Cursor)

        # 라디오버튼
        self.dog = QRadioButton('Dog', self)
        icon = QIcon('red.png')
        self.dog.setIcon(icon)
        self.dog.clicked.connect(self.radioclicked)

        self.cat = QRadioButton('Cat', self)
        icon = QIcon('blue.png')
        self.cat.setIcon(icon)
        self.cat.clicked.connect(self.radioclicked)

        self.dog.setChecked(True)

        self.animalType = 0

        # 디렉터리 선택 및 표시
        dirbtn = QPushButton('디렉터리 선택', self)
        dirbtn.clicked.connect(self.Directory)

        self.dir = QLineEdit(self)
        self.dir.setReadOnly(True)

        # 이미지 이동 버튼
        self.leftbtn = QPushButton("<", self)
        self.rightbtn = QPushButton(">", self)
        self.leftbtn.setShortcut("Left")
        self.rightbtn.setShortcut("Right")
        self.leftbtn.clicked.connect(self.movebtnClicked)
        self.rightbtn.clicked.connect(self.movebtnClicked)
        # 레이아웃 설정
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftbtn)
        hbox.addWidget(self.rightbtn)
        hbox.addStretch(3)
        hbox.addWidget(self.dog)
        hbox.addWidget(self.cat)
        vbox.addLayout(hbox)

        vbox.addWidget(self.label)

        hbox = QHBoxLayout()
        hbox.addWidget(dirbtn)
        hbox.addWidget(self.dir)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()

    def Directory(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/')
        try:
            self.dir.setText(self.folder)
            file_list = os.listdir(self.folder)
            self.label_list = [file for file in file_list if file.endswith(".png") or file.endswith(".jpg")]
            if not self.label_list:
               return
            self.file = self.folder+"/"+self.label_list[0]
            self.n1 = 0
            self.label.createPixmap()

        except FileNotFoundError:
            return

    def radioclicked(self):
        sender = self.sender()
        if sender == self.dog:
            self.animalType = 0
        else:
            self.animalType = 1

    def movebtnClicked(self):
        if not self.label_list:
            return
        sender = self.sender()
        self.label.text_upload()
        if sender == self.leftbtn:
            self.n1 = self.n1-1
        else:
            self.n1 = self.n1+1
        self.file = self.folder + "/" + self.label_list[self.n1]
        self.label.createPixmap()



class Label(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.drawing = False
        self.exist = False
        self.ix = None
        self.iy = None
        self.n2 = 0
        self.text = [[-1 for j in range(10)] for i in range(10)] # 0으로 채워진 3차원 리스트

    def createPixmap(self):
        self.image = cv2.imread(self.parent().file, cv2.IMREAD_COLOR)
        self.h, self.w = self.image.shape[:2]
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.exist = True

    def mousePressEvent(self, e):
        if not self.exist :
            return
        if e.button() == Qt.LeftButton:
            self.ix = e.x()
            self.iy = e.y()
            self.drawing = True

    def mouseMoveEvent(self, e):
        if not self.exist :
            return
        if self.drawing:
            qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
            self.setPixmap(QPixmap.fromImage(qimage))

            img = copy.deepcopy(self.image)
            if self.parent().animalType == 0:
                img = cv2.rectangle(img, (self.ix, self.iy), (e.x(), e.y()), (0, 0, 255))
            else :
                img = cv2.rectangle(img, (self.ix, self.iy), (e.x(), e.y()), (255, 0, 0))
            qimage = QImage(img.data, self.w, self.h, img.strides[0], QImage.Format_BGR888)
            self.setPixmap(QPixmap.fromImage(qimage))
            self.repaint()


    def mouseReleaseEvent(self, e):
        if not self.exist :
            return
        self.drawing = False
        if self.parent().animalType == 0:
            self.image = cv2.rectangle(self.image, (self.ix, self.iy), (e.x(), e.y()), (0, 0, 255))
            self.image = cv2.putText(self.image, 'Dog', ((self.ix+e.x())//2, self.iy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            list = [self.ix, self.iy, e.x(), e.y(), 'Dog']
        else:
            self.image = cv2.rectangle(self.image, (self.ix, self.iy), (e.x(), e.y()), (255, 0, 0))
            self.image = cv2.putText(self.image, 'Cat', ((self.ix+e.x())//2, self.iy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            list = [self.ix, self.iy, e.x(), e.y(), 'Cat']
        self.text[self.parent().n1][self.n2] = list
        self.n2 = self.n2 + 1
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))

    def text_upload(self):
        fname = self.parent().file.split('.')
        with open(fname[0]+".txt", 'w') as file :
            for i in self.text:
                for j in i:
                    if j == -1:
                        return
                    for k in j:
                        file.write(str(k)+' ')
                    file.write('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())