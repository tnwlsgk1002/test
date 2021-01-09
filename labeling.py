import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import os  # 확장자 파일 가져오기
import copy
import natsort


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('labeling program')
        self.setGeometry(300, 300, 500, 500)

        # 라벨
        self.label_list = []
        self.label = Label(self)

        # SetCursor 설정
        Cursor = QCursor(Qt.CrossCursor)
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
        try:
            self.folder = QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/')
            print("self.folder : ", self.folder)
            print(type(self.folder))
            if not self.folder:
                return
            self.dir.setText(self.folder)
            file_list = os.listdir(self.folder)
            self.label_list = [file for file in file_list if file.endswith(".png") or file.endswith(".jpg")]
            self.label_list = natsort.natsorted(self.label_list)
            if not self.label_list:
                return
            self.total = len(self.label_list)
            self.file = self.folder + "/" + self.label_list[0]
            self.n1 = 0 # 현재 label이 label_list에서 무엇을 가리키는 지 알리는 index
            self.label.initPixmap()
            self.label.text_upload()
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
        self.label.text_save()
        if sender == self.leftbtn:
            self.n1 = self.n1 - 1
            if self.n1 == -1:
                self.n1 = len(self.label_list) - 1
        elif sender == self.rightbtn :
            self.n1 = self.n1 + 1
            if self.n1 == len(self.label_list) :
                self.n1 = 0
        self.file = self.folder + "/" + self.label_list[self.n1]
        self.label.initPixmap()
        self.label.text_upload()
        self.label.createPixmap()


class Label(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.drawing = False
        self.removing = False
        self.exist = False
        self.ix = None
        self.iy = None

    def initPixmap(self):
        self.image = cv2.imread(self.parent().file, cv2.IMREAD_COLOR)
        self.h, self.w = self.image.shape[:2]
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.exist = True
        self.parent().resize(self.w + 50, self.h + 50)
        self.resize(self.w, self.h)
        self.text = [] # label 정보가 담긴 2차원 리스트

    # 파일 -> 텍스트
    def text_upload(self):
        try :
            fname = self.parent().file.split('.jpg')
            with open(fname[0] + ".txt", 'r') as file :
                line = None
                while line != '':
                    line = file.readline()
                    line = line.strip('\n')
                    text = line.split(', ')
                    if text == [''] :
                        break
                    xy = list(map(int, text[0:4]))
                    label = [text[4]]
                    self.text.append(xy+label)
        except FileNotFoundError: # 파일이 없는 경우
            return

    # text를 기반으로 pixmap 그리기
    def createPixmap(self):
        for i in self.text:
            if not i:
                pass
            if i[4] == 'Dog':
                self.image = cv2.rectangle(self.image, (i[0], i[1]), (i[2], i[3]), (0, 0, 255))
                self.image = cv2.putText(self.image, 'Dog', ((i[0] + i[2]) // 2, i[1] - 10),
                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif i[4] == 'Cat':
                self.image = cv2.rectangle(self.image, (i[0], i[1]), (i[2], i[3]), (255, 0, 0))
                self.image = cv2.putText(self.image, 'Cat', ((i[0] + i[2]) // 2, i[1] - 10),
                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.parent().resize(self.w + 50, self.h + 50)
        self.resize(self.w, self.h)
        self.repaint()

    def mousePressEvent(self, e):
        if not self.exist:
            return

        if e.button() == Qt.LeftButton:
            self.ix = e.x()
            self.iy = e.y()
            self.drawing = True
            return

        # 삭제
        if e.button() == Qt.RightButton:
            if not self.text :
                return

            remove_index = self.box_exist(e.x(), e.y())
            if remove_index == -1:
                return
            self.image = cv2.imread(self.parent().file, cv2.IMREAD_COLOR)
            self.h, self.w = self.image.shape[:2]

            # text에서 바운딩 박스 삭제
            # text를 바탕으로 self.image에 적용
            self.text.pop(remove_index)
            self.createPixmap()

            return

    # text 안에 바운딩 박스가 있는가 확인
    def box_exist(self, x, y):
        for i in self.text:
            if i == -1:
                break
            if (i[0] <= x and i[1] <= y and i[2] >= x and i[3] >= y) or (
                i[0] >= x and i[1] <= y and i[2] <= x and i[3] >= y) or (
                i[0] >= x and i[1] >= y and i[2] <= x and i[3] <= y) or (
                i[0] <= x and i[1] >= y and i[2] >= x and i[3] <= y) :
                return self.text.index(i)
        return -1

    def mouseMoveEvent(self, e):
        if not self.exist:
            return

        if self.drawing:
            qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
            self.setPixmap(QPixmap.fromImage(qimage))

            img = copy.deepcopy(self.image)
            if self.parent().animalType == 0:
                img = cv2.rectangle(img, (self.ix, self.iy), (e.x(), e.y()), (0, 0, 255))
            else:
                img = cv2.rectangle(img, (self.ix, self.iy), (e.x(), e.y()), (255, 0, 0))
            qimage = QImage(img.data, self.w, self.h, img.strides[0], QImage.Format_BGR888)
            self.setPixmap(QPixmap.fromImage(qimage))
            self.repaint()

    def mouseReleaseEvent(self, e):
        # 삭제 시 그리기 방지
        if e.button() == Qt.RightButton:
            return

        if not self.exist:
            return

        self.drawing = False
        if self.parent().animalType == 0:
            self.image = cv2.rectangle(self.image, (self.ix, self.iy), (e.x(), e.y()), (0, 0, 255))
            self.image = cv2.putText(self.image, 'Dog', ((self.ix + e.x()) // 2, self.iy - 10),
                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            list = [self.ix, self.iy, e.x(), e.y(), 'Dog']
        else:
            self.image = cv2.rectangle(self.image, (self.ix, self.iy), (e.x(), e.y()), (255, 0, 0))
            self.image = cv2.putText(self.image, 'Cat', ((self.ix + e.x()) // 2, self.iy - 10),
                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            list = [self.ix, self.iy, e.x(), e.y(), 'Cat']

        self.text.append(list)
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))


    # 텍스트파일을 저장하여 업로드
    def text_save(self):
        fname = self.parent().file.split('.jpg')
        with open(fname[0] + ".txt", 'w') as file:
            if not self.text :
                return
            for i in self.text:
                if not i:
                    return
                str_i = list(map(str, i))
                text = ', '.join(str_i)
                file.write(text)
                file.write('\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())